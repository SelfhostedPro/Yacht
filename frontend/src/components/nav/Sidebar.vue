<template>
    <v-navigation-drawer
      app
      clipped
      permanent
      mini-variant
      expand-on-hover>
      <!-- -->

      <v-list nav dense>

        <v-list-item to="/">
          <v-list-item-icon>
            <v-icon>mdi-view-dashboard</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Dashboard</v-list-item-title>
        </v-list-item>

        <v-divider />

        <v-list-group
          prepend-icon="mdi-folder"
          :value="false">

          <template v-slot:activator>
            <v-list-item-title>My Templates</v-list-item-title>
          </template>

          <v-list-item link to="/templates/">
            <v-list-item-icon>
              <v-icon>mdi-view-list</v-icon>
            </v-list-item-icon>
            <v-list-item-title>View Templates</v-list-item-title>
          </v-list-item>

          <v-list-item link to="/templates/new">
            <v-list-item-icon>
              <v-icon>mdi-plus</v-icon>
            </v-list-item-icon>
            <v-list-item-title>New Template</v-list-item-title>
          </v-list-item>

        </v-list-group>

        <v-list-group
          prepend-icon="mdi-application"
          :value="false">

          <template v-slot:activator>
            <v-list-item-title>My Applications</v-list-item-title>
          </template>

          <v-list-item link to="/apps">
            <v-list-item-icon>
              <v-icon>mdi-view-list</v-icon>
            </v-list-item-icon>
            <v-list-item-title>View Applications</v-list-item-title>
          </v-list-item>

          <v-list-item link to="/apps">
            <v-list-item-icon>
              <v-icon>mdi-plus</v-icon>
            </v-list-item-icon>
            <v-list-item-title>New Application</v-list-item-title>
          </v-list-item>

        </v-list-group>


        <v-list-group
          prepend-icon="mdi-package"
          :value="false">

          <template v-slot:activator>
            <v-list-item-title>My Container</v-list-item-title>
          </template>

          <v-list-item link>
            <v-list-item-icon to="/images">
              <v-icon>mdi-view-list</v-icon>
            </v-list-item-icon>
            <v-list-item-title>View Container</v-list-item-title>
          </v-list-item>

          <v-list-item link to="/images">
            <v-list-item-icon>
              <v-icon>mdi-plus</v-icon>
            </v-list-item-icon>
            <v-list-item-title>New Container</v-list-item-title>
          </v-list-item>

        </v-list-group>

      </v-list>

    </v-navigation-drawer>
</template>