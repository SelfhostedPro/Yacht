<template>
  <v-card raised>
    <v-card-title class="primary font-weight-bold">
      Logs
    </v-card-title>
    <v-virtual-scroll
      :bench="20"
      :items="this.$props.logs"
      height="600"
      item-height="20"
      class="text-no-wrap"
      id="logcontainer"
    >
      <template v-slot="{ item }">
        <div id="logtext">
          {{ item }}
        </div>
      </template>
    </v-virtual-scroll>
  </v-card>
</template>

<script>
// import axios from "axios";
export default {
  props: ["logs"],
  data() {
    return {};
  },
};
</script>

<style>
#logtext {
  font: 1rem Inconsolata, monospace;
}
#logcontainer {
  background-color: black;
}
</style>
