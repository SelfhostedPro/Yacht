import axios from "axios";

const state = {
  templates: []
};

const getters = {

};

const mutations = {
  setTemplates(state, templates) {
    state.templates = templates;
  }
};

const actions = {
  loadTemplates({ commit }) {
    const url = "/api/templates/";
    axios
      .get(url)
      .then(response => {
        let templates = response.data.data;
        commit("setTemplates", templates);
      })
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  getters,
  actions
};
