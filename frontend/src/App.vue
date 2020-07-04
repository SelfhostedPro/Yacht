<template>
  <div id="app">
    <b-navbar id="navbar" toggleable="lg" type="dark" variant="dark" v-if="isAuthenticated">
      <b-navbar-brand href="#">
        <img alt="Vue logo" src="./assets/logo.png" width="32" height="32" />
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <!--
          <router-link to="/dashboard">Dashboard</router-link> |
          -->
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template v-slot:button-content>
              <em>User</em>
            </template>
            <b-dropdown-item @click.native.prevent="logout">Sign Out</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <b-container fluid>
      <b-row>
        <b-col cols="2" v-if="isAuthenticated">
          <b-sidebar
            id="sidebar-big"
            shadow
            no-header-close
            no-close-on-esc
            no-close-on-route-change
          >
            <template v-slot:footer>
              <div class="d-flex bg-dark text-light align-items-center px-3 py-2">
                <b-button squared v-b-toggle="'sidebar-big sidebar-small'">
                  <b-icon-arrow-bar-left></b-icon-arrow-bar-left>
                </b-button>
              </div>
            </template>
            <div class="sidebar-header">
              <img alt="Vue logo" src="./assets/logo.png" width="32" height="32" />
              <h3>Yacht</h3>
              <p>Container Managment UI</p>
            </div>
          </b-sidebar>
          <b-sidebar
            id="sidebar-small"
            width="5em"
            shadow
            no-header-close
            no-close-on-esc
            no-close-on-route-change
            visible
          >
            <template v-slot:footer>
              <div class="d-flex bg-dark text-light align-items-center px-3 py-2">
                <b-button squared v-b-toggle="'sidebar-big sidebar-small'">
                  <b-icon-arrow-bar-right></b-icon-arrow-bar-right>
                </b-button>
              </div>
            </template>
            <div class="sidebar-header">
              <img alt="Vue logo" src="./assets/logo.png" width="32" height="32" />
            </div>
          </b-sidebar>
        </b-col>
        <b-col>
          <router-view id="content" />
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script type="text/javascript">
export default {
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
