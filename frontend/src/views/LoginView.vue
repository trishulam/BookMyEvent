<template>
    <div class="container">
        <div class="body" style="border-radius: 10px;">
            <div class="form-container d-flex" >
            <LoginComponent @toggle-event="toggle" v-if="show"/>
            <SignupComponent @toggle-event="toggle" v-else/>
            </div>
            <div>
            <img style="width: 450px; height: 100%; object-fit: cover; border-top-right-radius: 10px; border-bottom-right-radius: 10px;"  src="../assets/HD-wallpaper-speed-mix-logo-contrast-black-super-golden.jpg" alt="">
            </div>
        </div>
    </div>
</template>

<script>
import LoginComponent from '@/components/LoginComponent.vue';
import SignupComponent from '@/components/SignupComponent.vue';
import { mapActions } from 'vuex'
export default {
    name: 'LoginView',
    components: {
        LoginComponent,
        SignupComponent
    },

    data() {
        return {
            show: true
        }
    },
    methods: {
        ...mapActions({
            logout: 'LOGOUT_ACTION'
        }),
        toggle() {
            this.show = !this.show;
        }
    },
    mounted() {
        this.logout()
    }
}
</script>

<style scoped>
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
.body{
    max-width: 850px;
    display: flex;
    max-height: 600px;
     background-color: transparent;
  backdrop-filter: blur(10px);
-webkit-box-shadow: 40px 21px 45px 10px rgba(0,0,0,0.62);
-moz-box-shadow: 40px 21px 45px 10px rgba(0,0,0,0.62);
box-shadow: 40px 21px 45px 10px rgba(0,0,0,0.62);
}
.form-container {
  padding: 2%; 
  width: 400px;
 
}

</style>