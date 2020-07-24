<template lang="html">
  <v-card class="d-flex mx-auto page">
    <v-container fluid class="component">
      <v-card>
        <v-row>
          <v-col class="flex-shrink-1 flex-grow-0" cols="2">
            <Nav/>
          </v-col>
          <v-col class="flex-grow-1 flex-shrink-0" style="max-width:80%;">
            <v-card-title>
              {{ app.Name }}
            </v-card-title>
            <v-card-subtitle> View and Manage {{ app.Name }} </v-card-subtitle>
            <v-card-text>
              <transition
                name="slide"
                enter-active-class="animated slideInRight delay"
                leave-active-class="animated slideOutRight"
                mode="out-in"
              >
                <router-view :app="app" :processes="processes"/>
              </transition>
            </v-card-text>
          </v-col>
        </v-row>
      </v-card>
    </v-container>
  </v-card>
</template>

<script>
import ApplicationDetailsNav from "./ApplicationDetailsComponents/ApplicationDetailsNav";
import { mapActions, mapGetters, mapState } from "vuex";
export default {
  components: {
    Nav: ApplicationDetailsNav,
  },
  data() {
    return {};
  },
  computed: {
    ...mapState("apps", ["apps", "isLoading", "processes"]),
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
      readAppProcesses: "apps/readAppProcesses",
    }),
  },
  created() {
    const appName = this.$route.params.appName;
    this.readApp(appName);
    this.readAppProcesses(appName);
  },
  async mounted() {
    const appName = this.$route.params.appName;
    await this.readApp(appName);
    await this.readAppProcesses(appName);
  },
};
</script>

<style></style>
