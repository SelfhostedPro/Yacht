<template lang="html">
  <div class="apps-list component" style="max-width: 90%">
    <v-card>
      <v-fade-transition>
        <v-progress-linear
          indeterminate
          v-if="isLoading"
          color="primary"
          bottom
        />
      </v-fade-transition>
      <v-card-title>
        Apps
        <v-menu close-on-click close-on-content-click offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon size="small" v-bind="attrs" v-on="on">
              <v-icon>mdi-chevron-down</v-icon>
            </v-btn>
          </template>
          <v-list dense>
            <v-list-item @click="refresh()">
              <v-list-item-icon><v-icon>mdi-refresh</v-icon></v-list-item-icon>
              <v-list-item-title>Refresh Apps</v-list-item-title>
            </v-list-item>
            <v-list-item @click="checkUpdates()">
              <v-list-item-icon><v-icon>mdi-update</v-icon></v-list-item-icon>
              <v-list-item-title>Check for updates</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
        <v-menu
          :close-on-content-click="false"
          bottom
          offset-y
          color="secondary"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn v-bind="attrs" v-on="on" class="ml-2">
              Columns
            </v-btn>
          </template>
          <v-list>
            <v-list-item
              color="primary"
              v-for="(item, index) in headers"
              :key="index"
            >
              <v-checkbox
                v-model="selectedHeaders"
                :label="item.text"
                :value="item"
                multiple
              >
              </v-checkbox>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-card-title>
      <v-card-subtitle v-if="action">{{ action }} </v-card-subtitle>
      <v-data-table
        style="width: 99%"
        class="mx-auto"
        :headers="selectedHeaders"
        :items="apps"
        :items-per-page="10"
        :search="search"
        @click:row="handleRowClick"
        single-select
      >
        <template v-slot:item.name="{ item }">
          <div class="namecell">
            <v-menu :close-on-click="true" :close-on-content-click="true" offset-y>
              <template v-slot:activator="{ on, attrs }">
                <v-btn icon size="small" v-bind="attrs" v-on="on" class="">
                  <v-icon>mdi-chevron-down</v-icon>
                </v-btn>
              </template>
              <v-list dense>
                <v-list-item
                  @click="AppAction({ Name: item.name, Action: 'start' })"
                >
                  <v-list-item-icon>
                    <v-icon>mdi-play</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>Start</v-list-item-title>
                </v-list-item>
                <v-list-item
                  @click="AppAction({ Name: item.name, Action: 'stop' })"
                >
                  <v-list-item-icon>
                    <v-icon>mdi-stop</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>Stop</v-list-item-title>
                </v-list-item>
                <v-list-item
                  @click="AppAction({ Name: item.name, Action: 'restart' })"
                >
                  <v-list-item-icon>
                    <v-icon>mdi-refresh</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>Restart</v-list-item-title>
                </v-list-item>
                <v-divider
                  v-if="
                    !item.Config.Image.includes('selfhostedpro/yacht') &&
                      updatable.includes(item.name)
                  "
                />
                <v-list-item
                  v-if="
                    !item.Config.Image.includes('selfhostedpro/yacht') &&
                      updatable.includes(item.name)
                  "
                  @click="AppAction({ Name: item.name, Action: 'update' })"
                >
                  <v-list-item-icon>
                    <v-icon>mdi-update</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>Update</v-list-item-title>
                </v-list-item>
                <v-divider />
                <v-list-item
                  @click="AppAction({ Name: item.name, Action: 'kill' })"
                >
                  <v-list-item-icon>
                    <v-icon>mdi-fire</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>Kill</v-list-item-title>
                </v-list-item>
                
                    <v-list-item @click="AppAction({ Name: item.name, Action: 'remove' })">
                      <v-list-item-icon>
                        <v-icon>mdi-delete</v-icon>
                      </v-list-item-icon>
                      <v-list-item-title>Remove</v-list-item-title>
                    </v-list-item>
                  
              </v-list>
            </v-menu>
            <span class="nametext ml-1">{{ item.name }}</span>
            <v-tooltip
              right
              v-if="updatable.includes(item.name)"
              color="primary"
              class="mb-2"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-avatar
                  class="ml-1"
                  v-bind="attrs"
                  v-on="on"
                  color="primary"
                  size="6"
                ></v-avatar>
              </template>
              <span>Update Available</span>
            </v-tooltip>
          </div>
        </template>
        <template v-slot:item.project="{ item }">
          <div class="projectcell">
            <span
              >{{ item.Config.Labels["com.docker.compose.project"] || "-" }}
            </span>
          </div>
        </template>
        <template v-slot:item.status="{ item }">
          <div class="statuscell">
            <span>{{ item.State.Status }} </span>
          </div>
        </template>
        <template v-slot:item.ports="{ item }">
          <ins v-for="(port, index) in convPorts(item.ports)" :key="index">
            <v-tooltip top transition="scale-transition">
              <template v-slot:activator="{ on, attrs }">
                <v-chip
                  v-on="on"
                  v-bind="attrs"
                  class="mx-1"
                  v-if="port.hip == '0.0.0.0'"
                  color="indigo darken-2"
                  label
                  small
                  :href="'http://' + host_ip + ':' + port.hport"
                  target="_blank"
                  ><v-icon small class="mr-1">mdi-link-variant</v-icon
                  >{{
                    item.Config.Labels[`local.yacht.port.${port.hport}`] ||
                      port.hport
                  }}</v-chip
                >
                <v-chip
                  v-on="on"
                  v-bind="attrs"
                  class="ma-1"
                  v-else
                  color="indigo darken-2"
                  label
                  small
                  :href="'http://' + port.hip + ':' + port.hport"
                  target="_blank"
                  ><v-icon small class="mr-1">mdi-link-variant</v-icon
                  >{{
                    item.Config.Labels[`local.yacht.port.${port.hport}`] ||
                      port.hport
                  }}</v-chip
                >
              </template>
              <span>
                {{ port.hport }}
              </span>
            </v-tooltip>
          </ins>
        </template>
        <template v-slot:item.image="{ item }">
          <span class="ImageName">{{ item.Config.Image }}</span>
        </template>
        <template v-slot:item.created="{ item }">
          <span class="CreatedAt"> {{ item.Created | formatDate }} </span>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
export default {
  data() {
    return {
      search: "",
      expanded: [],
      removeDialog: false,
      host_ip: location.hostname,
      headers: [],
      headersMap: {
        name: {
          text: "Name",
          value: "name",
          sortable: true,
          align: "start",
          // width: "30%",
        },
        project: {
          text: "Project",
          value: "project",
          sortable: true,
        },
        status: {
          text: "Status",
          value: "status",
          sortable: true,
          // width: "10%",
        },
        image: {
          text: "Image",
          value: "image",
          sortable: true,
        },
        ports: {
          text: "Ports",
          value: "ports",
          sortable: true,
        },
        created: {
          text: "Created At",
          value: "created",
          sortable: true,
        },
      },
      selectedHeaders: [],
    };
  },
  methods: {
    ...mapActions({
      readApps: "apps/readApps",
      AppAction: "apps/AppAction",
      checkUpdates: "apps/checkAppsUpdates",
    }),
    handleRowClick(appName) {
      this.$router.push({ path: `/apps${appName.Name}/info` });
    },
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
      this.readApps();
    },
  },
  computed: {
    ...mapState("apps", ["apps", "isLoading", "action", "updatable"]),
    showHeaders() {
      return this.headers.filter((s) => this.selectedHeaders.includes(s));
    },
  },
  created() {
    console.log(this.headersMap);
    this.headers = Object.values(this.headersMap);
    this.selectedHeaders = this.headers;
  },
  mounted() {
    this.readApps();
  },
};
</script>

<style>
tr:hover {
  cursor: pointer;
}
.ImageName {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.CreatedAt {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.namecell {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>
