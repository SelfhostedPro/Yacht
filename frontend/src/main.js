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
// Animations
require("animate.css/animate.compat.css");

Vue.config.productionTip = false;

// Handle Token Refresh on 401
function createAxiosResponseInterceptor() {
  const interceptor = axios.interceptors.response.use(
    response => response,
    error => {
      if (error.response.status !== 401) {
        return Promise.reject(error);
      }

      axios.interceptors.response.eject(interceptor);

      return store
        .dispatch("auth/AUTH_REFRESH")
        .then(() => {
          error.response.config.xsrfCookieName = "csrf_access_token";
          error.response.config.xsrfHeaderName = "X-CSRF-TOKEN";
          console.log(error.response.config);
          return axios(error.response.config);
        })
        .catch(error => {
          if (error.response.status != 401) {
            return Promise.reject(error);
          } else {
            store.dispatch("auth/AUTH_LOGOUT");
            this.router.push("/");
            return Promise.reject(error);
          }
        })
        .finally(() => {
          createAxiosResponseInterceptor();
        });
    }
  );
}

// Vue.component('apexchart', VueApexCharts)

// Call interceptor
createAxiosResponseInterceptor();
Vue.use(VueUtils);
new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
