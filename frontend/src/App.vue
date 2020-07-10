<template>
  <div id="app">
    <!-- <Navbar></Navbar> -->
    <b-container fluid>
      <b-row no-gutters> 
        <b-col cols="1" >
          <Sidebar v-if="isAuthenticated"></Sidebar>
        </b-col>
        <b-col>
          <!-- <b-overlay :show="loading" variant="white" rounded="sm"> -->
            <router-view id="content" />
          <!-- </b-overlay>  -->
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script type="text/javascript">
import { mapState } from "vuex";
// import Navbar from "./components/nav/Navbar";
import Sidebar from "./components/nav/Sidebar";
export default {
  components: {
    Sidebar: Sidebar,
    // Navbar: Navbar,
  },
  computed: {
    ...mapState("templates", ["templates", "loading"]),
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

<style lang="scss">
@import "./assets/_custom.scss";
@import "~bootstrap/scss/bootstrap.scss";
@import "~bootstrap-vue/src/index.scss";

  #app {
    text-align: center;
    color: #2c3e50;
  }
</style>
