<template>
  <v-app id="yacht">
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
  </v-app>
</template>

<script>
import Sidebar from "./components/nav/Sidebar";
import Appbar from "./components/nav/Appbar";
export default {
  name: "App",

  components: {
    Sidebar: Sidebar,
    Appbar: Appbar,
  },

  data: () => ({}),
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
