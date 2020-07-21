<template lang="html">
  <div class="apps-list">
    <v-card>
      <v-card-title>
        Apps
        <v-fade-transition>
          <v-progress-circular class="ml-2" indeterminate v-if="isLoading" color="primary" />
        </v-fade-transition>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="apps"
        :items-per-page="10"
        :search="search"
        @click:row="handleRowClick"
      >
        <template v-slot:item.name="{ item }">
          <div class="namecell">
            <span class="nametext">{{ item.Name }}</span>
            <v-menu close-on-click close-on-content-click offset-y>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  size="small"
                  v-bind="attrs"
                  v-on="on"
                  class="float-right"
                >
                  <v-icon>mdi-chevron-down</v-icon>
                </v-btn>
              </template>
              <v-list dense>
                <v-list-item
                  @click="AppAction({ Name: item.Name, Action: 'start' })"
                >
                  <v-list-item-icon>
                    <v-icon>mdi-play</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>Start</v-list-item-title>
                </v-list-item>
                <v-list-item
                  @click="
                    AppAction({ Name: item.Name, Action: 'stop' });
                    stopping(item.State.Status);
                  "
                >
                  <v-list-item-icon>
                    <v-icon>mdi-stop</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>Stop</v-list-item-title>
                </v-list-item>
                <v-list-item @click="debug('restart ' + item.Name)">
                  <v-list-item-icon>
                    <v-icon>mdi-refresh</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>Restart</v-list-item-title>
                </v-list-item>
                <v-divider />
                <v-list-item @click="debug('kill ' + item.Name)">
                  <v-list-item-icon>
                    <v-icon>mdi-fire</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>Kill</v-list-item-title>
                </v-list-item>
                <v-list-item @click="debug('remove ' + item.Name)">
                  <v-list-item-icon>
                    <v-icon>mdi-delete</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>Remove</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </div>
        </template>
        <template v-slot:item.status="{ item }">
          <div class="statuscell">
            <span>{{ item.State.Status }} </span>
          </div>
        </template>
        <template v-slot:item.image="{ item }">
          <span>{{ item.Config.Image }}</span>
        </template>
        <template v-slot:item.created_at="{ item }">
          <span>{{ item.Created | formatDate }}</span>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
export default {
  props: {
    isLoading: { type: Boolean },
  },
  data() {
    return {
      search: "",
      headers: [
        {
          text: "Name",
          value: "name",
          sortable: true,
          align: "start",
        },
        {
          text: "Status",
          value: "status",
          sortable: true,
          width: "20%",
        },
        {
          text: "Image",
          value: "image",
          sortable: true,
          width: "20%",
        },
        {
          text: "Created At",
          value: "created_at",
          sortable: true,
          width: "20%",
        },
      ],
    };
  },
  methods: {
    ...mapActions({
      readApps: "apps/readApps",
      AppAction: "apps/AppAction",
    }),
    handleRowClick(value) {
      console.log(value);
    },
    // templateDetails(templateId) {
    //   this.$router.push({ path: `/templates/${templateId}` });
    // }
    debug(value) {
      console.log(value);
    },
  },
  computed: {
    ...mapState("apps", ["apps", "isLoading"]),
  },
  mounted() {
    this.readApps();
  },
};
</script>
