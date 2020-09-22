<template>
  <div>
    <v-tabs mobile-breakpoint="sm">
      <v-tab class="text-left" :to="{ path: 'info' }">
        <v-icon left class="mr-1">mdi-information-outline</v-icon>Info
      </v-tab>
      <v-tab class="text-left" :to="{ path: 'templateVariables' }">
        <v-icon left class="mr-1">mdi-view-list-outline</v-icon>Template
        Variables
      </v-tab>
    </v-tabs>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  }
};
</script>

<style>
.floating-menu {
  z-index: 1;
}
</style>
