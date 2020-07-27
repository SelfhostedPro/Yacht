<template>
  <div>
    <v-tabs mobile-breakpoint="sm">
      <v-tab class="text-left" :to="{ path: 'info' }">
        <v-icon left class="mr-1">mdi-information-outline</v-icon>Info
      </v-tab>
      <v-tab class="text-left" :to="{ path: 'top' }">
        <v-icon left class="mr-1">mdi-view-list-outline</v-icon>Processes
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
      return {}
    },
  props: ["isLoading"],
};
</script>

<style>
.floating-menu {
  z-index: 1;
}
</style>
