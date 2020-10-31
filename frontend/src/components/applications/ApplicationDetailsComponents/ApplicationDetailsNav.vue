<template>
  <div>
    <v-tabs background-color="tabs" mobile-breakpoint="sm">
      <v-tab class="text-left" @click="$router.go(-1)">
        <v-icon left class="mr-1">mdi-arrow-left-bold-outline</v-icon> Back
      </v-tab>
      <v-tab class="text-left" :to="{ path: 'info' }">
        <v-icon left class="mr-1">mdi-information-outline</v-icon>Info
      </v-tab>
      <v-tab class="text-left" :to="{ path: 'top' }">
        <v-icon left class="mr-1">mdi-view-list-outline</v-icon>Processes
      </v-tab>
      <v-tab class="text-left" :to="{ path: 'logs' }">
        <v-icon left class="mr-1">mdi-book-open-outline</v-icon>Logs
      </v-tab>
      <v-tab class="text-left" :to="{ path: 'stats' }">
        <v-icon left class="mr-1">mdi-gauge</v-icon>Stats
      </v-tab>
    </v-tabs>
    <v-fade-transition>
      <v-progress-linear
        indeterminate
        v-if="isLoading"
        color="primary"
        bottom
      />
    </v-fade-transition>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  props: ["isLoading"]
};
</script>

<style>
.floating-menu {
  z-index: 1;
}
</style>
