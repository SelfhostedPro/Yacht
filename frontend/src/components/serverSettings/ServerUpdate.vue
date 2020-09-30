<template>
  <v-card>
    <v-card-title class="subheading primary font-weight-bold"
      >Prune</v-card-title
    >
    <v-card-text class="mt-2"
      >Update Yacht to the latest version. <br/> Note: This will kill the running version of Yacht, Pull the latest version of the current tag, and run that with the same settings that are currently set.</v-card-text
    >
    <v-btn
      class="mx-5 mb-5"
      color="primary"
      @click="update()"
    >
      Update Yacht
    </v-btn>
  </v-card>
</template>

<script>
import axios from "axios";
import { mapMutations } from "vuex";
export default {
  data() {
    return {
      containerDialog: false,
    };
  },
  methods: {
    ...mapMutations({
      setMessage: "snackbar/setMessage",
      setErr: "snackbar/setErr",
    }),
    formatBytes(bytes) {
      if (bytes === 0) return "0 Bytes";
      const decimals = 2;
      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

      const i = Math.floor(Math.log(bytes) / Math.log(k));

      return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
    },
    update() {
      axios({
        url: "/api/settings/update",
        method: "GET",
        responseType: "text/json",
      })
        .then((response) => {
          console.log(response.data);
          this.setMessage(
            "Yacht is updating now"
          );
        })
        .catch((err) => {
          this.setErr(err);
        });
    },
  },
};
</script>
