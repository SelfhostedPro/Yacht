<template>
  <v-card color="foreground" class="mx-4 my-2" raised>
    <v-card-title class="primary font-weight-bold">
      Stats
    </v-card-title>
    <v-card-text
      v-if="app.State.Status != 'running'"
      class="secondary text-center px-5 py-5"
    >
      Start the app to view stats
    </v-card-text>
    <div v-else>
      <v-card color="foreground" flat>
        <v-card-title>
          CPU Usage {{ stats.cpu_percent[stats.cpu_percent.length - 1] }}%
        </v-card-title>
        <v-card-subtitle>
          (0-100%) <br />
          Max: {{ Math.max.apply(Math, stats.cpu_percent) }}%
        </v-card-subtitle>
        <PercentLineChart :chartData="fillCPU(stats.cpu_percent, stats.time)" />
      </v-card>
      <v-card color="foreground" flat>
        <v-card-title>
          Memory Usage {{ stats.mem_percent[stats.mem_percent.length - 1] }}%,
          {{ stats.mem_current[stats.mem_current.length - 1] }}/{{
            stats.mem_total[stats.mem_total.length - 1]
          }}
        </v-card-title>
        <v-card-subtitle>
          (0-100%) <br />
          Max: {{ Math.max.apply(Math, stats.mem_percent) }}%,
          {{ Math.max.apply(Math, stats.mem_current) }}/{{
            stats.mem_total[stats.mem_total.length - 1]
          }}
        </v-card-subtitle>
        <PercentLineChart :chartData="fillMem(stats.mem_percent, stats.time)" />
      </v-card>
    </div>
  </v-card>
</template>

<script>
import PercentLineChart from "../../charts/PercentLineChart";
export default {
  components: {
    PercentLineChart
  },
  props: ["app", "stats"],
  data() {
    return {};
  },
  methods: {
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
            })
          }
        ]
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
            })
          }
        ]
      };
      return datacollection;
    }
  }
};
</script>

<style></style>
