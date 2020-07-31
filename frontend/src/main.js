// Setup Vue
import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
// API Calls
import axios from "axios";
// UI Framework
import vuetify from "./plugins/vuetify";
// Form Validation
import VueUtils from "./plugins/vueutils";
import "./vee-validate";
// Websockets
// Animations
require("animate.css/animate.compat.css");

// Socket.io

Vue.config.productionTip = false;

// Handle Token Refresh on 401
function createAxiosResponseInterceptor() {
  const interceptor = axios.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response.status !== 401) {
        return Promise.reject(error);
      }

      axios.interceptors.response.eject(interceptor);

      return store
        .dispatch("auth/AUTH_REFRESH")
        .then((response) => {
          console.log(response)
          console.log(error.response.config)
          return axios(error.response.config);
        })
        .catch((error) => {
          store.dispatch("auth/AUTH_LOGOUT");
          this.router.push("/");
          return Promise.reject(error);
        })
        .finally(createAxiosResponseInterceptor);
    }
  );
}

// Call interceptor
createAxiosResponseInterceptor();
Vue.use(VueUtils);

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
