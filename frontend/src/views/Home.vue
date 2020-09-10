<template>
  <v-card raised>
    <v-container fluid class="templateDetailsContainer component">
      <v-card-title class="primary font-weight-bold">
        Stats
      </v-card-title>
      <v-card-text class="secondary text-center px-5 py-5">
        All application stats
        <v-icon v-on:click="refresh()">mdi-refresh</v-icon>
      </v-card-text>
      <v-row dense class="mt-3">
        <v-col
          v-for="(app, index) in stats"
          :key="index"
          cols="12"
          xl="2"
          md="3"
          sm="4"
          xs="12"
          class="d-flex"
          style="flex-direction:column"
        >
          <v-card class="flex-grow-1">
            <v-card-title v-text="app.name"></v-card-title>
            <PercentBarChart :chartData="fillStats(app)" />
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import PercentBarChart from "../components/charts/PercentBarChart";
export default {
  components: {
    PercentBarChart,
  },
  data() {
    return {
      stats: {},
    };
  },
  methods: {
    readAppStats() {
      console.log("Starting connection to Websocket");
      this.statConnection = new WebSocket(
        `ws://${location.hostname}:${location.port}/api/apps/stats`
      );
      this.statConnection.onopen = () => {
        this.statConnection.send(
          JSON.stringify({ type: "onopen", data: "Connected!" })
        );
      };
      this.statConnection.onmessage = (event) => {
        let statsGroup = JSON.parse(event.data);
        if (this.stats[statsGroup.name] == null) {
          this.initStats(statsGroup);
        }
        this.stats[statsGroup.name].name = statsGroup.name;
        this.stats[statsGroup.name].cpu_percent.push(statsGroup.cpu_percent);
        this.stats[statsGroup.name].mem_percent.push(statsGroup.mem_percent);
        // let statObject = {
        //   time: statsGroup.time,
        //   name: statsGroup.name,
        //   cpu_percent: [Math.round(statsGroup.cpu_percent)],
        //   mem_percent: [Math.round(statsGroup.mem_percent)],
        // };
        // this.$set(this.stats, statsGroup.name, statObject)
        // this.stats[statsGroup.name] = Object.assign(
        //   {},
        //   this.stats[statsGroup.name],
        //   statObject
        // );
        console.log(this.stats)
      };
    },
    refresh() {
      this.closeStats();
      this.readAppStats();
    },
    initStats(statsGroup) {
      this.stats[statsGroup.name] = {};
      this.stats[statsGroup.name].name = "";
      this.stats[statsGroup.name].cpu_percent = [];
      this.stats[statsGroup.name].mem_percent = [];
    },
    closeStats() {
      this.stats = {};
      this.statConnection.send(
        JSON.stringify({ message: "Closing Websocket" })
      );
      this.statConnection.close(1000, "Leaving page or refreshing");
    },
    formatBytes(bytes) {
      if (bytes === 0) return "0 Bytes";
      const decimals = 2;
      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

      const i = Math.floor(Math.log(bytes) / Math.log(k));

      return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
    },
    fillStats(app) {
      console.log(app);
      let datacollection = {
        labels: ["CPU Usage", "MEM Usage"],
        datasets: [
          {
            label: "CPU Usage",
            backgroundColor: "#41b883",
            lineTension: 0,
            pointRadius: 0,
            data: app.cpu_percent,
          },
          {
            label: "Mem Usage",
            backgroundColor: "#FFFFFF",
            lineTension: 0,
            pointRadius: 0,
            data: app.mem_percent,
          },
        ],
      };
      console.log(datacollection);
      return datacollection;
    },
  },
  async mounted() {
    this.readAppStats();
  },
  beforeDestroy() {
    this.closeStats();
  },
};
</script>

<style></style>
