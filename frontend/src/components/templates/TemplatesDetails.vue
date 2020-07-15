<template lang="html">
  <div class="templates-details">
    <v-container fluid v-if="template">
      <v-card>
        <v-card-title>
          {{ template.title }}
        </v-card-title>
        <v-card-subtitle>
          {{ template.url }}
        </v-card-subtitle>
      </v-card>

      <v-row dense class="mt-3">
        <v-col
          v-for="item in template.items"
          :key="item.id"
          cols="12"
          xl="2"
          md="3"
          sm="6"
          xs="12"
          class="d-flex"
          style="flex-direction:column"
        >
          <v-card class="flex-grow-1">
            <v-img
              :src="item.logo"
              contain
              class="white--text align-end"
              gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
              aspect-ratio="1"
              height="200px"
            >
              <v-card-title v-text="item.title"></v-card-title>
            </v-img>
            <v-card-text style="overflow-y: auto; height:168px">
              <!--
                Back link required!
                Perhaps display the description scrollable and add an action
                "Deploy"
                {{ item.description ? item.description : "" | truncate(200) }}
              -->
              {{ item.description ? item.description : "" | truncate(120) }}
            </v-card-text>

            <v-card-actions>
              <v-btn
                text
                @click="
                  selectedApp = item;
                  appDetailsDialog = true;
                "
              >
                View
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn
                text
                color="primary"
                :to="{ name: 'Deploy', params: { appId: item.id } }"
              >
                Deploy
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-dialog v-model="appDetailsDialog" max-width="290">
          <v-card>
            <v-card-title class="headline" style="word-break: break-all;">
              Delete the template?
            </v-card-title>
            <v-card-text>
              Are you sure you want to permanently delete the template?<br />
              This action cannot be revoked.
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text @click="appDetailsDialog = false">
                Cancel
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn
                text
                color="primary"
                :to="{ name: 'Deploy', params: { appId: item.id } }"
              >
                Deploy
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
export default {
  data() {
    return {
      appDetailsDialog: false,
    };
  },
  computed: {
    ...mapGetters({
      getTemplateById: "templates/getTemplateById",
    }),
    template() {
      const templateId = this.$route.params.templateId;
      return this.getTemplateById(templateId);
    },
  },
  methods: {
    ...mapActions({
      readTemplate: "templates/readTemplate",
    }),
  },
  created() {
    const templateId = this.$route.params.templateId;
    this.readTemplate(templateId);
    console.log(this.getTemplateById(templateId));
  },
};
</script>

<style lang="css" scoped></style>
