import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Templates from "../views/Templates.vue";
import TemplatesShow from "../components/templates/TemplatesDetails.vue";
import TemplatesForm from "../components/templates/TemplatesForm.vue";
import TemplatesList from "../components/templates/TemplatesList.vue";
import Applications from "../views/Applications.vue";
import ApplicationsForm from "../components/applications/ApplicationsForm.vue";
import Container from "../views/Container.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/templates",
    // name: "Templates",
    component: Templates,
    children: [
      {
        path: "",
        name: "Templates",
        component: TemplatesList // perhaps rename to TemplatesIndex
      },
      {
        path: "new",
        component: TemplatesForm // perhaps rename to TemplatesCreate
      },
      {
        path: ":templateId",
        component: TemplatesShow // perhaps rename to TemplateDetails
      }
    ]
  },
  {
    path: "/apps",
    component: Applications,
    children: [
      {
        name: "Deploy",
        path: "deploy/:appId",
        component: ApplicationsForm
      }
    ]
  },
  {
    path: "/images",
    name: "Images",
    component: Container
  }
];

const router = new VueRouter({
  routes
});

export default router;
