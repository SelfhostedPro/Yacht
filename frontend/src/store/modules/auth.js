import {
  AUTH_REQUEST,
  AUTH_ERROR,
  AUTH_SUCCESS,
  AUTH_LOGOUT,
  AUTH_REFRESH
} from "../actions/auth";
import axios from 'axios';

const state = {
  accessToken: localStorage.getItem("accessToken") || "",
  refreshToken: localStorage.getItem("refreshToken") || "",
  status: "",
  username: localStorage.getItem("username") || "",
};

const getters = {
  isAuthenticated: (state) => !!state.accessToken,
  authStatus: (state) => state.status,
  getUsername: (state) => state.username
};

const actions = {
  [AUTH_REQUEST]: ({ commit }, credentials) => {
    return new Promise((resolve, reject) => {
      commit(AUTH_REQUEST);
      const url = "/api/auth/login"
      axios
        .post(url, credentials)
        .then((resp) => {
          localStorage.setItem("accessToken", resp.data.access_token);
          localStorage.setItem("refreshToken", resp.data.refresh_token);
          localStorage.setItem("username", resp.data.username);
          axios.defaults.headers.common["Authorization"] = `Bearer ${resp.data.access_token}`;
          commit(AUTH_SUCCESS, resp);
          resolve(resp);
        })
        .catch((err) => {
          commit(AUTH_ERROR, err);
          localStorage.removeItem("accessToken");
          localStorage.removeItem("refreshToken");
          localStorage.removeItem("username");
          reject(err);
        });
    });
  },
  [AUTH_LOGOUT]: ({ commit }) => {
    return new Promise((resolve) => {
      commit(AUTH_LOGOUT);
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      localStorage.removeItem("username");
      resolve();
    });
  },
  [AUTH_REFRESH]: ({ commit }) => {
    return new Promise((resolve) => {
      commit(AUTH_REQUEST);
      const url = "/api/auth/refresh";
      const refreshToken = localStorage.getItem("refreshToken")
      const headers = { Authorization: `Bearer ${refreshToken}`};
      axios
        .post(url, {}, { headers: headers })
        .then(resp => {
          localStorage.setItem("accessToken", resp.data.access_token);
          commit(AUTH_REFRESH, resp);
          resolve(resp);
        })
        .catch((error) => {
          console.log(error)
          commit(AUTH_LOGOUT)
        })
    })
  }
};

const mutations = {
  [AUTH_REQUEST]: (state) => {
    state.status = "loading";
  },
  [AUTH_SUCCESS]: (state, resp) => {
    state.status = "success";
    state.accessToken = resp.data.access_token;
    state.refreshToken = resp.data.refresh_token;
    state.username = resp.data.username;
  },
  [AUTH_REFRESH]: (state, resp) => {
    state.accessToken = resp.data.access_token;
  },
  [AUTH_ERROR]: (state) => {
    state.status = "error";
  },
  [AUTH_LOGOUT]: (state) => {
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
