<template>
  <div>
    <!-- big sidebar start -->
    <b-sidebar id="sidebar-big" shadow no-header-close no-close-on-esc no-close-on-route-change>
      <!-- big sidebar footer -->
      <template v-slot:footer>
        <div class="d-flex bg-dark text-light align-items-center px-3 py-2">
          <b-button squared v-b-toggle="'sidebar-big sidebar-small'">
            <b-icon-arrow-bar-left></b-icon-arrow-bar-left>
          </b-button>
        </div>
      </template>
      <!-- big sidebar header -->
      <div class="sidebar-header">
        <img alt="Vue logo" src="@/assets/logo.png" width="32" height="32" />
      </div>
      <!-- big sidebar content -->
      <div>
        <b-nav vertical>
          <!-- Apps collapse -->
          <b-button squared v-b-toggle="'collapse-apps'" class="m-1" variant="dark">
            <b-icon-box /> Apps
          </b-button>
          <b-collapse id="collapse-apps" accordion="main-menu">
            <b-button squared class="m-1" variant="light">
              <b-icon-plus /> Add App
            </b-button>
            <b-button squared class="m-1" variant="light">
              <b-icon-list-ul /> List Apps
            </b-button>
          </b-collapse>
          <!-- Templates collapse -->
          <b-button squared v-b-toggle="'collapse-templates'" class="m-1" variant="dark">
            <b-icon-card-list /> Templates
          </b-button>
          <b-collapse id="collapse-templates" accordion="main-menu">
            <b-button squared class="m-1" variant="light">
              <b-icon-plus /> Add Template
            </b-button>
            <b-button squared class="m-1" variant="light">
              <b-icon-list-ul /> List Templates
            </b-button>
          </b-collapse>
        </b-nav>
      </div>
    </b-sidebar>
    <!-- small sidebar -->
    <b-sidebar
      id="sidebar-small"
      width="5em"
      shadow
      no-header-close
      no-close-on-esc
      no-close-on-route-change
      visible
    >
      <!-- small sidebar footer -->
      <template v-slot:footer>
        <div class="d-flex bg-dark text-light align-items-center px-3 py-2">
          <b-button squared v-b-toggle="'sidebar-big sidebar-small'">
            <b-icon-arrow-bar-right></b-icon-arrow-bar-right>
          </b-button>
        </div>
      </template>
      <!-- small sidebar header -->
      <div class="sidebar-header">
        <img alt="Vue logo" src="@/assets/logo.png" width="32" height="32" />
      </div>
      <!-- small sidebar content -->
      <div>
        <b-nav vertical>
          <!-- Apps collapse -->
          <b-button squared v-b-toggle="'collapse-apps'" class="m-1" variant="dark">
            <b-icon-box />
          </b-button>
          <b-collapse id="collapse-apps" accordion="main-menu">
            <b-button squared class="m-1" variant="light">
              <b-icon-plus />
            </b-button>
            <b-button squared class="m-1" variant="light">
              <b-icon-list-ul />
            </b-button>
          </b-collapse>
          <!-- Templates collapse -->
          <b-button squared v-b-toggle="'collapse-templates'" class="m-1" variant="dark">
            <b-icon-card-list />
          </b-button>
          <b-collapse id="collapse-templates" accordion="main-menu">
            <b-button squared class="m-1" variant="light">
              <b-icon-plus />
            </b-button>
            <b-button squared class="m-1" variant="light">
              <b-icon-list-ul />
            </b-button>
          </b-collapse>
        </b-nav>
      </div>
    </b-sidebar>
  </div>
</template>
