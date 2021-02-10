<template>
  <v-card color="foreground" class="elevation-12">
    <v-toolbar color="primary" dark flat>
      <v-toolbar-title>Server Settings</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-card-text>
      This is where you can change settings related to your server.
    </v-card-text>
    <v-card color="foreground">
      <v-card-title class="subheading secondary font-weight-bold"
        >Configuration</v-card-title
      >
      <v-card-title class="font-weight-bold"> Import: </v-card-title>
      <ValidationObserver ref="obs1" v-slot="{ invalid }">
        <validationProvider
          name="importFile"
          rules="required"
          v-slot="{ errors, valid }"
        >
          <v-file-input
            v-model="importFile"
            ref="importFile"
            label="Import export.json"
            :error-messages="errors"
            :success="valid"
            required
            show-size
            accept=".json"
            class="mx-5"
          />
        </validationProvider>
        <v-btn
          class="mx-5"
          color="primary"
          :disabled="invalid"
          @click="import_settings(importFile)"
          >Import
        </v-btn>
      </ValidationObserver>
      <v-card-title class="font-weight-bold mt-5"> Export: </v-card-title>
      <v-btn class="mx-5 mb-5" color="primary" @click="export_settings()"
        >Export
      </v-btn>
    </v-card>
  </v-card>
</template>

<script>
import { ValidationObserver, ValidationProvider } from "vee-validate";
import axios from "axios";
import { mapMutations } from "vuex";
export default {
  components: {
    ValidationObserver,
    ValidationProvider
  },
  data() {
    return {
      importFile: null
    };
  },
  methods: {
    ...mapMutations({
      setSuccess: "snackbar/setSuccess",
      setErr: "snackbar/setErr"
    }),
    export_settings() {
      axios({
        url: "/api/settings/export",
        method: "GET",
        responseType: "blob"
      }).then(response => {
        var FileURL = window.URL.createObjectURL(new Blob([response.data]));
        var fileLink = document.createElement("a");

        fileLink.href = FileURL;
        fileLink.setAttribute("download", "export.json");
        document.body.appendChild(fileLink);

        fileLink.click();
      });
    },
    import_settings(importFile) {
      let formData = new FormData();
      formData.append("upload", importFile);
      let axiosHeader = {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      };
      axios
        .post("/api/settings/export", formData, axiosHeader)
        .then(response => {
          this.setSuccess(response);
        })
        .catch(err => {
          this.setErr(err);
        });
    }
  }
};
</script>
