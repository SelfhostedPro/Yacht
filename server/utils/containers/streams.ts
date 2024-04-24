import { type FixedContainerStats, formatStats } from "./formatter"
import { PassThrough as StreamPassThrough } from "stream"

// Service Dependency Imports
import type { ServerDict } from "~/types/servers"

export const getContainerStats = async (close: () => void, send: (callback: (id: number) => any) => void) => {
    const servers = Object.entries(await useServers())
    // Get all servers
    servers.map(
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        async ([_server, docker]): Promise<void> => {

            // Get all containers on server
            const containers = await docker?.listContainers({ all: true }).catch((e) => {
                createError(e)
                return undefined
            })
            if (containers === undefined) {
                close()
                return
            } else {
                containers.map(
                    async (container) => {
                        if (container.State === 'running') {
                            // Get container object
                            const _container = docker?.getContainer(container.Id)
                            if (_container !== undefined) {

                                // Cache stats so we only send when they change
                                let cachedStats: FixedContainerStats | null = null;
                                // Placeholder string to assemble chunks of data
                                let partialChunk = '';

                                // Start streaming stats
                                _container.stats({ stream: true }, (err, stream) => {
                                    stream?.on('data', (data: Buffer) => {
                                        const chunkString = partialChunk + data.toString() // turn the chunk buffer into a string
                                        const jsonChunks = chunkString.split('\n'); // Split on newlines
                                        partialChunk = jsonChunks.pop() || ''; // Store any incomplete chunk for the next iteration
                                        jsonChunks.forEach((jsonChunk) => {
                                            const containerStats: FixedContainerStats = JSON.parse(jsonChunk);
                                            if (
                                                !cachedStats ||
                                                containerStats.name !== cachedStats.name ||
                                                containerStats.cpu_stats.cpu_usage.total_usage !== cachedStats.cpu_stats.cpu_usage.total_usage ||
                                                containerStats.memory_stats.usage !== cachedStats.memory_stats.usage
                                            ) {
                                                cachedStats = containerStats;
                                                send(() => formatStats(containerStats))
                                                sseHooks.callHook("sse:containerStats", formatStats(containerStats));
                                            }
                                        });
                                    })
                                })
                            }
                        }
                    }
                )
            }
        },
    )
}

export const getContainerLogs = async (server: string, id: string, close: () => void, send: (callback: (id: number) => any) => void) => {
    const _server = await useServers().then((servers: ServerDict) => servers[server])
    if (!_server) throw createError(new Error(`Server ${server} not found!`))
    const logStream = new StreamPassThrough()

    // Placeholder string to assemble chunks of data
    logStream.on('data', async (chunk) => {
        send(() => chunk.toString('utf8'))
        console.log(chunk.toString('utf8'))
    });

    const container = _server.getContainer(id)
    const running = await container.inspect().then((container) => container.State.Running)

    container.logs(
        {
            follow: true,
            stdout: true,
            stderr: true,
            timestamps: false,
        },
        (error, stream) => {
            container.modem.demuxStream(stream, logStream, logStream);
            if (stream) {
                stream.on('end', () => {
                    logStream.end('!stop!')
                    close()
                })
            } else {
                console.log('error getting stream', error)
            }
        }
    )

    // else {
    //     console.log('container not running')
    // }
}