<template>
  <div>
    <v-card tile raised class="flex-grow-1">
      <v-card-title class="subheading primary font-weight-bold">
        General
      </v-card-title>
      <!-- <v-card-subtitle>
              General container information
            </v-card-subtitle> -->
      <v-divider />
      <v-list class="secondary px-5">
        <v-list-item>
          <v-list-item-content
            ><v-list-item-title class="font-weight-bold"
              >Container Name</v-list-item-title
            ></v-list-item-content
          >
          <v-list-item-content>
            <v-list-item-title>
              {{ app.name }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider />

        <v-list-item>
          <v-list-item-content
            ><v-list-item-title class="font-weight-bold"
              >Container ID</v-list-item-title
            ></v-list-item-content
          >
          <v-list-item-content>
            <v-list-item-title>
              {{ app.short_id }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider />

        <v-list-item>
          <v-list-item-content
            ><v-list-item-title class="font-weight-bold"
              >Container Created On</v-list-item-title
            ></v-list-item-content
          >
          <v-list-item-content>
            <v-list-item-title>
              {{ app.Created | formatDate }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider />

        <v-list-item>
          <v-list-item-content
            ><v-list-item-title class="font-weight-bold"
              >Container Status</v-list-item-title
            ></v-list-item-content
          >
          <v-list-item-content>
            <v-list-item-title>
              {{ app.State.Status }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card>
    <v-card v-if="app.ports" tile>
      <v-card-title class="subheading indigo darken-2 font-weight-bold">
        Ports
      </v-card-title>
      <v-divider />
      <v-card-text
        v-if="app.State.Status != 'running'"
        class="secondary text-center px-5 py-5"
      >
        Start the app to view ports
      </v-card-text>
      <v-simple-table v-else class="secondary px-0 text-center">
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-center"> Label </th>
              <th class="text-center">Container Port</th>
              <th class="text-center">Host IP</th>
              <th class="text-center">Host Port</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(port, index) in convPorts(app.ports)" :key="index">
              <td>{{app.Config.Labels[`local.yacht.port.${port.hport}`]}}</td>
              <td>{{ port.cport }}</td>
              <td>{{ port.hip }}</td>
              <td>
                <v-chip
                  v-if="port.hip == '0.0.0.0'"
                  color="indigo darken-2"
                  label
                  :href="'http://' + host_ip + ':' + port.hport"
                  target="_blank"
                  ><v-icon small class="mr-1">mdi-link-variant</v-icon
                  >{{ port.hport }}</v-chip
                ><v-chip
                  v-else
                  color="indigo darken-2"
                  label
                  :href="'http://' + port.hip + ':' + port.hport"
                  target="_blank"
                  ><v-icon small class="mr-1">mdi-link-variant</v-icon
                  >{{ port.hport }}</v-chip
                >
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card>
    <v-card v-if="app.Mounts" tile>
      <v-card-title class="subheading amber darken-2 font-weight-bold">
        Volumes
      </v-card-title>
      <v-divider />
      <v-card-text
        v-if="app.State.Status != 'running'"
        class="secondary text-center px-5 py-5"
      >
        Start the app to view volumes
      </v-card-text>
      <v-simple-table v-else class="secondary px-0 text-center">
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-center">Container Path</th>
              <th class="text-center">Host Path</th>
              <th class="text-center">Mode</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(mount, index) in app.Mounts" :key="index">
              <td>{{ mount.Destination }}</td>
              <td>{{ mount.Source }}</td>
              <td>{{ mount.Mode }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card>
    <v-card v-if="app.Config.Env" tile>
      <v-card-title class="subheading green darken-3 font-weight-bold">
        Environment Variables
      </v-card-title>
      <v-divider />
      <v-card-text
        v-if="app.State.Status != 'running'"
        class="secondary text-center px-5 py-5"
      >
        Start the app to view volumes
      </v-card-text>
      <v-simple-table v-else class="secondary px-0 text-center">
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-center">Label</th>
              <th class="text-center">Data</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(env, index) in splitEnv(app.Config.Env)" :key="index">
              <td>{{ env[0] }}</td>
              <td>{{ env[1] }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card>
    <v-card tile raised v-if="app.HostConfig.CapAdd || app.HostConfig.Sysctls || app.HostConfig.Devices || app.Config.Labels">
      <v-card-title class="subheading primary font-weight-bold">
        Advanced
      </v-card-title>
      <!-- <v-card-subtitle>
              General container information
            </v-card-subtitle> -->
      <v-divider />
      <v-list class="secondary px-5">
        <v-list-item v-if="app.HostConfig.CapAdd">
          <v-list-item-content
            ><v-list-item-title class="font-weight-bold"
              >Added Capabilities</v-list-item-title
            ></v-list-item-content
          >
          <v-list-item-content>
            <v-list-item-title
              v-for="(cap, index) in app.HostConfig.CapAdd"
              :key="index"
            >
              {{ cap }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider v-if="app.HostConfig.CapAdd" />

        <v-list-item v-if="app.HostConfig.Devices">
          <v-list-item-content
            ><v-list-item-title class="font-weight-bold"
              >Mapped Devices</v-list-item-title
            ></v-list-item-content
          >
          <v-list-item-content>
            <v-list-item-title
              v-for="(device, index) in app.HostConfig.Devices"
              :key="index"
            >
              {{ device.PathOnHost + ':' + device.PathInContainer + ':' + device.CgroupPermissions }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider v-if="app.HostConfig.Devices" />
        <v-list-item v-if="app.Config.Labels">
          <v-list-item-content
            ><v-list-item-title class="font-weight-bold"
              >Container Labels</v-list-item-title
            ></v-list-item-content
          >
          <v-list-item-content>
            <v-list-item-title
              v-for="(label, index) in Object.entries(app.Config.Labels)"
              :key="index"
            >
              <p class="float-left"> {{label[0]}}:</p> <p class="float-right"> {{label[1]}} </p>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider v-if="app.Config.Labels" />
        <v-list-item v-if="app.HostConfig.Sysctls">
          <v-list-item-content
            ><v-list-item-title class="font-weight-bold"
              >Sysctls</v-list-item-title
            ></v-list-item-content
          >
          <v-list-item-content>
            <v-list-item-title
              v-for="(sysctl, index) in Object.keys(app.HostConfig.Sysctls)"
              :key="index"
            >
              {{ sysctl }} = {{ app.HostConfig.Sysctls[sysctl] }},
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      host_ip: location.hostname
    };
  },
  props: ["app"],
  methods: {
    convPorts(data) {
      let o = [];
      for (var k in data) {
        if (data[k]) {
          o = o.concat(
            data[k].map(function(x) {
              return { cport: k, hip: x.HostIp, hport: x.HostPort };
            })
          );
        }
      }
      return o;
    },
    refresh() {
      const appName = this.$route.params.appName;
      this.readApp(appName);
      this.readAppProcesses(appName);
    },
    splitEnv(data) {
      const env = [];
      for (let index = 0; index < data.length; index++) {
        let _split_data = data[index].split("=");
        env.push(_split_data);
      }
      return env;
    }
  }
};
</script>
