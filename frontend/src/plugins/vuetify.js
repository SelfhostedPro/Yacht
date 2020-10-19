import Vue from "vue";
import Vuetify from "vuetify/lib";

Vue.use(Vuetify);

// function is_dark() {
//   if (process.env.VUE_APP_IS_DARK) {
//     return process.env.VUE_APP_IS_DARK
//   }
// }
function theme() {
  var Default = {
    theme: {
      themes: {
        dark: {
          primary: "#41b883",
          background: "#000"
        },
      },
      dark: true,
      options: { customProperties: true }
    },
  };
  var DigitalOcean = {
    theme: {
      themes: {
        light: {
          primary: "#008bcf",
          secondary: "#F3F5F9",
          background: "#FFF"
        },
      },
      light: true,
      options: { customProperties: true }
    },
  };
  if (!process.env.VUE_APP_THEME || process.env.VUE_APP_THEME == "Default") {
    return Default;
  } else if (process.env.VUE_APP_THEME == "DigitalOcean") {
    return DigitalOcean;
  }
}

export default new Vuetify(theme());
