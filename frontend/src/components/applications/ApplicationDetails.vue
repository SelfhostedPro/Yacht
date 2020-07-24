<template lang="html">
  <v-card class="d-flex mx-auto">
    <v-container fluid class="component">
      <v-card>
        <v-row justify="space-between">
          <v-col cols="auto" class="text-center px-0">
            <v-row class="flex-column ma-0 fill-height">
              <Nav />
            </v-row>
          </v-col>

          <v-col cols="auto" class="flex-grow-1">
            <v-card-title>
              {{ app.Name }}
            </v-card-title>
            <v-card-subtitle> View and Manage {{ app.Name }} </v-card-subtitle>
            <v-card-text>
              <transition
                name="slide"
                enter-active-class="animated slideInRight delay"
                leave-active-class="animated slideOutLeft"
              >
                <router-view />
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
  },
  async mounted() {
    const appName = this.$route.params.appName;
    await this.readApp(appName);
  },
};
</script>
