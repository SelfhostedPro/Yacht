import Vue from "vue";
import VueRouter from "vue-router";
// import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Dashboard from "../views/Dashboard.vue";
import store from "@/store";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    // perhaps use same view different components (Login, Dashboard) if isAuthenticated
    component: Login,  // Home
    beforeEnter: (to, from, next) => {
      if (store.getters["auth/isAuthenticated"]) {
        // if is authenticated then redirect to dashboard
        return next("dashboard")
      }
      next();
    }
  },
  // {
  //   path: "/about",
  //   name: "About",
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import("../views/About.vue")
  // },
  // {
  //   path: "/login",
  //   name: "Login",
  //   component: () => import("../views/Login.vue")
  // },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
    meta: {
      requiresAuth: true
    },
    // nested routes for (example: /sample/apps)
    children: []
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
    !store.getters["auth/isAuthenticated"] &&
    to.matched.some(record => record.meta.requiresAuth)
  ) {
    return next("/");
  }
  next();
});

export default router;