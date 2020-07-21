import axios from "axios";

const state = {
  apps: [],
  isLoading: false,
};

const mutations = {
  setApps(state, apps) {
    state.apps = apps;
  },
  setApp(state, app) {
    const idx = state.apps.findIndex(x => x.Id === app.Id);
    if (idx < 0) {
      state.apps.push(app);
    } else {
      state.apps.splice(idx, 1, app);
    }
  },
  setLoading(state, loading) {
    state.isLoading = loading
  },

};

const actions = {
  readApps({ commit }) {
    commit("setLoading", true)
    const url = "/api/apps/";
    axios
      .get(url)
      .then(response => {
        const apps = response.data.data;
        commit("setApps", apps);
      })
      .finally(() => {
        commit("setLoading", false)
      });
  },
  readApp({ commit }, Name) {
    const url = `/api/apps/${Name}`;
    axios.get(url).then(response => {
      const app = response.data.data;
      commit("setApp", app);
    });
  },
  AppAction({ commit }, { Name, Action }) {
    commit("setLoading", true)
    const url = `/api/apps/${Name}/${Action}`;
    axios
      .get(url)
      .then(response => {
        const app = response.data.data;
        commit("setApps", app);
      })
      .finally(() => {
        commit("setLoading", false)
      });
  },
};

const getters = {
  getAppByName(state) {
    return name => {
      console.log(state.apps);
      return state.apps.find(x => x.name == name);
    };
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  getters,
  actions
};