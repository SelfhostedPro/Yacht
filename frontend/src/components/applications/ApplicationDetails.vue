<template lang="html">
  <v-card color="foreground" class="d-flex mx-auto page">
    <v-container fluid class="component">
      <Nav class="mb-3" :isLoading="isLoading" />
      <v-card color="foreground" tile>
        <v-row>
          <v-col xs="12" sm="12" md="6" class="flex-grow-1 flex-shrink-0">
            <v-card
              :class="{
                'mx-4 primary': $vuetify.breakpoint.smAndDown,
                'ml-4 primary': $vuetify.breakpoint.mdAndUp
              }"
            >
              <v-card-title>
                {{ app.name }}
                <v-spacer />
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      size="x-small"
                      color="secondary"
                      v-bind="attrs"
                      v-on="on"
                      class="mx-1 my-1 hidden-sm-and-down"
                      @click="editClick({ Name: app.name })"
                    >
                      <span class="hidden-md-and-down">Edit</span>
                      <v-icon>mdi-file-document-edit-outline</v-icon>
                    </v-btn>
                  </template>
                  <span>Edit</span>
                </v-tooltip>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      size="x-small"
                      @click="refresh()"
                      v-bind="{ attrs }"
                      v-on="on"
                      color="secondary"
                      ><v-icon>mdi-refresh</v-icon></v-btn
                    >
                  </template>
                  <span>Refresh</span>
                </v-tooltip>
                <v-menu
                  close-on-click
                  close-on-content-click
                  offset-y
                  class="hidden-md-and-up"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      size="small"
                      color="secondary"
                      v-bind="attrs"
                      v-on="on"
                      class="hidden-md-and-up mx-1"
                    >
                      <v-icon>mdi-chevron-down</v-icon>
                    </v-btn>
                  </template>
                  <v-list color="foreground" class="hidden-md-and-up" dense>
                    <v-list-item @click="editClick({ Name: app.name })">
                      <v-list-item-icon>
                        <v-icon>mdi-file-document-edit-outline</v-icon>
                      </v-list-item-icon>
                      <v-list-item-title>Edit</v-list-item-title>
                    </v-list-item>
                    <v-divider />
                    <v-list-item
                      @click="AppAction({ Name: app.name, Action: 'start' })"
                    >
                      <v-list-item-icon>
                        <v-icon>mdi-play</v-icon>
                      </v-list-item-icon>
                      <v-list-item-title>Start</v-list-item-title>
                    </v-list-item>
                    <v-list-item
                      @click="AppAction({ Name: app.name, Action: 'stop' })"
                    >
                      <v-list-item-icon>
                        <v-icon>mdi-stop</v-icon>
                      </v-list-item-icon>
                      <v-list-item-title>Stop</v-list-item-title>
                    </v-list-item>
                    <v-list-item
                      @click="AppAction({ Name: app.name, Action: 'restart' })"
                    >
                      <v-list-item-icon>
                        <v-icon>mdi-refresh</v-icon>
                      </v-list-item-icon>
                      <v-list-item-title>Restart</v-list-item-title>
                    </v-list-item>
                    <v-divider />
                    <v-list-item
                      @click="AppAction({ Name: app.name, Action: 'kill' })"
                    >
                      <v-list-item-icon>
                        <v-icon>mdi-fire</v-icon>
                      </v-list-item-icon>
                      <v-list-item-title>Kill</v-list-item-title>
                    </v-list-item>
                    <v-list-item
                      @click="AppAction({ Name: app.name, Action: 'remove' })"
                    >
                      <v-list-item-icon>
                        <v-icon>mdi-delete</v-icon>
                      </v-list-item-icon>
                      <v-list-item-title>Remove</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </v-card-title>
            </v-card>
          </v-col>
          <v-spacer class="hidden-sm-and-down" />
          <v-col sm="12" md="6" class="hidden-sm-and-down">
            <v-card
              :class="{
                'mx-4 secondary': $vuetify.breakpoint.smAndDown,
                'mr-4 secondary': $vuetify.breakpoint.mdAndUp
              }"
            >
              <v-card-title class="d-flex justify-space-between">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      v-bind="{ attrs }"
                      v-on="on"
                      class="mx-1 my-1"
                      @click="AppAction({ Name: app.name, Action: 'start' })"
                    >
                      <span class="hidden-md-and-down">start</span>
                      <v-icon>mdi-play</v-icon>
                    </v-btn>
                  </template>
                  <span>Start</span>
                </v-tooltip>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      v-bind="{ attrs }"
                      v-on="on"
                      class="mx-1 my-1"
                      @click="AppAction({ Name: app.name, Action: 'stop' })"
                    >
                      <span class="hidden-md-and-down">stop</span>
                      <v-icon>mdi-stop</v-icon>
                    </v-btn>
                  </template>
                  <span>Stop</span>
                </v-tooltip>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      v-bind="{ attrs }"
                      v-on="on"
                      class="mx-1 my-1"
                      @click="AppAction({ Name: app.name, Action: 'restart' })"
                    >
                      <span class="hidden-md-and-down">restart</span>
                      <v-icon>mdi-refresh</v-icon>
                    </v-btn>
                  </template>
                  <span>Restart</span>
                </v-tooltip>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      v-bind="attrs"
                      v-on="on"
                      class="mx-1 my-1"
                      @click="AppAction({ Name: app.name, Action: 'kill' })"
                    >
                      <span class="hidden-md-and-down">kill</span>
                      <v-icon>mdi-fire</v-icon>
                    </v-btn>
                  </template>
                  <span>Kill</span>
                </v-tooltip>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      v-bind="attrs"
                      v-on="on"
                      class="mx-1 my-1"
                      @click="AppAction({ Name: app.name, Action: 'remove' })"
                    >
                      <span class="hidden-md-and-down">remove</span>
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </template>
                  <span>Remove</span>
                </v-tooltip>
              </v-card-title>
            </v-card>
          </v-col>
        </v-row>
        <transition
          name="slide"
          enter-active-class="animated slideInRight delay"
          leave-active-class="animated slideOutRight"
          mode="out-in"
        >
          <router-view
            :app="app"
            :processes="processes"
            :logs="logs"
            :stats="stats"
          />
        </transition>
      </v-card>
    </v-container>
  </v-card>
</template>

<script>
import ApplicationDetailsNav from "./ApplicationDetailsComponents/ApplicationDetailsNav";
import { mapActions, mapGetters, mapState } from "vuex";
export default {
  components: {
    Nav: ApplicationDetailsNav
  },
  data() {
    return {
      logs: [],
      stats: {
        time: [],
        cpu_percent: [],
        mem_percent: [],
        mem_current: [],
        mem_total: []
      },
      connection: null,
      statConnection: null
    };
  },
  computed: {
    ...mapState("apps", ["apps", "app", "isLoading", "processes"]),
    ...mapGetters({
      getAppByName: "apps/getAppByName"
    }),
    app() {
      const appName = this.$route.params.appName;
      return this.getAppByName(appName);
    }
  },
  methods: {
    ...mapActions({
      readApp: "apps/readApp",
      readAppProcesses: "apps/readAppProcesses",
      AppAction: "apps/AppAction"
    }),
    editClick(appName) {
      this.$router.push({ path: `/apps/edit/${appName.Name}` });
    },
    refresh() {
      const appName = this.$route.params.appName;
      this.readApp(appName);
      this.readAppProcesses(appName);
      this.closeLogs();
      this.closeStats();
      this.readAppLogs(appName);
      this.readAppStats(appName);
    },
    readAppLogs(appName) {
      var proto = "";
      if (location.protocol == "http:") {
        proto = "ws://";
      } else {
        proto = "wss://";
      }
      this.connection = new WebSocket(
        `${proto}${location.hostname}:${location.port}/api/apps/${appName}/livelogs`
      );
      this.connection.onopen = () => {
        this.connection.send(
          JSON.stringify({ type: "onopen", data: "Connected!" })
        );
      };

      this.connection.onmessage = event => {
        this.logs.push(event.data);
      };
    },
    closeLogs() {
      this.logs = [];
      this.connection.send(JSON.stringify({ message: "Closing Websocket" }));
      this.connection.close(1000, "Leaving page or refreshing");
      // this.connection.close("Leaving page or refreshing", 1001);
    },
    readAppStats(appName) {
      var sproto = "";
      if (location.protocol == "http:") {
        sproto = "ws://";
      } else {
        sproto = "wss://";
      }

      this.statConnection = new WebSocket(
        `${sproto}${location.hostname}:${location.port}/api/apps/${appName}/stats`
      );
      this.statConnection.onopen = () => {
        this.statConnection.send(
          JSON.stringify({ type: "onopen", data: "Connected!" })
        );
      };
      this.statConnection.onmessage = event => {
        let statsGroup = JSON.parse(event.data);
        this.stats.time.push(statsGroup.time);
        this.stats.cpu_percent.push(Math.round(statsGroup.cpu_percent));
        this.stats.mem_percent.push(Math.round(statsGroup.mem_percent));
        this.stats.mem_current.push(statsGroup.mem_current);
        this.stats.mem_total.push(statsGroup.mem_total);
        for (let key in this.stats) {
          if (this.stats[key].length > 300) {
            this.stats[key].shift();
          }
        }
      };
    },
    closeStats() {
      this.stats.time = [];
      this.stats.cpu_percent = [];
      this.stats.mem_percent = [];
      this.stats.mem_current = [];
      this.stats.mem_total = [];
      this.statConnection.send(
        JSON.stringify({ message: "Closing Websocket" })
      );
      this.statConnection.close(1000, "Leaving page or refreshing");
      // this.statConnection.close(1001, "Leaving page or refreshing");
    }
  },
  created() {
    const appName = this.$route.params.appName;
    this.readApp(appName);
    this.readAppProcesses(appName);
  },
  async mounted() {
    const appName = this.$route.params.appName;
    await this.readApp(appName);
    await this.readAppProcesses(appName);
    await this.readAppLogs(appName);
    await this.readAppStats(appName);
  },
  beforeDestroy() {
    this.closeLogs();
    this.closeStats();
  }
};
</script>

<style></style>
