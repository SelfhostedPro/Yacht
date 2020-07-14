import axios from "axios";

const state = {
  templates: []
};

const mutations = {
  setTemplates(state, templates) {
    state.templates = templates;
  },
  setTemplate(state, template) {
    const idx = state.templates.findIndex(x => x.id === template.id);
    if (idx < 0) {
      state.templates.push(template);
    } else {
      state.templates.splice(idx, 1, template);
    }
  },
  addTemplate(state, template) {
    state.templates.push(template);
  },
  removeTemplate(state, template) {
    const idx = state.templates.findIndex(x => x.id === template.id);
    if (idx < 0) { return; }
    state.templates.splice(idx, 1);
  }
};

const actions = {
  readTemplates({ commit }) {
    const url = "/api/templates/";
    axios
      .get(url)
      .then(response => {
        const templates = response.data.data;
        commit("setTemplates", templates);
      });
  },
  readTemplate({ commit }, id) {
    const url = `/api/templates/${id}`;
    axios
      .get(url)
      .then(response => {
        const template = response.data.data;
        commit("setTemplate", template);
      });
  },
  writeTemplate({ commit }, payload) {
    const url = "/api/templates/";
    axios
      .post(url, payload)
      .then(response => {
        const template = response.data.data;
        commit("addTemplate", template);
      });
  },
  updateTemplate({ commit }, id) {
    const url = `/api/templates/${id}/refresh`;
    axios
      .post(url)
      .then(response => {
        const template = response.data.data;
        commit("setTemplate", template);
      })
  },
  deleteTemplate({ commit }, id) {
    const url = `/api/templates/${id}`;
    axios
      .delete(url)
      .then(response => {
        const template = response.data.data;
        commit("removeTemplate", template);
      })
  }
};

const getters = {
  getTemplateById(state) {
    return id => {
      return state.templates.find(x => x.id == id);
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
