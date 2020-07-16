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
                  debugthis(selectedApp);
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
      </v-row>
    </v-container>
    <v-dialog
      v-model="appDetailsDialog"
      max-width="500"
      scrollable
      v-if="selectedApp"
    >
      <v-card>
        <v-img
          :src="selectedApp.logo"
          contain
          class="white--text align-end"
          gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
          aspect-ratio="1"
          height="200px"
        >
          <v-card-title class="headline" style="word-break: break-all;">
            {{ selectedApp.title }}
          </v-card-title>
        </v-img>
        <v-card-text class="pt-2">
          {{ selectedApp.description }}
        </v-card-text>
        <v-card-text v-if="selectedApp.notes">
          <b>Notes:</b> <br />
          <span v-html="selectedApp.notes" />
        </v-card-text>
        <v-divider />

        <v-card>
          <v-card-title class="subheading font-weight-bold">
            General
          </v-card-title>
          <v-divider />
          <v-list dense>
            <v-list-item>
              <v-list-item-content>Name</v-list-item-content>
              <v-list-item-content>
                {{ selectedApp.name }}
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>Image</v-list-item-content>
              <v-list-item-content>
                {{ selectedApp.image }}
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>Platform</v-list-item-content>
              <v-list-item-content>
                {{ selectedApp.platform }}
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card>
        <v-divider />
        <v-card v-if="selectedApp.ports">
          <v-card-title class="subheading font-weight-bold">
            Ports
          </v-card-title>
          <v-divider />
          <v-simple-table>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="px-5 text-left">Host Port</th>
                  <th class="px-5 text-left">Container Port/Proto</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="port in selectedApp.ports" :key="port.hport">
                  <td class="px-5 text-left">{{ port.hport }}</td>
                  <td class="px-5 text-left">
                    {{ port.cport }}/{{ port.proto }}
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card>
        <v-divider />

        <v-card v-if="selectedApp.volumes">
          <v-card-title class="subheading font-weight-bold">
            Volumes
          </v-card-title>
          <v-divider />
          <v-simple-table>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="px-5 text-left">Host</th>
                  <th class="px-5 text-left">Container</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="volume in selectedApp.volumes"
                  :key="volume.container"
                >
                  <td>{{ volume.bind }}</td>
                  <td>{{ volume.container }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card>

        <v-divider />
        <v-card v-if="selectedApp.env">
          <v-card-title class="subheading font-weight-bold">
            Env Variables
          </v-card-title>
          <v-divider />
          <v-simple-table>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="px-5 text-left">Label</th>
                  <th class="px-5 text-left">Default</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="env in selectedApp.env"
                  :key="env.label"
                >
                  <td>{{ env.label }}</td>
                  <td>{{ env.default }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card>
        <v-divider />
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="appDetailsDialog = false">
            Cancel
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            text
            color="primary"
            :to="{ name: 'Deploy', params: { appId: selectedApp.id } }"
          >
            Deploy
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
export default {
  data() {
    return {
      appDetailsDialog: false,
      selectedApp: null,
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
    debugthis(app) {
      console.log(app);
    },
  },
  created() {
    const templateId = this.$route.params.templateId;
    this.readTemplate(templateId);
    console.log(this.getTemplateById(templateId));
  },
};
</script>

<style lang="css" scoped></style>
