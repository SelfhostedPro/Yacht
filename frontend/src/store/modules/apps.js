import axios from "axios";

const state = {
  apps: []
};

const mutations = {
  setApp(state, app) {
    const idx = state.apps.findIndex(x => x.id === app.id);
    if (idx < 0) {
      state.apps.push(app);
    } else {
      state.apps.splice(idx, 1, app);
    }
  }
};

const actions = {
  readApp({ commit }, id) {
    const url = `/api/apps/${id}`;
    axios.get(url).then(response => {
      const app = response.data.data;
      commit("setApp", app);
    });
  }
};

const getters = {
  getAppById(state) {
    return id => {
      console.log(state.apps);
      return state.apps.find(x => x.id == id);
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