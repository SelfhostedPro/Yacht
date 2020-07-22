import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import VueUtils from "./plugins/vueutils";
import "./vee-validate";
require('animate.css/animate.compat.css');

Vue.config.productionTip = false;

Vue.use(VueUtils);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");