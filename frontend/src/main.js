import Vue from "vue";
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

Vue.config.productionTip = false;
Vue.prototype.$http = axios;
// Vue.prototype.$http.interceptors.response.use(
//   response => {
//     console.log("intercept resp - response");
//     return response;
//   },
//   error => {
//     // handle 401 error here!
//     console.log("intercept resp - error", error);
//     if (error.response && error.response.status === 401) {
//       store.commit("clearAuth");
//       localStorage.removeItem("username");
//       localStorage.removeItem("access_token");
//       localStorage.removeItem("refresh_token");
//       delete axios.defaults.headers.common["Authorization"];
//       router.push('/')
//     }
//     return Promise.reject();
//   });

// Hmmm ?
const token = localStorage.getItem("access_token");
if (token) {
  Vue.prototype.$http.defaults.headers.common[
    "Authorization"
  ] = `Bearer ${token}`;
}
//  else {
//   router.push("/");
// }

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
