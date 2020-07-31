import axios from "axios";

const state = {
  apps: [],
  logs: [],
  processes: [],
  isLoading: false,
};

const mutations = {
  setApps(state, apps) {
    state.apps = apps;
  },
  setApp(state, app) {
    const idx = state.apps.findIndex((x) => x.Name === app.Name);
    if (idx < 0) {
      state.apps.push(app);
    } else {
      state.apps.splice(idx, 1, app);
    }
  },
  setAppProcesses(state, processes) {
    state.processes = processes
  },
  setAppLogs(state, logs) {
    state.logs = logs
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
  async readApp({ commit }, Name) {
    commit("setLoading", true);
    const url = `/api/apps/${Name}`;
    let response = await axios.get(url);
    if (response) {
      const app = response.data.data;
      commit("setLoading", false);
      commit("setApp", app);
    }
  },
  async readAppProcesses({ commit }, Name) {
    const url = `/api/apps/${Name}/processes`;
    let response = await axios.get(url);
    if (response) {
      const processes = response.data.data;
      commit("setAppProcesses", processes);
    }
  },
  async readAppLogs({commit}, Name) {
    let url = `/api/apps/${Name}/logs`;
    axios
      .get(url)
      .then((response) => {
        console.log(response);
        let logs = [];
        let _log = response.data.logs;
        let split_log = _log.split("\n");
        split_log.forEach((element) => {
          logs.push(element);
        });
        console.log(logs);
        commit("setAppLogs", logs)
      })
      .catch((err) => {
        console.log(err);
        this.logs.push(err);
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
    return (Name) => {
      Name = "/" + Name;
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
