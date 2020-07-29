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
// let isRefreshing = false;

// axios.interceptors.response.use(
//   (response) => {
//     return response;
//   },
//   (err) => {
//     const {
//       config,
//       response: { status, data },
//     } = err;

//     const originalRequest = config;

//     if (status === 401 && data.message === "Token has expired") {
//       if (!isRefreshing) {
//         isRefreshing = true;
//         store
//           .dispatch("auth/AUTH_REFRESH")
//           .then(({ status }) => {
//             if (status === 200 || status === 204) {
//               isRefreshing = false;
//               return new Promise((resolve, reject) => {
//                 axios
//                   .request(originalRequest)
//                   .then((response) => {
//                     resolve(response);
//                   })
//                   .catch((error) => {
//                     reject(error);
//                   });
//               });
//             }
//           })
//           .catch((error) => {
//             console.error(error);
//           });
//       }
//     } else {
//       store.dispatch("auth/AUTH_LOGOUT")
//     }
//   }
// );

// const interceptor = axios.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     if (errorResponse.status !== 401) {
//       return Promise.reject(error);
//     }

//     axios.interceptors.response.eject(interceptor);

//     return store
//       .dispatch("auth/AUTH_REFRESH")
//       .then((response) => {
//         console.log(response);
//         return axios(error.response.config);
//       })
//       .catch((error) => {
//         store.dispatch("auth/AUTH_CLEAR");
//         this.router.push("/");
//         return Promise.reject(error);
//       });
//   }
// );

Vue.use(VueUtils);

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
