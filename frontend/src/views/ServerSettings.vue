<template lang="html">
  <v-card color="foreground" class="d-flex mx-auto page">
    <v-container fluid class="component">
      <Nav class="mb-3" />
      <v-card color="foreground" tile>
        <v-row>
          <v-col class="flex-grow-1 flex-shrink-0">
            <v-card-title>
              Server Settings
            </v-card-title>
            <v-card-subtitle> Manage Server Settings </v-card-subtitle>
            <v-card-text>
              <transition
                name="slide"
                enter-active-class="animated fadeIn delay"
                leave-active-class="animated fadeOut"
                mode="out-in"
              >
                <router-view />
              </transition>
            </v-card-text>
          </v-col>
        </v-row>
        <v-card-text>Version: {{ version }}</v-card-text>
      </v-card>
    </v-container>
  </v-card>
</template>

<script>
// import { mapState } from "vuex";
import ServerSettingsNav from "../components/serverSettings/ServerSettingsNav";
export default {
  data() {
    return {
      version: process.env.VUE_APP_VERSION || "unreleased"
    };
  },
  components: {
    Nav: ServerSettingsNav
  }
};
</script>

<style></style>
