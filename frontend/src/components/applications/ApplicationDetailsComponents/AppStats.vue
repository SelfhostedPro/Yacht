<template>
  <v-card raised>
    <v-card-title class="primary font-weight-bold">
      Stats {{stats.cpu_percent}} {{stats.mem_percent}}
    </v-card-title>
    <v-card-text
      v-if="app.State.Status != 'running'"
      class="secondary text-center px-5 py-5"
    >
      Start the app to view logs
    </v-card-text>
    <apexchart type="line" :options="options" :series="series" />
  </v-card>
</template>

<script>
// import axios from "axios";
export default {
  props: ["app", "stats"],
  data() {
    return {
      options: {
        chart: {
          id: 'stats_chart'
        },
        animations: {
          enabled: true,
          erasing: 'linear',
          dynamicAction: {
            speed: 10
          }
        },
        xaxis: {
          type: 'datetime',
        },
        yaxis: {
          max: 100
        }
      }
    };
  },
  methods: {
    formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];      
    }
  },
  computed: {
    stat_comp() {
      var cpu_percent = this.$props
    },
    series() {
      console.log(this.$props.stats)
      return [
        {
        name: 'mem_cpu',
        data: [this.$props.stats.cpu_percent]
        }
      ]
    }
  }
};
</script>

<style>
#logtext {
  font: 1rem Inconsolata, monospace;
}
#logcontainer {
  background-color: black;
}
.keep-whitespace {
  white-space:pre
}
</style>
