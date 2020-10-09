<template>
  <div class="page">
    <v-card>
      <v-fade-transition>
        <v-progress-linear
          indeterminate
          v-if="isLoading"
          color="primary"
          bottom
        />
      </v-fade-transition>
      <v-card-title>
        {{ image.Id }}
      </v-card-title>
      <v-card-subtitle>
        {{ image.RepoTags[0] || image.RepoDigests[0] }}
      </v-card-subtitle>
    </v-card>
    <v-card class="mt-2">
      <v-card-title>
        Image Details
      </v-card-title>
      <v-list dense>
        <v-list-item>
          <v-list-item-content>
            Tag
          </v-list-item-content>
          <v-list-item-content>
            {{ image.RepoTags[0] }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            Architecture
          </v-list-item-content>
          <v-list-item-content>
            {{ image.Architecture }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            Platform
          </v-list-item-content>
          <v-list-item-content>
            {{ image.Os }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            Architecture
          </v-list-item-content>
          <v-list-item-content>
            {{ image.Architecture }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            Created
          </v-list-item-content>
          <v-list-item-content>
            {{ image.Created | formatDate }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            Size
          </v-list-item-content>
          <v-list-item-content>
            {{ formatBytes(image.Size) }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            VirtualSize
          </v-list-item-content>
          <v-list-item-content>
            {{ formatBytes(image.VirtualSize) }}
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card>

    <v-card class="mt-2">
      <v-card-title>
        Container Details
      </v-card-title>
      <v-list dense>
        <v-list-item>
          <v-list-item-content style="max-width:20%">
            Command
          </v-list-item-content>
          <v-list-item-content>
            {{ getCMD(image.ContainerConfig.Cmd) }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content style="max-width:20%">
            Entrypoint
          </v-list-item-content>
          <v-list-item-content>
            {{ image.ContainerConfig.Entrypoint[0] }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content style="max-width:20%">
            Ports
          </v-list-item-content>
          <v-list-item-content v-for="(port, index) in Object.keys(image.ContainerConfig.ExposedPorts)" :key="index">
            {{ port }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content style="max-width:20%">
            Labels
          </v-list-item-content>
          <v-list-item-content>
            <v-card outlined tile>
            <v-simple-table dense>
              <tbody>
                <tr v-for="(value, key, index) in image.ContainerConfig.Labels" :key="index">
                  <td style="min-width:20%;" class="align-self-center"> {{key}} </td>
                  <td class="text-truncate align-self-center" style="width:100%"> {{value}} </td>
                </tr>
              </tbody>
            </v-simple-table>
            </v-card>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content style="max-width:20%">
            ENV
          </v-list-item-content>
          <v-list-item-content>
            <v-card outlined tile>
            <v-simple-table>
              <tbody>
                <tr v-for="(key, index) in image.ContainerConfig.Env" :key="index">
                  <td style="width:100%;" class="align-self-center text-truncate"> {{key}} </td>
                </tr>
              </tbody>
            </v-simple-table>
            </v-card>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";

export default {
  data() {
    return {};
  },
  computed: {
    ...mapState("images", ["image", "images", "isLoading"]),
    ...mapGetters({
      getImageById: "images/getImageById",
    }),
    image() {
      const imageid = this.$route.params.imageid;
      return this.getImageById(imageid);
    },
  },
  methods: {
    ...mapActions({
      readImage: "images/readImage",
    }),
    formatBytes(bytes) {
      if (bytes === 0) return "0 Bytes";
      const decimals = 2;
      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

      const i = Math.floor(Math.log(bytes) / Math.log(k));

      return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
    },
    getCMD(cmd) {
      for (var entry in cmd) {
        if (cmd[entry].includes("CMD")) {
          return cmd[entry];
        }
      }
    },
  },
  created() {
    const imageid = this.$route.params.imageid;
    this.readImage(imageid);
    console.log(this.image)
  },
};
</script>

<style scoped></style>
