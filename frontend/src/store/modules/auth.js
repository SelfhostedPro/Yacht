import axios from "axios";
// import router from "@/router";

// where ot use this
// axios.interceptors.request.use(
//   config => {
//     console.log("intercept requ - config");
//     return config;
//   },
//   error => {
//     console.log("intercept requ - error", error);
//     return Promise.reject();
//   });
//
// axios.interceptors.response.use(
//   response => {
//     console.log("intercept resp - response");
//     return response;
//   },
//   error => {
//     // handle 401 error here!
//     console.log("intercept resp - error", error);
//     if (401 === error.response.status) {
//       // logout
//     }
//     return Promise.reject();
//   });


const state = {
  // single source of data
  username: localStorage.getItem("username") || "",
  accessToken: localStorage.getItem("access_token") || "",
  refreshToken: localStorage.getItem("refresh_token") || ""
};

const getters = {
  isAuthenticated(state) {
    return !!state.accessToken;
  }
};

const mutations = {
  // isolated data mutations
  setAuth(state, data) {
    state.username = data.username;
    state.accessToken = data.access_token;
    state.refreshToken = data.refresh_token;
  },
  clearAuth(state) {
    state.username = "";
    state.accessToken = "";
    state.refreshToken = "";
  }
};

const actions = {
  login(context, credentials) {
    return new Promise((resolve, reject) => {
      axios
        .post("/api/auth/login", {
          username: credentials.username,
          password: credentials.password
        })
        .then(response => {
          console.log(response.data);

          localStorage.setItem("username", credentials.username);
          localStorage.setItem("access_token", response.data.access_token);
          localStorage.setItem("refresh_token", response.data.refresh_token);

          context.commit("setAuth", {
            username: credentials.username,
            access_token: response.data.access_token,
            refresh_token: response.data.refresh_token
          });

          axios.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${response.data.access_token}`;

          resolve(response);
        })
        .catch(error => {
          console.error(error);

          context.commit("clearAuth");

          localStorage.removeItem("username");
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");

          delete axios.defaults.headers.common["Authorization"];

          reject(error);
        });
    });
  },
  logout(context) {
    return new Promise(resolve => {
      // axios
      //   .post('/api/logout')
      //   .then(response => {
      //     localStorage.removeItem("username");
      //     localStorage.removeItem("access_token");
      //     localStorage.removeItem("refresh_token");
      //     context.commit("clearAuth")
      //     delete axios.defaults.headers.common["Authorization"];
      //     resolve()
      //   })
      //   .catch(error => {
      //     localStorage.removeItem("username");
      //     localStorage.removeItem("access_token");
      //     localStorage.removeItem("refresh_token");
      //     context.commit("clearAuth")
      //     delete axios.defaults.headers.common["Authorization"];
      //     reject()
      //   });
      context.commit("clearAuth");
      localStorage.removeItem("username");
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      delete axios.defaults.headers.common["Authorization"];
      resolve();
    });
  },
  // register() {},
  refreshTokens() {
    // TODO
  },
  autoRefresh() {
    // TODO perhaps moe to app
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  getters,
  actions
};