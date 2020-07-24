<template>
  <v-card raised>
    <v-card-title class="primary font-weight-bold">
      Processes
    </v-card-title>
    <v-card-text v-if="app.processes">
      Working
    </v-card-text>
    <v-card-text v-else>
      not working
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: ['app', 'processes'],
};
</script>