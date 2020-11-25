<template lang="html">
  <div class="template-form component">
    <v-card>
      <!-- <v-fade-transition>
        <v-progress-linear
          indeterminate
          v-if="isLoading"
          color="primary"
          bottom
        />
      </v-fade-transition> -->
      <v-form>
        <div class="d-flex">
        <v-row>
          <v-col class="flex-grow-1 flex-shrink-0">
        <v-card-title class="mt-1">
          New Compose Template
        </v-card-title>
        </v-col>
        <v-col class="flex-grow-1 flex-shrink-0">
        <v-text-field
          class="mr-3"
          v-model="form.name"
          label="Template Name"
          required
        >
        </v-text-field>
        </v-col>
        <v-col class="flex-grow-0 flex-shrink-1">
          <v-btn @click="submitCompose()" color="primary" class="mr-2 mt-3">submit</v-btn>
        </v-col>
        </v-row>
        </div>
        <editor
          v-model="form.content"
          @init="editorInit"
          lang="yaml"
          theme="twilight"
          :height="windowHeight"
          :width="windowWidth"
          class="editor"
        ></editor>
      </v-form>
    </v-card>
  </div>
</template>

<script>
// import { mapActions, mapState } from "vuex";
import axios from "axios";
export default {
  data() {
    return {
      form: {
        name: "",
        content: null,
      },
      windowHeight: window.innerHeight - 205,
      windowWidth: window.innerWidth - 80,
    };
  },
  components: {
    editor: require("vue2-ace-editor"),
  },
  methods: {
    editorInit() {
      require("brace/mode/yaml");
      require("brace/theme/twilight");
    },
    submitCompose() {
      console.log(this.form);
      let url = '/api/templates/compose/edit'
      axios
        .post(url, this.form, {})
        .then(response => {
          console.log(response)
        })
        .catch(err => {
          console.log(err)
        })
    },
  },
};
</script>

<style lang="css">
.ace_gutter {
  z-index: 1;
}
.ace_gutter-active-line {
  z-index: 1;
}
</style>