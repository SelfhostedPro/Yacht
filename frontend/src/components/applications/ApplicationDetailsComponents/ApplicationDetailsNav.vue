<template>
  <v-tabs vertical>
    <v-tab class="text-left" :to="{ path: 'info' }"> <v-icon class="mr-1">mdi-information-outline</v-icon>Info </v-tab>
    <v-tab class="text-left" :to="{ path: 'top' }"> <v-icon class="mr-1">mdi-view-list-outline</v-icon>Processes </v-tab>
  </v-tabs>
</template>

<style>
.floating-menu {
  z-index: 1;
}
</style>