<template>
    <div>
      <b-navbar toggleable="lg" type="light" class="custom-navbar">
        <b-navbar-brand href="#">{{ user.username }}</b-navbar-brand>
        

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-brand style="margin-left: 42.5%;">BookMyEvent</b-navbar-brand>
          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <b-nav-item-dropdown right>
              <!-- Using 'button-content' slot -->
              <template #button-content>
                <em>User</em>
              </template>
              <b-dropdown-item v-if="!prof || other" @click="profile">Profile</b-dropdown-item>
              <b-dropdown-item v-if="prof || other" @click="dashboard">Dashboard</b-dropdown-item>
              <b-dropdown-item @click="signOut">Sign Out</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
</template>

<script>
export default {
    name: 'NavBar',
    props: {
      user : {
        type: Object,
        required: true
      },
      prof: {
        type: Boolean,
        required: true
      },
      other: {
        type: Boolean,
        required: true
      }

       
    },
    methods: {
        signOut() {
            localStorage.removeItem('token');
            this.$router.push('/');
        },
        profile() {
            if (this.user.admin) {
                this.$router.push('/admin/profile');
            } else {
                this.$router.push('/profile');
            }
        },
        dashboard() {
            if (this.user.admin) {
                this.$router.push('/admin');
            } else {
                this.$router.push('/dashboard');
            }
        }
    },
}
</script>

<style>
.custom-navbar {
    top: 0;
    left: 0;
    right: 0;
    z-index: 999;
    backdrop-filter: blur(10px);
    box-shadow:rgb(0, 0, 0) -8px 20px 65px;
    width: 100%;
}
</style>