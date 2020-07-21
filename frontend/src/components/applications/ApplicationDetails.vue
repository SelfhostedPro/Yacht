<template>
    <h1 v-if="apps">Test</h1>
</template>

<script>
import { mapActions, mapState } from "vuex";
export default {
  data() {},
  methods: {
    ...mapActions({
      readApp: "apps/readApp",
      AppAction: "apps/AppAction",
    }),
    handleRowClick(appName) {
      this.$router.push({ path: `/apps/${appName.Name}` });
    },
    // templateDetails(templateId) {
    //   this.$router.push({ path: `/templates/${templateId}` });
    // }
    debug(value) {
      console.log(value);
    },
  },
  computed: {
    ...mapState("apps", ["apps", "isLoading"]),
  },
  mounted() {
    this.readApps();
  },
};
</script>