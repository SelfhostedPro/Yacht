import {
  AUTH_REQUEST,
  AUTH_ERROR,
  AUTH_SUCCESS,
  AUTH_LOGOUT,
  // AUTH_REFRESH,
  AUTH_CLEAR,
  AUTH_CHANGE_PASS,
} from "../actions/auth";
import axios from "axios";
import router from "@/router/index";

const state = {
  status: "",
  username: localStorage.getItem("username") || "",
};

const getters = {
  isAuthenticated: (state) => !!state.username,
  authStatus: (state) => state.status,
  getUsername: (state) => state.username,
};

const actions = {
  [AUTH_REQUEST]: ({ commit }, credentials) => {
    return new Promise((resolve, reject) => {
      commit(AUTH_REQUEST);
      const url = "/api/auth/login";
      const formData = new FormData();
      formData.set('username', credentials.username);
      formData.set('password', credentials.password)
      axios
        .post(url, formData, { withCredentials: true })
        .then(() => {
          let url = "/api/users/me";
          axios
            .get(url, { withCredentials: true })
            .then((resp) => {
              console.log(resp)
              localStorage.setItem("username", resp.data.email);
              axios.defaults.withCredentials = true;
              commit(AUTH_SUCCESS, resp);
              resolve(resp);
            })
            .catch((err) => {
              commit(AUTH_ERROR, err);
              localStorage.removeItem("username");
              reject(err);
            });
        })
        .catch((err) => {
          commit(AUTH_ERROR, err);
          localStorage.removeItem("username");
          reject(err);
        });
    });
  },

  [AUTH_LOGOUT]: ({ commit }) => {
    return new Promise((resolve) => {
      commit(AUTH_REQUEST);
      const url = "/api/auth/logout";
      axios
        .post(
          url,
          {},
          { withCredentials: true }
        )
        .then((resp) => {
          commit(AUTH_CLEAR, resp);
          localStorage.removeItem("username");
          router.push({ path: "/" });
          resolve(resp);
        })
        .catch((error) => {
          console.log(error);
          commit(AUTH_CLEAR);
        });
    });
  },
  // [AUTH_REFRESH]: ({ commit }) => {
  //   return new Promise((resolve) => {
  //     commit(AUTH_REQUEST);
  //     const url = "/api/auth/refresh";
  //     axios
  //       .post(url, {}, { xsrfCookieName: "csrf_refresh_token", xsrfHeaderName: "X-CSRF-TOKEN", withCredentials: true })
  //       .then((resp) => {
  //         resolve(resp);
  //       })
  //       .catch((error) => {
  //         console.log(error);
  //         commit(AUTH_CLEAR);
  //       });
  //   });
  // },
  [AUTH_CHANGE_PASS]: ({ commit }, credentials) => {
    return new Promise((resolve, reject) => {
      commit(AUTH_REQUEST);
      const url = "/api/users/me";
      let password = credentials.password
      let email = credentials.username
      console.log(email, password)
      axios
        .patch(url, {
            password: password,
            email: email
        })
        .then((resp) => {
          localStorage.setItem("username", resp.data.email);
          commit(AUTH_SUCCESS, resp);
          resolve(resp);
        })
        .finally(() => {
          router.push({ path: `/user/info` });
        })
        .catch((err) => {
          reject(err);
        });
    });
  },
};

const mutations = {
  [AUTH_REQUEST]: (state) => {
    state.status = "loading";
  },
  [AUTH_SUCCESS]: (state, resp) => {
    state.status = "success";
    state.username = resp.data.email;
  },
  [AUTH_ERROR]: (state) => {
    state.status = "error";
  },
  [AUTH_CLEAR]: (state) => {
    state.accessToken = "";
    state.refreshToken = "";
    state.username = "";
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  getters,
  actions,
};
