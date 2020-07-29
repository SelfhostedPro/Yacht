import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";
import vuetify from "./plugins/vuetify";
import VueUtils from "./plugins/vueutils";
import "./vee-validate";
require("animate.css/animate.compat.css");

Vue.config.productionTip = false;

const accessToken = localStorage.getItem("accessToken");
if (accessToken) {
  axios.defaults.headers.common = { Authorization: `Bearer ${accessToken}` };
}

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
          console.log(response);
          console.log(error.response.config)
          const accessToken = localStorage.getItem("accessToken");
          const headers = { Authorization: `Bearer ${accessToken}` };
          error.response.config.headers = headers
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
