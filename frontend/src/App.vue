<template>
  <div id="app">
    <Navbar v-if="isAuthenticated"></Navbar>
    <b-container fluid>
      <Sidebar v-if="isAuthenticated"></Sidebar>
      <router-view id="content" />
    </b-container>
  </div>
</template>

<script type="text/javascript">
import Navbar from "./components/nav/Navbar";
import Sidebar from "./components/nav/Sidebar";
export default {
  components: {
    Navbar: Navbar,
    Sidebar: Sidebar
  },
  computed: {
    isAuthenticated() {
      return this.$store.getters["auth/isAuthenticated"];
    }
  }
};
</script>

<style>
#app {
  text-align: center;
  color: #2c3e50;
}
#navbar {
  min-height: 4em;
}
#sidebar-small {
  top: 4em;
  max-height: calc(100vh - 4rem);
}
#sidebar-big {
  top: 4em;
  max-height: calc(100vh - 4rem);
}
</style>
