<template>
  <div id="app">
    <Navbar v-if="isAuthenticated"></Navbar>
    <b-container fluid>
      <b-row no-gutters> 
        <b-col cols="1" >
          <Sidebar v-if="isAuthenticated"></Sidebar>
        </b-col>
        <b-col>
          <router-view id="content" />
        </b-col>
      </b-row>
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
  },
  methods: {
    logout() {
      console.log("logout");
      this.$store.dispatch("auth/logout").then(() => {
        this.$router.push("/");
      });
    }
  },
  created() {
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
  z-index: 2000;
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
