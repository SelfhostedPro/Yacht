import Vue from "vue";
import Vuex from "vuex";
import auth from "./modules/auth";

Vue.use(Vuex);

const state = {};
const mutations = {};
const actions = {};
const modules = {
  auth
};

export default new Vuex.Store({
  state,
  mutations,
  actions,
  modules
});
