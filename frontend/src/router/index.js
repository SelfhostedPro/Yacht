import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Templates from "../views/Templates.vue";
import TemplatesShow from "../components/templates/TemplatesDetails.vue";
import TemplatesForm from "../components/templates/TemplatesForm.vue";
import TemplatesList from "../components/templates/TemplatesList.vue";
import Applications from "../views/Applications.vue";
import AppContent from "../components/applications/ApplicationDetailsComponents/AppContent.vue";
import AppProcesses from "../components/applications/ApplicationDetailsComponents/AppProcesses.vue";
import ApplicationDetails from "../components/applications/ApplicationDetails.vue";
import ApplicationsList from "../components/applications/ApplicationsList.vue";
import ApplicationsForm from "../components/applications/ApplicationsForm.vue";
import Container from "../views/Container.vue";
import UserSettings from "../views/UserSettings.vue";
import ChangePasswordForm from "../components/userSettings/ChangePasswordForm.vue";
import UserInfo from "../components/userSettings/UserInfo.vue"

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/templates",
    // name: "Templates",
    component: Templates,
    children: [
      {
        path: "",
        name: "View Templates",
        component: TemplatesList, // perhaps rename to TemplatesIndex
      },
      {
        path: "new",
        name: "New Template",
        component: TemplatesForm, // perhaps rename to TemplatesCreate
      },
      {
        path: ":templateId",
        name: "Template Details",
        component: TemplatesShow, // perhaps rename to TemplateDetails
      },
    ],
  },
  {
    path: "/apps",
    component: Applications,
    children: [
      {
        name: "Deploy",
        path: "deploy/:appId",
        component: ApplicationsForm,
      },
      {
        name: "View Applications",
        path: "/",
        component: ApplicationsList,
      },
      {
        name: "Add Application",
        path: "deploy",
        component: ApplicationsForm,
      },
      {
        path: ":appName",
        component: ApplicationDetails,
        children: [
          {
            name: "Processes",
            path: "top",
            component: AppProcesses,
          },
          {
            name: "Info",
            path: "info",
            component: AppContent,
          },
        ],
      },
    ],
  },
  {
    path: "/user",
    component: UserSettings,
    children: [
      {
        name: "UserInfo",
        path: "info",
        component: UserInfo,
      },
      {
        name: "Chane Password",
        path: "changePassword",
        component: ChangePasswordForm,
      },
    ],
  },
  {
    path: "/images",
    name: "Images",
    component: Container,
  },
];

const router = new VueRouter({
  mode: "hash",
  base: "",
  routes,
});

export default router;
