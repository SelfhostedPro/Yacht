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
                <router-view
                  :app="app"
                  :processes="processes"
                  :logs="logs"
                  :stats="stats"
                />
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
      readAppProcesses: "apps/readAppProcesses"
      // readAppLogs: "apps/readAppLogs",
    }),
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
      console.log("Starting connection to Logs");
      this.connection = new WebSocket(
        `ws://${location.hostname}:${location.port}/api/apps/${appName}/livelogs`
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
      console.log("Starting connection to Stats");

      this.statConnection = new WebSocket(
        `ws://${location.hostname}:${location.port}/api/apps/${appName}/stats`
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
