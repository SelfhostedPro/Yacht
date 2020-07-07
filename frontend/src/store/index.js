import Vue from "vue";
import Vuex from "vuex";
import auth from "./modules/auth";
import templates from "./modules/templates";

Vue.use(Vuex);

const state = {};
const mutations = {};
const actions = {};
const modules = {
  auth,
  templates
};

export default new Vuex.Store({
  state,
  mutations,
  actions,
  modules
});