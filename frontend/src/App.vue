<template>
  <v-app id="yacht">
    <div v-if="isLoggedIn">
      <Sidebar />
      <Appbar />
      <v-main>
        <!-- Provides the application the proper gutter -->
        <v-container fluid>
          <!-- If using vue-router -->
          <transition
            name="slide"
            enter-active-class="animated slideInRight delay"
            leave-active-class="animated slideOutLeft"
          >
            <router-view></router-view>
          </transition>
        </v-container>
      </v-main>

      <!--
    <v-footer app>
       <span class="px-4">&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  -->
    </div>
    <div v-else>
      <v-container fluid>
        <LoginForm />
      </v-container>
    </div>
  </v-app>
</template>

<script>
import { mapGetters } from "vuex";
import Sidebar from "./components/nav/Sidebar";
import Appbar from "./components/nav/Appbar";
import LoginForm from "./components/auth/LoginForm";
export default {
  name: "App",

  components: {
    Sidebar: Sidebar,
    Appbar: Appbar,
    LoginForm: LoginForm,
  },

  data: () => ({}),
  computed: {
    ...mapGetters({
      isLoggedIn: "auth/isLoggedIn",
    }),
  },
  created() {
    document.addEventListener("beforeunload", this.logout);
  },
};
</script>

<style>
html {
  overflow-y: auto;
  background-color: black;
}
.animated {
  --animate-duration: 0.3s;
}
.fast-anim {
  --animate-duration: 0.1s;
}
#yacht {
  display: flex;
  width: 100vw;
}
.page {
  position: relative;
  flex-grow: 1;
}
.component {
  position: absolute;
  min-width: 100%;
}
</style>
