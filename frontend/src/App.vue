<template>
  <v-app id="yachtrevue">
    <Sidebar />
    <Appbar />

    <v-main>
      <!-- Provides the application the proper gutter -->
      <v-container fluid>
        <!-- If using vue-router -->
        <router-view></router-view>
      </v-container>
    </v-main>

    <!--
    <v-footer app>
       <span class="px-4">&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  -->
  </v-app>
</template>

<script>
import Sidebar from "./components/nav/Sidebar";
import Appbar from "./components/nav/Appbar"
export default {
  name: "App",

  components: {
    Sidebar:Sidebar,
    Appbar:Appbar,
  },

  data: () => ({}),
};
</script>

<style>
html{
  overflow-y:auto;
}
</style>