<template>
  <div class="app-details component">
    <h1>Test</h1>
    <h2 v-if="app">hi</h2>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
export default {
  methods: {
    ...mapActions({
      readApp: "apps/readApp",
    }),
    created() {
      const appName = this.$route.params.appName;
      this.readApp(appName);
      console.log(this.getAppByName(appName));
    },
  },
  computed: {
    ...mapState("apps", ["apps", "isLoading"]),
  },
  app() {
    const appName = this.$route.params.appName;
    return this.getAppById(appName);
  },
  async mounted() {
    const appName = this.$route.params.appName;
    console.log(this.readApp(appName));
    await this.readApp(appName);
  },
};
</script>
