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
            background: "#000000"
          },
          light: {
            primary: "#41b883",
            secondary: "#c4c4c4",
            background: "#FFFFFF"
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
        themes: {
          light: {
            primary: "#008bcf",
            secondary: "#F3F5F9",
            background: "#FFFFFF"
          },
          dark: {
            primary: "#008bcf",
            secondary: "#424242",
            background: "#000000"
          }
        },
        dark: false,
        options: {
          customProperties: true,
        }
      },
    },
  }
  console.log(presetThemes)
  console.log(process)
  return presetThemes[process.env.VUE_APP_THEME || 'Default']
}

export default new Vuetify(theme());
