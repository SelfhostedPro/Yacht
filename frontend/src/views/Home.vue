<template>
  <v-card raised>
    <v-container fluid class="templateDetailsContainer component">
      <v-card-title class="primary font-weight-bold">
        Stats
      </v-card-title>
      <v-card-text class="secondary text-center px-5 py-5">
        All application stats
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
          <v-card-text>CPU Usage {{ app.cpu_percent[app.cpu_percent.length - 1] }}%</v-card-text>
          <!-- <PercentLineChart :chartData="fillCPU(app.cpu_percent, app.time)" /> -->
        </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
// import PercentLineChart from "../components/charts/PercentLineChart";
export default {
  components: {
    // PercentLineChart
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
        this.stats[statsGroup.name].time.push(statsGroup.time);
        this.stats[statsGroup.name].cpu_percent.push(
          Math.round(statsGroup.cpu_percent)
        );
        this.stats[statsGroup.name].mem_percent.push(
          Math.round(statsGroup.mem_percent)
        );
        this.stats[statsGroup.name].mem_current.push(statsGroup.mem_current);
        this.stats[statsGroup.name].mem_total.push(statsGroup.mem_total);
        for (let key in this.stats[statsGroup.name]) {
          if (this.stats[statsGroup.name][key].length > 300) {
            this.stats[statsGroup.name][key].shift();
          }
        }
      };
    },
    initStats(statsGroup) {
      this.stats[statsGroup.name] = {};
      this.stats[statsGroup.name].name = statsGroup.name
      this.stats[statsGroup.name].time = [];
      this.stats[statsGroup.name].cpu_percent = [];
      this.stats[statsGroup.name].mem_percent = [];
      this.stats[statsGroup.name].mem_current = [];
      this.stats[statsGroup.name].mem_total = [];
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
    fillCPU(stat, time) {
      let datacollection = {
        datasets: [
          {
            label: "CPU Usage",
            backgroundColor: "#41b883",
            lineTension: 0,
            pointRadius: 0,
            data: time.map((t, i) => {
              return { x: t, y: stat[i] };
            }),
          },
        ],
      };
      return datacollection;
    },
    fillMem(stat, time) {
      let datacollection = {
        datasets: [
          {
            label: "Memory Usage",
            backgroundColor: "#41b883",
            lineTension: 0,
            pointRadius: 0,
            data: time.map((t, i) => {
              return { x: t, y: stat[i] };
            }),
          },
        ],
      };
      return datacollection;
    },
  },
  async mounted() {
    await this.readAppStats();
  },
};
</script>

<style></style>
