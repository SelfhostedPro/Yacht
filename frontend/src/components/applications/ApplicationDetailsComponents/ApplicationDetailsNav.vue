<template>
  <v-card class="component floating-menu">
    <v-navigation-drawer floating permanent expand-on-hover right width="20vw">
      <v-list nav dense>
        <v-list-item :to="{ path: 'info' }">
          <v-list-icon> <v-icon>mdi-information-outline</v-icon> </v-list-icon>
          <v-list-item-content>
            <v-list-item-title class="ml-1"> Info </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item :to="{ path: 'top' }">
          <v-list-icon> <v-icon>mdi-view-list-outline</v-icon> </v-list-icon>
          <v-list-item-content>
            <v-list-item-title class="ml-1"> Processes </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </v-card>
</template>

<style>
.floating-menu {
  z-index: 1;
}
</style>
