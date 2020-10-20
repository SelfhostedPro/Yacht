import Vue from "vue";
import Vuetify from "vuetify/lib";

Vue.use(Vuetify);

function theme() {
  var presetThemes = {
    Default: {
      theme: {
        themes: {
          dark: {
            primary: "#41b883",
            background: "#000"
          },
        },
        dark: true,
        options: {
          customProperties: true,
          themeCache: {
            get: key => localStorage.getItem(key),
            set: (key, value) => localStorage.setItem(key, value)
          }
        }
      },
    },
    DigitalOcean: {
      theme: {
        themes: {
          light: {
            primary: "#008bcf",
            secondary: "#F3F5F9",
            background: "#FFFFFF"
          },
          dark: {
            primary: "#008bcf",
            background: "#000000"
          }
        },
        light: true,
        options: {
          customProperties: true,
          themeCache: {
            get: key => localStorage.getItem(key),
            set: (key, value) => localStorage.setItem(key, value)
          }
        }
      },
    },
  }
  return presetThemes[process.env.VUE_APP_THEME || 'Default']
}

export default new Vuetify(theme());
