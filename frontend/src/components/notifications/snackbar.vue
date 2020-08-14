<template>
  <v-snackbar v-model="visible" :color="color" :bottom="bottom">
    {{ content }}
    <template v-slot:action="{ attrs }">
      <v-btn text v-bind="attrs" :color="btnColor" @click="clearSnack()">
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
import { mapState, mapMutations } from "vuex";
export default {
  data() {
    return {};
  },
  computed: {
    ...mapState("snackbar", ["content", "bottom", "color", "visible", "btnColor"]),
  },
  methods: {
    ...mapMutations({
      clearSnack: "snackbar/clearSnack",
    }),
  },
};
</script>
