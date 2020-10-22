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
            secondary: "#424242",
            background: "#000000",
            tabs: "#1E1E1E",
            foreground: "#1E1E1E"
          },
          light: {
            primary: "#41b883",
            secondary: "#c4c4c4",
            background: "#FFFFFF",
            tabs: "#FFFFFF",
            foreground: "#FFFFFF"
          }
        },
        dark: true,
        options: {
          customProperties: true,
        }
      },
    },
    DigitalOcean: {
      theme: {
        dark: false,
        themes: {
          light: {
            primary: "#008bcf",
            secondary: "#F3F5F9",
            background: "#FFFFFF",
            tabs: "#FFFFFF",
            foreground: "#FFFFFF"
          },
          dark: {
            primary: "#008bcf",
            secondary: "#424242",
            background: "#000000",
            tabs: "#1E1E1E",
            foreground: "#1E1E1E"
          }
        },
        options: {
          customProperties: true,
        }
      },
    },
  }
  return presetThemes[process.env.VUE_APP_THEME || 'Default']
}

export default new Vuetify(theme());
