<template>
  <div>
    <v-card>
      <v-card-title>
        Color Settings
      </v-card-title>
      <v-card-text>
        <v-btn-toggle v-model="color_toggle">
          <v-btn :color="$vuetify.theme.themes[theme].primary" class="secondary--text">Primary</v-btn>
          <v-btn :color="$vuetify.theme.themes[theme].secondary" class="primary--text">Secondary</v-btn>
          <v-btn :color="$vuetify.theme.themes[theme].background" class="primary--text">Background</v-btn>
        </v-btn-toggle>
        <v-color-picker v-if="color_toggle !== undefined" v-model="picker" class="mt-2 ml-2" mode="hexa" :value="picker"/>
      </v-card-text>
    </v-card>
    <v-card>
      <v-card-title>
        Logo Settings
      </v-card-title>
      <v-card-text>
        <v-switch
          v-model="$vuetify.theme.dark"
          :label="`Dark Theme: ${$vuetify.theme.dark.toString()}`"
        />
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      color_toggle: 0,
    };
  },
  computed: {
    theme() {
      return this.$vuetify.theme.dark ? "dark" : "light";
    },
    picker: {
        get() {
            if (this.color_toggle == 0) {return this.$vuetify.theme.themes[this.theme].primary}
            else if (this.color_toggle == 1) {return this.$vuetify.theme.themes[this.theme].secondary}
            else if (this.color_toggle == 2) {return this.$vuetify.theme.themes[this.theme].background}
            else return null
        },
        set(v) {
            console.log('v= ' + v)
            console.log(this.$vuetify.theme.themes[this.theme])
            console.log('theme_color= ' + this.$vuetify.theme.themes[this.theme].primary)
            if (this.color_toggle == 0) {this.$vuetify.theme.themes[this.theme].primary = v}
            else if (this.color_toggle == 1) {this.$vuetify.theme.themes[this.theme].secondary = v }
            else if (this.color_toggle == 2) {this.$vuetify.theme.themes[this.theme].background = v}
            else return null
        }
    },
    setColor() {
        this.$vuetify.theme.themes[this.theme][this.picker] == this.color
        return this.color
    }
  },
  methods: {
    backgroundColor(dark) {
      console.log(dark);
    },
  },
};
</script>

<style></style>
