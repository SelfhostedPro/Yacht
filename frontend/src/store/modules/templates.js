import axios from "axios";

const state = {
  loading: false,
  // better use object as set {<id>: template} to guarantee uniqueness
  templates: [],
  // workaround to prevent BUG in singleview
  currentTemplate: null
};

const getters = {
  // BUG: Can't get property of state.templates on readTemplate(ctx, id)
  getTemplateById(state) {
    return id => {
      return state.templates.find(x => x.id == id);
    };
  }
};

const mutations = {
  setLoading(state, loading) {
    state.loading = loading;
  },
  setTemplates(state, templates) {
    state.templates = templates;
  },
  setTemplate(state, template) {
    const idx = state.templates.findIndex(x => x.id === template.id);
    state.templates.splice(idx, 1, template);
  },
  addTemplate(state, template) {
    state.templates.push(template);
  },
  removeTemplate(state, template) {
    const idx = state.templates.findIndex(x => x.id === template.id);
    state.templates.splice(idx, 1);
    console.log(state.templates);
  },
  // workaround to prevent BUG in single view
  setCurrentTemplate(state, template) {
    state.currentTemplate = template;
  }
};

const actions = {
  readTemplates({ commit }) {
    commit("setLoading", true);
    const url = "/api/templates/";
    axios
      .get(url)
      .then(response => {
        let templates = response.data.data;
        commit("setTemplates", templates);
      })
      .finally(() => {
        commit("setLoading", false);
      });
  },
  readTemplate({ commit }, id) {
    const url = `/api/templates/${id}`;
    commit("setLoading", true);
    axios
      .get(url)
      .then(response => {
        let template = response.data.data;
        // workaround to prevent BUG in single view
        commit("setCurrentTemplate", template);
        // BUG: getter getTemplateById(id) result undefined
        commit("setTemplate", template);
      })
      .finally(() => {
        commit("setLoading", false);
      });
  },
  writeTemplate({ commit }, payload) {
    const url = "/api/templates/";
    commit("setLoading", true);
    axios
      .post(url, payload)
      .then(response => {
        let template = response.data.data;
        commit("addTemplate", template);
      })
      .finally(() => {
        commit("setLoading", false);
      });
  },
  updateTemplate({ commit }, id) {
    const url = `/api/templates/${id}/refresh`;
    commit("setLoading", true);
    axios
      .post(url)
      .then(response => {
        let template = response.data.data;
        commit("setTemplate", template);
      })
      .finally(() => {
        commit("setLoading", false);
      });
  },
  deleteTemplate({ commit }, id) {
    const url = `/api/templates/${id}`;
    commit("setLoading", true);
    axios
      .delete(url)
      .then(response => {
        let template = response.data.data;
        commit("removeTemplate", template);
      })
      .finally(() => {
        commit("setLoading", false);
      });
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  getters,
  actions
};
