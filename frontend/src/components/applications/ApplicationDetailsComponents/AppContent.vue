<template>
  <v-card raised class="flex-grow-1">
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
export default {
  props: ['app']
}
</script>
