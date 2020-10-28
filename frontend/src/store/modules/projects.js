import axios from "axios";
import router from "@/router/index";

const state = {
  projects: [],
  isLoading: false
};

const mutations = {
  setProjects(state, projects) {
    state.projects = projects;
  },
  setProject(state, project) {
    const idx = state.projects.findIndex(x => x.name === project.name);
    if (idx < 0) {
      state.projects.push(project);
    } else {
      state.projects.splice(idx, 1, project);
    }
  },
  addProject(state, project) {
    state.projects.push(project);
  },
  removeProject(state, project) {
    const idx = state.projects.findIndex(x => x.name === project.name);
    if (idx < 0) {
      return;
    }
    state.projects.splice(idx, 1);
  },
  setLoading(state, loading) {
    state.isLoading = loading;
  }
};

const actions = {
  _readProjects({ commit }) {
    const url = "/api/compose/";
    commit("setLoading", true);
    return new Promise((resolve, reject) => {
      axios
        .get(url)
        .then(response => {
          const projects = response.data;
          commit("setLoading", false);
          commit("setProjects", projects);
          resolve(projects);
        })
        .finally(() => {
          commit("setLoading", false);
        })
        .catch(error => {
          commit("snackbar/setErr", error, { root: true });
          reject(error);
        });
    });
  },
  readProjects({ commit }) {
    commit("setLoading", true);
    const url = "/api/compose/";
    axios
      .get(url)
      .then(response => {
        console.log(response)
        const projects = response.data;
        commit("setProjects", projects);
      })
      .catch(err => {
        commit("snackbar/setErr", err, { root: true });
      })
      .finally(() => {
        commit("setLoading", false);
      });
  },
  readProject({ commit }, name) {
    commit("setLoading", true);
    const url = `/api/compose/${name}`;
    axios
      .get(url)
      .then(response => {
        const project = response.data;
        commit("setProject", project);
      })
      .catch(err => {
        commit("snackbar/setErr", err, { root: true });
      })
      .finally(() => {
        commit("setLoading", false);
      });
  },
  writeProject({ commit }, payload) {
    commit("setLoading", true);
    const url = "/api/compose/";
    axios
      .post(url, payload)
      .then(response => {
        const projects = response.data;
        commit("setProjects", projects);
      })
      .catch(err => {
        commit("snackbar/setErr", err, { root: true });
      })
      .finally(() => {
        commit("setLoading", false);
        router.push({ name: "Projects" });
      });
  },
  ProjectAction({ commit }, { Name, Action }) {
    commit("setLoading", true);
    const url = `/api/compose/${Name}/${Action}`;
    axios
      .get(url)
      .then((response) => {
        const projects = response.data;
        commit("setProjects", projects);
      })
      .catch((err) => {
        commit("snackbar/setErr", err, { root: true });
      })
      .finally(() => {
        commit("setLoading", false);
      });
  },
};

const getters = {
  getProjectByName(state) {
    return name => {
      return state.projects.find(x => x.name == name);
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
