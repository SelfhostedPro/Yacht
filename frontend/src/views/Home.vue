<template>
  <v-card raised>
    <v-container fluid class="templateDetailsContainer component">
      <v-card-title class="primary font-weight-bold">
        Stats <v-icon v-on:click="refresh()">mdi-refresh</v-icon>
      </v-card-title>
      <v-card-text class="secondary text-center px-5 py-5">
        <v-row dense class="mt-3">
          <v-col
            v-for="app in sortByTitle(stats)"
            :key="app.name"
            cols="12"
            xl="2"
            md="2"
            sm="3"
            xs="6"
            class="d-flex"
            style="flex-direction:column"
          >
            <v-card class="flex-grow-1">
              <v-card-title class="pb-0">
                <v-tooltip top transition="scale-transition">
                  <template v-slot:activator="{ on, attrs }">
                    <span v-bind="attrs" v-on="on" @click="handleAppClick(app.name)" class="AppTitle">{{
                      app.name
                    }}</span>
                  </template>
                  <span>{{ app.name }}</span>
                </v-tooltip>
              </v-card-title>
              <v-tooltip bottom transition="scale-transition">
                <template v-slot:activator="{ on, attrs }">
                  <v-card-text
                    v-bind="attrs"
                    v-on="on"
                    class="text-left pt-0 AppTitle"
                  >
                    CPU Usage:
                    {{ app.cpu_percent[app.cpu_percent.length - 1] }}%
                    <br />
                    MEM Usage:
                    {{ app.mem_percent[app.mem_percent.length - 1] }}%,
                    {{
                      formatBytes(app.mem_current[app.mem_current.length - 1])
                    }}
                  </v-card-text>
                </template>
                <span
                  >CPU Usage: {{ app.cpu_percent[app.cpu_percent.length - 1] }}%
                  <br />
                  MEM Usage: {{ app.mem_percent[app.mem_percent.length - 1] }}%,
                  {{ formatBytes(app.mem_current[app.mem_current.length - 1]) }}
                </span>
              </v-tooltip>
              <PercentBarChart
                :chart-id="app.name"
                :chartData="fillStats(app)"
              />
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-container>
  </v-card>
</template>

<script>
import axios from "axios";
import PercentBarChart from "../components/charts/PercentBarChart";
export default {
  components: {
    PercentBarChart
  },
  data() {
    return {
      stats: {}
    };
  },
  methods: {
    readAppStats() {
      console.log("Starting connection to Websocket");
      let url = "/api/users/me";
      axios.get(url, { withCredentials: true }).catch(err => {
        localStorage.removeItem("username");
        window.location.reload();
        console.log(err);
      });
      this.statConnection = new WebSocket(
        `ws://${location.hostname}:${location.port}/api/apps/stats`
      );
      this.statConnection.onopen = () => {
        this.statConnection.send(
          JSON.stringify({ type: "onopen", data: "Connected!" })
        );
      };
      this.statConnection.onmessage = event => {
        let statsGroup = JSON.parse(event.data);
        if (this.stats[statsGroup.name] == null) {
          this.initStats(statsGroup);
        }
        this.stats[statsGroup.name].name = statsGroup.name;
        this.stats[statsGroup.name].cpu_percent.push(
          Math.round(statsGroup.cpu_percent)
        );
        this.stats[statsGroup.name].mem_percent.push(
          Math.round(statsGroup.mem_percent)
        );
        this.stats[statsGroup.name].mem_current.push(statsGroup.mem_current);
        this.stats[statsGroup.name].mem_total.push(statsGroup.mem_total);
        for (let key in this.stats[statsGroup.name]) {
          if (
            this.stats[statsGroup.name][key].length > 5 &&
            Array.isArray(this.stats[statsGroup.name][key])
          ) {
            this.stats[statsGroup.name][key].shift();
          }
        }
        this.$forceUpdate();
      };
    },
    refresh() {
      console.log(this.stats);
      this.closeStats();
      this.readAppStats();
    },
    initStats(statsGroup) {
      this.stats[statsGroup.name] = {};
      this.stats[statsGroup.name].name = "";
      this.stats[statsGroup.name].cpu_percent = [];
      this.stats[statsGroup.name].mem_percent = [];
      this.stats[statsGroup.name].mem_current = [];
      this.stats[statsGroup.name].mem_total = [];
    },
    sortByTitle(arr) {
      let sorted = Object.keys(arr)
        .sort()
        .reduce(
          (acc, key) => ({
            ...acc,
            [key]: arr[key]
          }),
          {}
        );
      return sorted;
    },
    handleAppClick(appName) {
      this.$router.push({ path: `/apps/${appName}/info` });
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
      let datacollection = {
        labels: ["Resource Usage"],
        datasets: [
          {
            label: "CPU Usage",
            backgroundColor: "#41b883",
            data: app.cpu_percent
          },
          {
            label: "Mem Usage",
            backgroundColor: "#FFFFFF",
            data: app.mem_percent
          }
        ]
      };
      return datacollection;
    }
  },
  async mounted() {
    this.readAppStats();
  },
  beforeDestroy() {
    this.closeStats();
  }
};
</script>

<style>
.AppTitle {
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}
</style>
