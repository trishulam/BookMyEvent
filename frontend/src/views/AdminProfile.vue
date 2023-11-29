<template>
    <div>
    <NavComponent :user="user" :prof="true"/>
    <div class="d-flex">
        <ChartComponent class="mt-5 mx-auto chart p-5"  style="width: 500px; height: 500px; color:white; backdrop-filter: blur(20px); border-radius: 20px;"/>
    </div>
    </div>
</template>

<script>
import NavComponent from '@/components/NavComponent.vue';   
import ChartComponent from '@/components/ChartComponent.vue';
import axios from 'axios';
import { mapGetters } from 'vuex';
export default {
    name: 'AdminProfile',
    components: {
        NavComponent,
        ChartComponent
    },

    data() {
        return {
            user: {}
        }
    },
    methods: {
        async getuser() {
            this.dataLoading = true;
            await axios.get('http://127.0.0.1:5000/users/' + this.user_id,
            {
                headers: { 'x-access-token': this.token }
            }
            ).then((response) => {
                this.user = response.data.user;
                this.dataLoading = false;
            })
                .catch((error) => {
                    console.log(error);
                });
        },
    },

    mounted() {
        if (this.token === null) {
            this.$router.push('/');
        }
        else {
            if (localStorage.getItem('admin') === 'false') {
                this.$router.push('/');
            }
        }
        this.getuser();

    },

    computed: {
        ...mapGetters({
            user_id: 'USER_ID',
            token: 'TOKEN'
        })
    }

}
</script>

<style scoped>
.chart{
    box-shadow:rgb(0, 0, 0) 22px 24px 65px;

}
</style>