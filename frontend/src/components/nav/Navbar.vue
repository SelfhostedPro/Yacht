<template>
  <b-navbar id="navbar" toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand href="#">
      <img alt="Vue logo" src="@/assets/logo.png" width="32" height="32" />
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
</template>

<script>
export default {
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