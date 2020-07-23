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
    console.log("-------From setApp: --------")
    console.log("app=")
    console.log(app)
    console.log("~~~Find~~~")
    console.log("result of find=")
    console.log(state.apps.findIndex((x) => x.Name === app.Name))
    const idx = state.apps.findIndex((x) => x.Name === app.Name);
    if (idx < 0) {
      state.apps.push(app);
    } else {
      state.apps.splice(idx, 1, app);
    }
  },
  setLoading(state, loading) {
    state.isLoading = loading;
  },
};

const actions = {
  readApps({ commit }) {
    commit("setLoading", true);
    const url = "/api/apps/";
    axios
      .get(url)
      .then((response) => {
        const apps = response.data.data;
        commit("setApps", apps);
      })
      .finally(() => {
        commit("setLoading", false);
      });
  },
  readApp({ commit }, Name) {
    commit("setLoading", true);
    const url = `/api/apps/${Name}`;
    axios
      .get(url)
      .then((response) => {
        const app = response.data.data;
        console.log("------From readApp:---- ")
        console.log("app=")
        console.log(app)
        commit("setApp", app);
      })
      .finally(() => {
        commit("setLoading", false);
      });
  },
  AppAction({ commit }, { Name, Action }) {
    commit("setLoading", true);
    const url = `/api/apps/${Name}/${Action}`;
    axios
      .get(url)
      .then((response) => {
        const app = response.data.data;
        commit("setApps", app);
      })
      .finally(() => {
        commit("setLoading", false);
      });
  },
};

const getters = {
  getAppByName(state) {
    console.log("--- From getAppByName: ---")
    console.log("state=")
    console.log(state)
    return (Name) => {
      console.log("~~~Return~~~")
      console.log("state.apps =")
      console.log(state.apps);
      console.log("~~~Return - find: ~~~")
      console.log("result of find=")
      console.log(state.apps.find(x => x.Name == Name))
      console.log(state.apps.find((x) => x.Name == Name))
      return state.apps.find((x) => x.Name == Name);
    };
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  getters,
  actions,
};
