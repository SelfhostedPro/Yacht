<template lang="html">
  <div class="app-details component">
    <h1>Test</h1>
    <h2 v-if="item">hi</h2>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
export default {
  data() {
    return {};
  },
  computed: {
    ...mapState("apps", ["apps", "isLoading"]),
    ...mapGetters({
      getAppByName: "apps/getAppByName",
    }),
    app() {
      const appName = this.$route.params.appName;
      return this.getAppByName(appName);
    },
  },
  methods: {
    ...mapActions({
      readApp: "apps/readApp",
    }),
  },
  created() {
    const appName = this.$route.params.appName;
    this.readApp(appName);
    console.log("From created"+this.getAppByName(appName));
  },
};
</script>