<template>
    <div>
    <div v-if="!dataLoading" :class="{ 'blur-content': showModal }">
        <NavComponent :title=this.user.username :user="user" :prof="false"/>
         <!-- create a search bar input bootstrap form -->
        <div class="d-flex mt-2">
            <b-form class="mx-auto" style="width: 50%;" @submit.prevent="search">
                    <b-form-input
                        @input="search"
                        id="input-1"
                        v-model="searchTerm"
                        style="background-color: transparent; backdrop-filter: blur(5px); color: white;"
                        type="search"
                        required
                        placeholder="Enter search term"
                        class="placeholder-white"
                    ></b-form-input>
            </b-form>
        </div>
        <div v-if="!dataLoading" class="flex-row d-flex justify-content-around mb-5">
            <div style="max-width: 550px; height: 309px;" v-for="venue in venues" :key=venue.id
                class="col-md-6 mt-3 rounded p-0 venue">
                <div class="row">
                    <div class="col-md-3 pl-5 p-1 my-auto"><b-button class="but" pill variant="dark" @click="exportvenue(venue)"><img style="height: 20px; width: 20px;" src="../assets/expand-arrows.png" alt=""></b-button></div>
                    <div class="col-md-6 pt-1 my-auto">
                        <h2 style="color: #F3797E;">{{ venue.name }}</h2>
                    </div>
                    <div class="col-md-3 pr-5 p-1 my-auto"><b-button class="but" pill variant="dark" @click="venueview(venue)"><img style="height: 20px; width: 20px;" src="../assets/icons8-info-30.png" alt=""></b-button></div>
                </div>
                <VenueComponent :venue="venue" :user="user" :searchTerm="searchTerm" @event-changed="getvenues" @modal-show="modalshow" @modal-hide="modalhide" />
            </div>
        </div>
        <b-modal @hide="showModal = false" id="export-venue" title="Export Venue" >
                <ExportPage :venue="selectedvenue"/>
        </b-modal>
    </div>
    <div v-else class="d-flex justify-content-center">
                <b-spinner label="Spinning" variant="primary"></b-spinner>
    </div>
    </div>
</template>

<script>
import NavComponent from '@/components/NavComponent.vue';
import VenueComponent from '@/components/VenueComponent.vue';
import ExportPage from '@/components/ExportPage.vue';
import axios from 'axios';
import { mapGetters } from 'vuex'
import { mapActions } from 'vuex'

export default {
    name: 'AdminDashboard',
    components: {
        NavComponent,
        VenueComponent,
        ExportPage
    },

    data() {
        return {
            venues: [],
            showModal: false,
            user: {},
            dataLoading: true,
            file: null,
            searchTerm: '',
            bgColor: '#778899',
            position: 'bottom-right',

        }
    },
    methods: {
        ...mapActions({
            setvenue: 'SET_VENUE_ACTION'
        }),
        getImageSrc(imageData) {
            return `data:image/png;base64,${imageData}`
        },
        onFileChange(event) {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = (e) => {
                this.file = e.target.result;
            };
            reader.readAsDataURL(file);
        },
        exportvenue(venue) {
            console.log('Exported');
            this.selectedvenue = venue;
            this.$bvModal.show('export-venue');
            this.showModal = true;
        },
        async getvenues() {
            this.dataLoading = true;
            await axios.get('http://127.0.0.1:5000/venues',
                {
                    headers: { 'x-access-token': this.token }
                }
            ).then((response) => {
                this.venues = response.data.venues;
                this.dataLoading = false;
            })
                // if admin call admin dashboard
                // else call user dashboard
                .catch((error) => {
                    console.log(error);
                });
        },
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

        modalshow() {
            this.showModal = true;
        },
        modalhide() {
            this.showModal = false;
        },

        search(val) {
            console.log(val);
            this.searchTerm = val;
            if (this.searchTerm === '') {
                this.getvenues();
            }
            this.venues = this.venues.filter((venue) => {
                return venue.name.toLowerCase().includes(this.searchTerm.toLowerCase());
            });
        },

        venueview(venue) {
            this.setvenue(venue.id)
            this.$router.push('/venue');
        },
        

    },

    async mounted() {
        this.dataLoading = true;
        if (localStorage.getItem('token') === null) {
            this.$router.push('/');
        }
        await this.getvenues();
        await this.getuser();
        this.dataLoading = false;

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
.venue{
    box-shadow:rgb(0, 0, 0) 22px 24px 65px;
    backdrop-filter: blur(7px);
}

.but {
    background: #838181;
    box-shadow: inset 17px 17px 35px #555454,
        inset -17px -17px 35px #b1aeae;
}

.blur-content {
    filter: blur(5px);
}

.placeholder-white::placeholder {
  color: white;
}
</style>
