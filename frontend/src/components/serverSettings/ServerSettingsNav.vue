<template>
  <div>
    <v-tabs background-color="tabs" mobile-breakpoint="sm">
      <v-tab class="text-left" :to="{ path: 'info' }">
        <v-icon left class="mr-1">mdi-information-outline</v-icon>Info
      </v-tab>
      <v-tab class="text-left" :to="{ path: 'theme' }">
        <v-icon left class="mr-1">mdi-format-color-fill</v-icon>Theme
      </v-tab>
      <v-tab class="text-left" :to="{ path: 'templateVariables' }">
        <v-icon left class="mr-1">mdi-view-list-outline</v-icon>Template
        Variables
      </v-tab>
      <v-tab class="text-left" :to="{ path: 'prune' }">
        <v-icon left class="mr-1">mdi-trash-can-outline</v-icon>
        Prune
      </v-tab>
      <v-tab class="text-left" :to="{ path: 'update' }">
        <v-icon left class="mr-1">mdi-update</v-icon>
        Update
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
