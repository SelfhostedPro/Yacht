import axios from "axios";

const state = {
  accessToken: "",
  refreshToken: "",
  refreshTimeout: null
};

const mutations = {
  loggedIn(state, tokens) {
    state.accessToken = tokens.accessToken;
    state.refreshToken = tokens.refreshToken;
    // update token periodically, optional reduce requests
    // better use setTimeout to prevent race conditions
    state.refreshTimeout = setInterval(() => {
      this.dispatch("refresh");
    }, 1000 * 60 * 12);
    axios.defaults.headers.common[
      "Authorization"
    ] = `Bearer ${state.accessToken}`;
    // better add to the global scope or eject with the returned id
    axios.interceptors.response.use(
      response => {
        return response;
      },
      error => {
        if (error.response && error.response.status == 401) {
          this.dispatch("logout");
        }
        return Promise.reject(error);
      }
    );
  },
  loggedOut(state) {
    delete axios.defaults.headers.common["Authorization"];
    clearInterval(state.refreshTimeout);
    state.refreshTimeout = null;
    state.accessToken = "";
    state.refreshToken = "";
  }
};

const actions = {
  login({ commit }, credentials) {
    const url = "/api/auth/login";
    axios
      .post(url, credentials)
      .then(response => {
        commit("loggedIn", {
          accessToken: response.data.access_token,
          refreshToken: response.data.refresh_token
        });
        // resolve username
      })
      .catch(() => {
        // console.log(error.response.data.error.message, error.message);
        commit("loggedOut");
        // reject(message)
      });
  },
  logout({ commit }) {
    commit("loggedOut");
  },
  refresh({ commit, state }) {
    const url = "/api/auth/refresh";
    const headers = { Authorization: `Bearer ${state.refreshToken}` };
    axios
      .post(url, {}, { headers: headers })
      .then(response => {
        state.accessToken = response.data.access_token;
      })
      .catch(() => {
        commit("loggedOut");
      });
  }
};

const getters = {
  isLoggedIn(state) {
    return !!state.accessToken;
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  getters,
  actions
};