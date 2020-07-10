import axios from "axios";

const state = {
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
  },
};

const mutations = {
  setTemplates(state, templates) {
    state.templates = templates
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
    // console.log(template)
    state.currentTemplate = template;
  }
};

const actions = {
  readTemplates({ commit }) {
    const url = "/api/templates/";
    axios.get(url).then(response => {
      let templates = response.data.data;
      commit("setTemplates", templates);
    });
  },
  readTemplate({ commit }, id) {
    const url = `/api/templates/${id}`;
    axios.get(url).then(response => {
      let template = response.data.data;
      // workaround to prevent BUG in single view
      commit("setCurrentTemplate", template);
      // BUG: getter getTemplateById(id) result undefined
      commit("setTemplate", template);
    });
  },
  writeTemplate({ commit }, payload) {
    const url = "/api/templates/";
    axios.post(url, payload).then(response => {
      let template = response.data.data;
      commit("addTemplate", template);
    });
  },
  updateTemplate(context, id) {
    const url = `/api/templates/${id}/refresh`;
    axios.get(url).then(response => {
      let template = response.data.data;
      context.commit("setTemplate", template);
    });
  },
  deleteTemplate(context, id) {
    const url = `/api/templates/${id}`;
    axios.delete(url).then(response => {
      let template = response.data.data;
      context.commit("removeTemplate", template);
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