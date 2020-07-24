<template>
  <div>
    <v-card raised class="flex-grow-1">
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
            ><v-list-title class="font-weight-bold"
              >Container Name</v-list-title
            ></v-list-item-content
          >
          <v-list-item-content>
            <v-list-title>
              {{ app.name }}
            </v-list-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider />

        <v-list-item>
          <v-list-item-content
            ><v-list-title class="font-weight-bold"
              >Container ID</v-list-title
            ></v-list-item-content
          >
          <v-list-item-content>
            <v-list-title>
              {{ app.short_id }}
            </v-list-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider />

        <v-list-item>
          <v-list-item-content
            ><v-list-title class="font-weight-bold"
              >Container Created On</v-list-title
            ></v-list-item-content
          >
          <v-list-item-content>
            <v-list-title>
              {{ app.Created | formatDate }}
            </v-list-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider />

        <v-list-item>
          <v-list-item-content
            ><v-list-title class="font-weight-bold"
              >Container Status</v-list-title
            ></v-list-item-content
          >
          <v-list-item-content>
            <v-list-title>
              {{ app.State.Status }}
            </v-list-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card>
    <v-card v-if="app.ports" tile>
      <v-card-title class="subheading indigo darken-2 font-weight-bold">
        Ports
      </v-card-title>
      <v-divider />
      <v-simple-table class="secondary px-0 text-center">
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-center">Container Port</th>
              <th class="text-center">Host IP</th>
              <th class="text-center">Host Port</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(port, index) in convPorts(app.ports)" :key="index">
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
  </div>
</template>

<script>
export default {
  data() {
    return {
      host_ip: location.hostname,
    };
  },
  props: ["app"],
  methods: {
    convPorts(data) {
      let o = [];
      for (var k in data) {
        o = o.concat(
          data[k].map(function(x) {
            console.log(x.HostIp);
            return { cport: k, hip: x.HostIp, hport: x.HostPort };
          })
        );
      }
      return o;
    },
  },
};
</script>
