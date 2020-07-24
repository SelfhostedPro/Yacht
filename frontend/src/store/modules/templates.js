import axios from "axios";

const state = {
  templates: [],
  isLoading: false,
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
  },
  setApp(state, app) {
    const idx = state.apps.findIndex(x => x.id === app.id);
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
  readTemplates({ commit }) {
    commit("setLoading", true);
    const url = "/api/templates/";
    axios
      .get(url)
      .then(response => {
        const templates = response.data.data;
        commit("setTemplates", templates);
      })
      .finally(() => {
        commit("setLoading", false);
      });
  },
  readTemplate({ commit }, id) {
    commit("setLoading", true);
    const url = `/api/templates/${id}`;
    axios
      .get(url)
      .then(response => {
        const template = response.data.data;
        commit("setTemplate", template);
      })
      .finally(() => {
        commit("setLoading", false);
      });
  },
  writeTemplate({ commit }, payload) {
    commit("setLoading", true);
    const url = "/api/templates/";
    axios
      .post(url, payload)
      .then(response => {
        const template = response.data.data;
        commit("addTemplate", template);
      })
      .finally(() => {
        commit("setLoading", false);
      });
  },
  updateTemplate({ commit }, id) {
    commit("setLoading", true);
    const url = `/api/templates/${id}/refresh`;
    axios
      .post(url)
      .then(response => {
        const template = response.data.data;
        commit("setTemplate", template);
      })
      .finally(() => {
        commit("setLoading", false);
      });
  },
  deleteTemplate({ commit }, id) {
    commit("setLoading", true);
    const url = `/api/templates/${id}`;
    axios
      .delete(url)
      .then(response => {
        const template = response.data.data;
        commit("removeTemplate", template);
      })
      .finally(() => {
        commit("setLoading", false);
      });
  },
  readApp({ commit }, id) {
    commit("setLoading", true);
    const url = `/api/apps/${id}`;
    axios.get(url).then(response => {
      const app = response.data.data;
      commit("setApp", app);
    })
    .finally(() => {
      commit("setLoading", false);
    });
  },
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
