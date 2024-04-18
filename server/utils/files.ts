import { join, extname, dirname, basename } from 'node:path'
import { mkdirp, pathExists, outputFile } from 'fs-extra/esm'
import { readFile } from 'fs/promises'
import dree from 'dree';
import { fileURLToPath } from 'url'
import type { CallbackAsync, Dree, ScanOptions, } from 'dree';
import { useNuxtApp } from 'nuxt/app';

export const dataDir = useRuntimeConfig().yacht.configOptions.dataPath

export const initData = async () => {
    const dataExists = await pathExists(dataDir)
    if (!dataExists) {
        mkdirp(dataDir)
        console.log('creating data dir')
    }
}
interface GetTreeRootProps {
    options?: ScanOptions,
    path?: string,
    relative?: boolean,
    onFile?: CallbackAsync<Dree>,
    onDir?: CallbackAsync<Dree>
}

export const getTreeRoot = async ({ path, options, onFile, onDir, relative }: GetTreeRootProps) => {
    await initData()
    let rootPath = path
    if (relative) {
        rootPath = join(dataDir, path || '')
    }
    if (rootPath && !rootPath.startsWith(dataDir)) throw createError(`${path} is outside of the data directory!!!`)
    return await dree.scanAsync(rootPath || dataDir, options, onFile, onDir)
}

export const getFile = async (path: string) => {
    await initData()
    // const filePath = join(dataDir, path)
    if (!path.startsWith(dataDir)) throw createError(`${path} is outside of the data directory!!!`)
    return {
        name: basename(path),
        extension: extname(path),
        path: path,
        content: (await readFile(path, { encoding: 'utf-8' })).toString()
    }
}

export const saveFile = async (path: string, content: string) => {
    await initData()
    const filePath = join(dataDir, path)
    if (!filePath.startsWith(dataDir)) throw createError(`${filePath} is outside of the data directory!!!`)
    await outputFile(join(dataDir, path), content)
    Logger.sucess(`File ${path} saved!`, 'lvfiles - saveFile', { message: `File ${path} saved!`, level: 'success', timeout: 3000, title: 'Saved!' })
    return getFile(path)
}