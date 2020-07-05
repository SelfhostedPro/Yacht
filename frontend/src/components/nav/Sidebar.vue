<template>
  <div>
    <b-sidebar id="sidebar-big" shadow no-header-close no-close-on-esc no-close-on-route-change>
      <template v-slot:footer>
        <div class="d-flex bg-dark text-light align-items-center px-3 py-2">
          <b-button squared v-b-toggle="'sidebar-big sidebar-small'">
            <b-icon-arrow-bar-left></b-icon-arrow-bar-left>
          </b-button>
        </div>
      </template>
      <div class="sidebar-header">
        <img alt="Vue logo" src="@/assets/logo.png" width="32" height="32" />
        <h3>Yacht</h3>
        <p>Container Managment UI</p>
      </div>
    </b-sidebar>
    <b-sidebar
      id="sidebar-small"
      width="5em"
      shadow
      no-header-close
      no-close-on-esc
      no-close-on-route-change
      visible
    >
      <template v-slot:footer>
        <div class="d-flex bg-dark text-light align-items-center px-3 py-2">
          <b-button squared v-b-toggle="'sidebar-big sidebar-small'">
            <b-icon-arrow-bar-right></b-icon-arrow-bar-right>
          </b-button>
        </div>
      </template>
      <div class="sidebar-header">
        <img alt="Vue logo" src="@/assets/logo.png" width="32" height="32" />
      </div>
    </b-sidebar>
  </div>
</template>
