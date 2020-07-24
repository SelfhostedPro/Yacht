<template>
  <v-card raised>
    <v-card-title class="subheading primary font-weight-bold">
      General
    </v-card-title>
    <!-- <v-card-subtitle>
              General container information
            </v-card-subtitle> -->
    <v-divider />
    <v-list class="secondary" dense>
      <v-list-item>
        <v-list-item-content
          ><v-list-title class="px-5 text-centered font-weight-bold"
            >Container Name</v-list-title
          ></v-list-item-content
        >
        <v-list-item-content>
          <v-list-title class="px-5 text-centered">
            {{ app.Name }}
          </v-list-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider />

      <v-list-item>
        <v-list-item-content
          ><v-list-title class="px-5 text-centered font-weight-bold"
            >Container ID</v-list-title
          ></v-list-item-content
        >
        <v-list-item-content>
          <v-list-title class="px-5 text-centered">
            {{ app.Id.substring(0, 10) }}
          </v-list-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider />

      <v-list-item>
        <v-list-item-content
          ><v-list-title class="px-5 text-centered font-weight-bold"
            >Container Created On</v-list-title
          ></v-list-item-content
        >
        <v-list-item-content>
          <v-list-title class="px-5 text-centered">
            {{ app.Created | formatDate }}
          </v-list-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider />

      <v-list-item>
        <v-list-item-content
          ><v-list-title class="px-5 text-centered font-weight-bold"
            >Container Status</v-list-title
          ></v-list-item-content
        >
        <v-list-item-content>
          <v-list-title class="px-5 text-centered">
            {{ app.State.Status }}
          </v-list-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
export default {
  data() {
    return {};
  },
  computed: {
    ...mapState("apps", ["apps", "isLoading"]),
    ...mapGetters({
      getAppByName: "apps/getAppByName",
    }),
    app() {
      const appName = this.$route.params.appName;
      return this.getAppByName(appName);
    },
  },
  methods: {
    ...mapActions({
      readApp: "apps/readApp",
    }),
  },
  created() {
    const appName = this.$route.params.appName;
    this.readApp(appName);
  },
  async mounted() {
    const appName = this.$route.params.appName;
    await this.readApp(appName);
  },
};
</script>
