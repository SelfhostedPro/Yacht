<template>
  <div id="app">
    <!-- <Navbar></Navbar> -->
    <b-container fluid>
      <b-row no-gutters v-if="isLoggedIn"> 
        <b-col cols="1" >
          <Sidebar />
        </b-col>
        <b-col>
          <!-- <b-overlay :show="loading" variant="white" rounded="sm"> -->
            <router-view id="content" />
          <!-- </b-overlay>  -->
        </b-col>
      </b-row>
      <b-row v-else>
       <LoginForm />
      </b-row>
    </b-container>
  </div>
</template>

<script type="text/javascript">
import { mapActions, mapGetters } from "vuex";
import LoginForm from "./components/auth/LoginForm";
import Sidebar from "./components/nav/Sidebar";
export default {
  components: {
    LoginForm,
    Sidebar: Sidebar,
  },
  data() {
    return {};
  },
  computed: {
    ...mapGetters({
      isLoggedIn: "auth/isLoggedIn"
    })
  },
  methods: {
    ...mapActions({
      logout: "auth/logout"
    })
  },
  created() {
    document.addEventListener("beforeunload", this.logout);
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
