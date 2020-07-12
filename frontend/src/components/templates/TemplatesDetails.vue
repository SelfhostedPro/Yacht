<template lang="html">
  <div v-if="currentTemplate">
    <!-- <b-button type="button" @click="removeTemplate(currentTemplate.id)"
      >Delete</b-button
    > -->
    <b-card no-body border-variant="dark">
      <b-tabs
        pills
        class="text-light bg-dark"
        active-tab-class="text-light bg-primary"
        card
      >
        <b-tab title="Template Details" class="text-dark bg-light" active>
          <b-card-text>
            <h2>Template Details</h2>
            <hr />
          </b-card-text>
          <b-container>
            <b-row align-v="center" align-h="center">
              <b-col cols="1">
                <b-button-group vertical>
                  <b-button>update</b-button>
                  <b-button>delete</b-button>
                </b-button-group>
              </b-col>
              <b-col cols="7">
                <b-table
                  stacked
                  borderless
                  small
                  responsive
                  :fields="fields"
                  :items="currentTemplateTable"
                ></b-table>
              </b-col>
            </b-row>
          </b-container>
        </b-tab>
        <b-tab title="Tab 2" class="text-dark bg-light">
          <b-card-text v-if="contents">
            <h2>Template Contents</h2>
            <hr />
          </b-card-text>
          <b-container fluid>
            <b-row cols="1">
              <b-col
                v-for="app in currentTemplate.items"
                :key="app.id"
                col
                no-gutters
                class="mb-2"
              >
                <b-media>
                  <template v-slot:aside>
                    <img :src="app.logo" width="64" alt="Media Aside" />
                  </template>

                  <h2 class="text-left">{{ app.title }}</h2>
                  <p class="text-left">{{ app.description }}</p>
                  <!-- b-[Optional: add media children here for nesting] -->
                </b-media>
                <hr />
              </b-col>
            </b-row>
          </b-container>
        </b-tab>
        <b-tab title="Tab 3" class="text-dark bg-light"
          ><b-card-text>Tab contents 3</b-card-text></b-tab
        >
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";
import { mapActions } from "vuex";
import { mapState } from "vuex";
export default {
  data() {
    return {
      fields: [
        {
          key: "title",
          label: "Title",
          sortable: true,
        },
        {
          key: "created_at",
          sortable: true,
          formatter: "formarDate",
          thClass: "w-25",
        },
        {
          key: "updated_at",
          sortable: true,
          formatter: "fmtDate",
          thClass: "w-25",
        },
        {
          key: "url",
          sortable: false,
          label: "URL",
          headerTitle: "Update Buttons",
        },
      ],
      contents: [],
    };
  },
  computed: {
    ...mapState("templates", ["currentTemplate"]),
    ...mapGetters({
      getTemplateById: "templates/getTemplateById",
    }),
    // currently unused, see currentTemplate
    template() {
      const templateId = this.$route.params.templateId;
      return this.getTemplateById(templateId);
    },
    currentTemplateTable() {
      const templateId = this.$route.params.templateId;
      let items = [];
      let item = this.getTemplateById(templateId);
      items.push(item);
      return items;
    },
  },
  methods: {
    ...mapActions({
      readTemplate: "templates/readTemplate",
      readTemplates: "templates/readTemplates",
      deleteTemplate: "templates/deleteTemplate",
    }),
    removeTemplate(id) {
      // console.log(id);
      this.deleteTemplate(id);
      this.$router.push("/templates/");
    },
    templateContent(id) {
      const url = `/api/templates/${id}/contents`;
      axios
        .get(url)
        .then((response) => {
          this.contents = response.data.data;
          console.log(this.contents);
        })
        .catch((err) => console.log(err));
    },
  },
  mounted() {
    // BUG:
    const templateId = this.$route.params.templateId;
    this.readTemplate(templateId);
    // NO BUG:
    // this.readTemplates();
    this.templateContent(templateId);
  },
  beforeRouterUpdates(to, from, next) {
    // BUG:
    const templateId = this.$route.params.templateId;
    this.readTemplate(templateId);

    // NO BUG:
    // this.readTemplates();
    next();
  },
};
</script>

<style lang="css" scoped></style>
