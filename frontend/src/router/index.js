import Vue from "vue";
import VueRouter from "vue-router";
// import Home from "../views/Home.vue";
// import Login from "../views/Login.vue";
import Dashboard from "../views/Dashboard.vue";
import Templates from "../views/Templates.vue";
import TemplatesIndex from "../components/templates/TemplatesIndex.vue";
import TemplatesDetails from "../components/templates/TemplatesDetails.vue";
// import TemplatesCreate from "../components/templates/TemplatesCreate.vue";

import store from "@/store";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Dashboard",
    component: Dashboard,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/templates",
    // name: "Templates",
    component: Templates,
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: "",
        name: "Templates",
        component: TemplatesIndex
      },
      // {
      //   path: "new",
      //   component: TemplatesCreate,
      // },
      {
        path: ":templateId",
        component: TemplatesDetails
      }
    ]
  },
  // otherwise return home
  {
    path: "*",
    redirect: "/"
  }
];

const router = new VueRouter({
  routes
});

router.beforeEach((to, from, next) => {
  // check if username is stored in localStorage to prevent routing
  if (
    !store.getters["auth/isLoggedIn"] &&
    to.matched.some(record => record.meta.requiresAuth)
  ) {
    return next("/");
  }
  next();
});

export default router;
