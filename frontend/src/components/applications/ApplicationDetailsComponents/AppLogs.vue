<template>
  <v-card raised>
    <v-card-title class="primary font-weight-bold">
      Logs
    </v-card-title>
    <v-card-text
      v-if="app.State.Status != 'running'"
      class="secondary text-center px-5 py-5"
    >
      Start the app to view logs
    </v-card-text>
    <v-virtual-scroll
      v-else
      :bench="20"
      :items="logs"
      height="600"
      item-height="20"
      class="keep-whitespace"
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
  props: ["app", "logs"],
  data() {
    return {
    };
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
.keep-whitespace {
  white-space:pre
}
</style>
