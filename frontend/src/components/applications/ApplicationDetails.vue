<template lang="html">
  <v-card class="d-flex mx-auto page">
    <v-container fluid class="component">
      <Nav :isLoading="isLoading" />
      <v-card tile>
        <v-row>
          <v-col class="flex-grow-1 flex-shrink-0">
            <v-card-title>
              {{ app.name }}
            </v-card-title>
            <v-card-subtitle>
              View and Manage {{ app.name }}
              <v-icon v-on:click="refresh()"
                >mdi-refresh</v-icon
              ></v-card-subtitle
            >
            <v-card-text>
              <transition
                name="slide"
                enter-active-class="animated slideInRight delay"
                leave-active-class="animated slideOutRight"
                mode="out-in"
              >
                <router-view :app="app" :processes="processes" :logs="logs" :stats="stats"/>
              </transition>
            </v-card-text>
          </v-col>
        </v-row>
      </v-card>
    </v-container>
  </v-card>
</template>

<script>
import ApplicationDetailsNav from "./ApplicationDetailsComponents/ApplicationDetailsNav";
import { mapActions, mapGetters, mapState } from "vuex";
export default {
  components: {
    Nav: ApplicationDetailsNav,
  },
  data() {
    return {
      logs: [],
      stats: []
    };
  },
  computed: {
    ...mapState("apps", ["apps", "app", "isLoading", "processes"]),
    ...mapGetters({
      getAppByName: "apps/getAppByName",
    }),
    app() {
      const appName = this.$route.params.appName;
      return this.getAppByName(appName);
    },
  },
  methods: {
    ...mapActions({
      readApp: "apps/readApp",
      readAppProcesses: "apps/readAppProcesses",
      // readAppLogs: "apps/readAppLogs",
    }),
    refresh() {
      const appName = this.$route.params.appName;
      this.readApp(appName);
      this.readAppProcesses(appName);
      this.closeLogs();
      this.readAppLogs(appName);
      this.readAppStats(appName)
    },
    readAppLogs(appName) {
      console.log("Starting connection to Websocket");
      this.connection = new WebSocket(
        `ws://${location.hostname}:${location.port}/api/apps/${appName}/livelogs`
      );
      this.connection.onopen = () => {
        this.connection.send(
          JSON.stringify({ type: "onopen", data: "Connected!" })
        );
      };

      this.connection.onmessage = (event) => {
        this.logs.push(event.data);
      };
    },
    closeLogs() {
      this.logs = [];
      this.connection.send(JSON.stringify({ message: "Closing Websocket" }));
      this.connection.close(1001, "Leaving log page or refreshing");
    },
    readAppStats(appName) {
      console.log("Starting connection to Websocket");
      this.statConnection = new WebSocket(
        `ws://${location.hostname}:${location.port}/api/apps/${appName}/stats`
      );
      this.statConnection.onopen = () => {
        this.statConnection.send(
          JSON.stringify({ type: "onopen", data: "Connected!" })
        );
      };

      this.statConnection.onmessage = (event) => {
        this.stats.push(JSON.parse(event.data));
      };
    },
    closeStats() {
      this.stats = [];
      this.statConnection.send(JSON.stringify({ message: "Closing Websocket" }));
      this.statConnection.close(1001, "Leaving stats page or refreshing");
    },
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
  },
};
</script>

<style></style>
