<template>
  <div>
    <!-- big sidebar start -->
    <b-sidebar id="sidebar-big" bg-variant=dark shadow no-header-close no-close-on-esc no-close-on-route-change width="12em">
      <!-- big sidebar footer -->
      <template v-slot:footer>
        <div>
          <b-nav vertical>
            <b-collapse id="collapse-settings" accordion="main-menu">
              <b-card bg-variant="light" no-body>
                <b-button block squared class="d-flex align-items-center" variant="light">
                  Info
                  <b-icon-info-circle class="ml-auto"/>
                </b-button>
                <b-button block squared class="d-flex align-items-center" variant="light">
                  Server Settings
                  <b-icon-gear-wide-connected class="ml-auto"/>
                </b-button>
                <b-button block squared class="d-flex align-items-center" variant="light">
                  Account Settings
                  <b-icon-person-circle class="ml-auto"/>
                </b-button>
              </b-card>
            </b-collapse>
            <b-button squared v-b-toggle="'collapse-settings'" class="m-1" variant="dark">
              <b-icon-gear />
              Settings
            </b-button>
            <b-button squared @click="logout" class="m-1" variant="dark">
              <b-icon-box-arrow-left />
              Log out
            </b-button>
          </b-nav>
        </div>
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
          <b-button :to="{name:'Dashboard'}" class="d-flex align-items-center" squared block variant="dark">
            Home
            <b-icon-house class="ml-auto"/>
          </b-button>
          <!-- Apps collapse -->
          <b-button squared v-b-toggle="'collapse-apps'" class="d-flex align-items-center" block variant="dark">
            Apps
            <b-icon-box class="ml-auto"/>
          </b-button>
          <b-collapse id="collapse-apps" accordion="main-menu">
            <b-card bg-variant="light" no-body>
              <b-button squared block variant="light" class="d-flex align-items-center">
                Add App
                <b-icon-plus class="ml-auto"/>
              </b-button>
              <b-button squared block variant="light" class="d-flex align-items-center">
                List Apps
                <b-icon-list-ul class="ml-auto"/>
              </b-button>
            </b-card>
          </b-collapse>
          <!-- Templates collapse -->
          <b-button squared block v-b-toggle="'collapse-templates'" class="d-flex align-items-center" variant="dark">
            Templates
            <b-icon-card-list class="ml-auto"/>
          </b-button>
          <b-collapse id="collapse-templates" accordion="main-menu">
            <b-card bg-variant="light" no-body>
              <b-button :to="{name: 'NewTemplate'}" class="d-flex align-items-center" squared block variant="light">
                Add Template
                <b-icon-plus class="ml-auto"/>
              </b-button>
              <b-button :to="{name: 'Templates'}" class="d-flex align-items-center" squared block variant="light">
                List Templates
                <b-icon-list-ul class="ml-auto"/>
              </b-button>
            </b-card>
          </b-collapse>
        </b-nav>
      </div>
    </b-sidebar>
    <!-- small sidebar -->
    <b-sidebar
      id="sidebar-small"
      width="5em"
      bg-variant=dark
      shadow
      no-header-close
      no-close-on-esc
      no-close-on-route-change
      visible
      
    >
      <!-- small sidebar footer -->
      <template v-slot:footer>
        <div>
          <b-nav vertical>
            <b-collapse id="collapse-settings" accordion="main-menu">
              <b-card bg-variant="light" no-body>
                <b-button squared class="m-1" title="Info" variant="light">
                  <b-icon-info-circle />
                </b-button>
                <b-button squared class="m-1" title="Server Settings" variant="light">
                  <b-icon-gear-wide-connected />
                </b-button>
                <b-button squared class="m-1" title="User Settings" variant="light">
                  <b-icon-person-circle />
                </b-button>
              </b-card>
            </b-collapse>
            <b-button
              squared
              v-b-toggle="'collapse-settings'"
              title="Settings"
              class="m-1"
              variant="dark"
            >
              <b-icon-gear />
            </b-button>
            <b-button squared class="m-1" @click="logout" title="Logout" variant="dark">
              <b-icon-box-arrow-left />
            </b-button>
          </b-nav>
        </div>
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
          <b-button :to="{name:'Dashboard'}" squared class="m-1" variant="dark">
            <b-icon-house />
          </b-button>
          <!-- Apps collapse -->
          <b-button squared v-b-toggle="'collapse-apps'" title="Apps" class="m-1" variant="dark">
            <b-icon-box />
          </b-button>
          <b-collapse id="collapse-apps" accordion="main-menu">
            <b-card bg-variant="light" no-body>
              <b-button squared class="m-1" title="Add App" variant="light">
                <b-icon-plus />
              </b-button>
              <b-button squared class="m-1" title="App List" variant="light">
                <b-icon-list-ul />
              </b-button>
            </b-card>
          </b-collapse>
          <!-- Templates collapse -->
          <b-button
            squared
            v-b-toggle="'collapse-templates'"
            title="Templates"
            class="m-1"
            variant="dark"
          >
            <b-icon-card-list />
          </b-button>
          <b-collapse id="collapse-templates" accordion="main-menu">
            <b-card bg-variant="light" no-body>
              <b-button :to="{name: 'NewTemplate'}" squared class="m-1" title="Add Template" variant="light">
                <b-icon-plus />
              </b-button>
              <b-button :to="{name: 'Templates'}" squared class="m-1" title="List Templates" variant="light">
                <b-icon-list-ul />
              </b-button>
            </b-card>
          </b-collapse>
        </b-nav>
      </div>
    </b-sidebar>
  </div>
</template>

<script>
export default {
  methods: {
    logout() {
      console.log("logout");
      this.$store.dispatch("auth/logout").then(() => {
        this.$router.push("/");
      });
    }
  }
};
</script>