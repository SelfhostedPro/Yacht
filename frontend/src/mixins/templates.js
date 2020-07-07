// import Vue from "vue";
import axios from "axios";
import router from "@/router";

export default {
  data() {
    return {
      templatesData: [],
      templateData: null,
    };
  },
  methods: {
    readTemplates() {
      const url = "/api/templates/";
      axios
        .get(url)
        .then(response => {
          this.templatesData = response.data.data;
        });
    },
    readTemplate(templateId) {
      const id = templateId || this.templatData.id;
      // Number.isInteger(id)
      // if (id == null) { throw new Error('template id missing'); }
      const url = `/api/templates/${id}`;
      axios
        .get(url)
        .then(response => {
          this.templateData = response.data.data;
        });
    },
    writeTemplate(data) {
      const url = "/api/templates/";
      axios
        .post(url, data)
        .then(response => {
          this.templateData = response.data.data;
          router.push('/templates/');
        });
    },
    updateTemplate(data) {
      const id = data;
      const url = `/api/templates/${id}/refresh`;
      axios
        .get(url)
        .then(response => {
          this.templateData = response.data.data;
        });
    },
    deleteTemplate(templateId) {
      const id = templateId || this.templatData.id;
      // Number.isInteger(id)
      // if (id == null) { throw new Error('template id missing'); }
      const url = `/api/templates/${id}`;
      axios
        .delete(url)
        .then((response) => {
          this.templateData = response.data.data;
          router.push('/templates/');
        })
    }
  }

}
