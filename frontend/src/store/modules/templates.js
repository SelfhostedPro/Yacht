import axios from "axios";

const state = {
  // better use object as set {<id>: template} to guarantee uniqueness
  templates: {},
  // workaround to prevent BUG in single view
  currentTemplate: null
};

const getters = {
  /* BUG: Can't get property of state.templates on readTemplate */
  // getTemplateById: state => id => {
  //   return state.templates[id]
  // },
  // getTemplateById(state) {
  //   return id => {
  //     return state.templates[id];
  //   }
  // },
  getTemplateById(state) {
    return function(id) {
      console.log(state.templates);
      return state.templates[id];
    }
  },
  // getTemplates: state => {
  //   return Object.values(state.templates);
  // },
  getTemplates(state) {
    return Object.values(state.templates);
  }
};

const mutations = {
  setTemplates(state, templates) {
    state.templates = templates.reduce((map, obj) => {
      map[obj.id] = obj;
      return map;
    }, {});
  },
  setTemplate(state, template) {
    state.templates[template.id] = template;
  },
  updateTemplate(state, payload) {
    state.templates[payload.id] = payload;
  },
  removeTemplate(state, template) {
    delete state.templates[template.id];
  },
  // workaround to prevent BUG in single view
  setCurrentTemplate(state, template) {
    state.currentTemplate = template;
  }
};

const actions = {
  readTemplates({ commit }) {
    const url = "/api/templates/";
    axios.get(url).then((response) => {
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
    axios.post(url, payload).then((response) => {
      let template = response.data.data;
      commit("addTemplate", template);
    });
  },
  updateTemplate(context, id) {
    const url = `/api/templates/${id}/refresh`;
    axios.get(url).then((response) => {
      let template = response.data.data;
      context.commit("updateTemplate", template);
    });
  },
  deleteTemplate(context, id) {
    const url = `/api/templates/${id}`;
    axios.delete(url).then((response) => {
      let template = response.data.data;
      context.commit("removeTemplate", template);
    });
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  getters,
  actions,
};
