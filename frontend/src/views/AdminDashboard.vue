<template>
    <div :class="{ 'blur-content': showModal }">    
    <NavComponent :user="user" :prof="false" :other="false"/>
        <div v-if="!dataLoading" class="row flex-row d-flex justify-content-around mb-5">
            <div style="max-width: 550px; height: 309px;" v-for="venue in venues" :key=venue.id  class="col-md-6 mt-5 rounded p-0 venue">
                    <div class="row">
                    <div class="col-md-2 pl-5 p-1 my-auto"><b-button class="but" pill variant="danger" @click="venueDelete(venue)"><img style="height: 20px; width: 20px;" src="../assets/icons8-delete-button-90.png" alt=""></b-button></div>
                    <div class="col-md-2 pl-5 p-1 my-auto"><b-button class="but" pill variant="dark" @click="exportvenue(venue)"><img style="height: 20px; width: 20px;" src="../assets/expand-arrows.png" alt=""></b-button></div>
                    <div class="col-md-4 pt-1 my-auto"><h2 style="color: #F3797E;">{{ venue.name }}</h2></div>
                    <div class="col-md-2 pr-5 p-1 my-auto"><b-button class="but" pill variant="warning" @click="venueEdit(venue)" ><img style="height: 20px; width: 20px;" src="../assets/edit.png" alt=""></b-button></div>
                    <div class="col-md-2 pr-5 p-1 my-auto"><b-button class="but" pill variant="success" @click="addEvent(venue)"><img style="height: 20px; width: 20px;" src="../assets/plus.png" alt=""></b-button></div>
                    </div>
                    <VenueComponent :venue="venue" :user="false" @event-changed="getvenues" @modal-show="modalshow" @modal-hide="modalhide" />
            </div>
        </div>

        <fab
       :position="position"
       :bg-color="bgColor"
       :actions="fabActions"
       @venue="venue"
       @event="event"
        ></fab>
        <b-modal @hide="showModal = false" id="add-venue" title="Add Venue" @ok="onvenueSubmit">
            <b-form>
            <b-form-group
                id="input-group-1"
                label="Name:"
                label-for="input-1"
            >
                <b-form-input
                id="input-1"
                v-model="venueform.name"
                type="text"
                placeholder="Enter name"
                required
                ></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-2" label="Address:" label-for="input-2">
                <b-form-input
                id="input-2"
                v-model="venueform.address"
                placeholder="Enter address"
                required
                ></b-form-input>
            </b-form-group>
            <b-form-group id="input-group-3" label="City:" label-for="input-3">
                <b-form-input
                id="input-3"
                v-model="venueform.city"
                placeholder="Enter city"
                required
                ></b-form-input>
            </b-form-group>
            <b-form-group id="input-group-4" label="State:" label-for="input-4">
                <b-form-input
                id="input-4"
                v-model="venueform.state"
                placeholder="Enter state"
                required
                ></b-form-input>
            </b-form-group>
            <b-form-group id="input-group-5" label="Description:" label-for="input-5">
                <b-form-input
                id="input-5"
                v-model="venueform.description"
                placeholder="Enter description"
                required
                ></b-form-input>
            </b-form-group>
            <b-form-group id="input-group-6" label="Capacity:" label-for="input-6">
                <b-form-input
                id="input-6"
                type="number"
                v-model="venueform.capacity"
                placeholder="Enter capacity"
                required
                ></b-form-input>
            </b-form-group>
            <b-form-group label="Image" label-for="image-input" invalid-feedback="Image is Required">
                        <b-form-file required accept="image/*" v-model="file"
                            placeholder="Choose a file or drop it here..." drop-placeholder="Drop file here...">
                        </b-form-file>
            </b-form-group>
            </b-form>
        </b-modal>

        <b-modal @hide="showModal = false" id="edit-venue" title="Edit Venue" @ok="onvenueEditSubmit">
            <b-form>
                <b-form-group
                    id="input-group-1"
                    label="Name:"
                    label-for="input-1"
                >
                    <b-form-input
                    id="input-1"
                    v-model="selectedvenue.name"
                    type="text"
                    placeholder="Enter name"
                    required
                    ></b-form-input>
                </b-form-group>

                <b-form-group id="input-group-2" label="Address:" label-for="input-2">
                    <b-form-input
                    id="input-2"
                    v-model="selectedvenue.address"
                    placeholder="Enter address"
                    required
                    ></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-3" label="City:" label-for="input-3">
                    <b-form-input
                    id="input-3"
                    v-model="selectedvenue.city"
                    placeholder="Enter city"
                    required
                    ></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-4" label="State:" label-for="input-4">
                    <b-form-input
                    id="input-4"
                    v-model="selectedvenue.state"
                    placeholder="Enter state"
                    required
                    ></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-5" label="Description:" label-for="input-5">
                    <b-form-input
                    id="input-5"
                    v-model="selectedvenue.description"
                    placeholder="Enter description"
                    required
                    ></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-6" label="Capacity:" label-for="input-6">
                    <b-form-input
                    id="input-6"
                    type="number"
                    v-model="selectedvenue.capacity"
                    placeholder="Enter capacity"
                    required
                    ></b-form-input>
                </b-form-group>
            </b-form>
        </b-modal>


        <b-modal @hide="showModal = false" id="add-event" title="Add Event" @ok="onsubmitAddEvent">
            <b-form>
                <b-form-group
                        id="input-group-1"
                        label="Name:"
                        label-for="input-1"
                    >
                    <b-form-input
                    id="input-1"
                    v-model="eventform.name"
                    type="text"
                    placeholder="Enter name"
                    required
                        >
                    </b-form-input>
                </b-form-group>
                <b-form-group id="input-group-1" label="Event Date:" label-for="input-1">
                        <b-form-input id="input-1" v-model="eventform.date" type="date" placeholder="Enter Event Date"
                            required></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-1" label="Event Time:" label-for="input-1">
                    <b-form-input id="input-1" v-model="eventform.time" type="time" placeholder="Enter Event Time"
                        required></b-form-input>
                </b-form-group>
                <b-form-group
                        id="input-group-1"
                        label="Description:"
                        label-for="input-1"
                    >
                    <b-form-input
                    id="input-1"
                    v-model="eventform.description"
                    type="text"
                    placeholder="Enter description"
                    required
                        >
                    </b-form-input>
                <TagsDrop class="mt-3" @input="tags"/>
                </b-form-group>
                <b-form-group id="input-group-1" label="Price:" label-for="input-1">
                    <b-form-input id="input-1" v-model="eventform.price" type="number" placeholder="Enter Price"
                        required></b-form-input>
                </b-form-group>

                <b-form-group label="Image:" label-for="image-input" invalid-feedback="Image is Required">
                        <b-form-file required accept="image/*" v-model="file"
                            placeholder="Choose a file or drop it here..." drop-placeholder="Drop file here...">
                        </b-form-file>
                </b-form-group>

            </b-form>
        </b-modal>
        <!-- delete venue confirm modal -->
        <b-modal ok-title="Confirm" @hide="showModal = false" id="delete-venue" title="Delete Venue" @ok="venuedeleteconfirm">
            <p>Are you sure you want to delete this venue?</p>
            <!-- confirm button -->
        </b-modal>
        <b-modal @hide="showModal = false" id="export-venue" title="Export Venue" >
            <ExportPage :venue="selectedvenue"/>
        </b-modal>
    </div>
</template>

<script>
import NavComponent from '@/components/NavComponent.vue';
import VenueComponent from '@/components/VenueComponent.vue';
import ExportPage from '@/components/ExportPage.vue';
import TagsDrop from '@/components/TagsDrop.vue';  
import fab from 'vue-fab';
import axios from 'axios';
import { mapGetters } from 'vuex';
export default {
    name: 'AdminDashboard',
    components: {
        NavComponent,
        VenueComponent,
        TagsDrop,
        ExportPage,
        fab
    },

    data() {
        return {
            venueform: {
                name: '',
                address: '',
                city: '',
                state: '',
                description: '',
                capacity: '',
            },
            selectedvenue: '',
            eventform: {
                name: '',
                date: '',
                time: '',
                description: '',
                price: ''
            },
            venues: [],
            user: {},
            genre: [],
            showModal: false,
            dataLoading: true,
            file: null,
            bgColor: '#778899',
            position: 'bottom-right',
            fabActions: [
                {
                    name: 'venue',
                    icon: 'pin_drop'
                },
                {
                    name: 'event',
                    icon: 'event'
                }
            ]

        }
    },
    methods: {
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
        tags(tags) {
            this.genre = tags;
            console.log(this.genre);
        },
        venue() {
            console.log('Venue Added');
            this.$bvModal.show('add-venue');
            this.showModal = true;

        },
        event() {
            this.$bvModal.show('add-event');
            this.showModal = true;
        },
        exportcsv() {
            console.log('Exported');
        },
        venueEdit(venue) {
            console.log('Venue Edited');
            this.selectedvenue = venue;
            this.$bvModal.show('edit-venue');
            this.showModal = true;
        },

        addEvent(venue) {
            console.log('Event Added');
            this.selectedvenue = venue; 
            this.$bvModal.show('add-event');
            this.showModal = true;
        },

        onvenueEditSubmit(event) {
            event.preventDefault()
            console.log(this.venueform);
            axios.post('http://127.0.0.1:5000/updatevenue',
                {
                    id: this.selectedvenue.id,
                    name: this.selectedvenue.name,
                    address: this.selectedvenue.address,
                    city: this.selectedvenue.city,
                    state: this.selectedvenue.state,
                    description: this.selectedvenue.description,
                    capacity: this.selectedvenue.capacity,
                }
                ).then(() => {
                    console.log("hello");
                    this.$bvToast.toast('Venue Edited', {
                        title: 'Success',
                        variant: 'success',
                        autoHideDelay: 5000,
                        solid: true
                    })
                    this.$bvModal.hide('edit-venue');
                    this.resetvenueform();
                    this.getvenues();
                })
                    // if admin call admin dashboard
                    // else call user dashboard
                    .catch((error) => {
                        console.log(error);
            });
        },
        onvenueSubmit(event) {
            event.preventDefault()
            console.log(this.file);
            const formData = new FormData();
            formData.append('name', this.venueform.name);
            formData.append('address', this.venueform.address);
            formData.append('city', this.venueform.city);
            formData.append('state', this.venueform.state);
            formData.append('description', this.venueform.description);
            formData.append('capacity', this.venueform.capacity);
            formData.append('file', this.file);
            axios.post('http://127.0.0.1:5000/addvenue', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then(() => {
                    console.log("hello");
                    this.$bvToast.toast('Venue Added', {
                        title: 'Success',
                        variant: 'success',
                        autoHideDelay: 5000,
                        solid: true
                    })
                    this.$bvModal.hide('add-venue');
                    this.showModal = false;
                    this.resetvenueform();
                    this.getvenues();
                    })
                    // if admin call admin dashboard
                    // else call user dashboard
                .catch((error) => {
                    console.log(error);
                });
            
        },

        onsubmitAddEvent(event) {
            event.preventDefault()
            this.dataLoading = true;
            const formData = new FormData();
            formData.append('name', this.eventform.name);
            formData.append('date', this.eventform.date);
            formData.append('time', this.eventform.time);
            formData.append('description', this.eventform.description);
            formData.append('price', this.eventform.price);
            formData.append('venue_id', this.selectedvenue.id);
            formData.append('tags', this.genre);
            formData.append('file', this.file);
            axios.post('http://127.0.0.1:5000/addevent',formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
                ).then((response) => {
                    console.log(response.data);
                    this.venues = response.data.venues;
                    this.$bvModal.hide('add-event');
                    this.showModal = false;
                    this.reseteventform();
                    this.getvenues(),
                    this.dataLoading = false;
                })
                // if admin call admin dashboard
                // else call user dashboard
                .catch((error) => {
                    console.log(error);
            });

        },    

        getvenues() {
            axios.get('http://127.0.0.1:5000/venues',
                {
                     headers: { 'x-access-token': this.token }
                }
            ).then((response) => {
                console.log(response.data.venues);
                this.venues = response.data.venues;
                this.dataLoading = false;
            })
                // if admin call admin dashboard
                // else call user dashboard
            .catch((error) => {
                console.log(error);
            });
        },
        venueDelete(venue) {
            this.selectedvenue = venue;
            this.$bvModal.show('delete-venue');
            this.showModal = true;
        },
        venuedeleteconfirm() {
            console.log('Venue Deleted');
            axios.post('http://127.0.0.1:5000/deletevenue',
                {
                    "id" : this.selectedvenue.id
                }
            ).then(() => {
                console.log("deleted");
                this.getvenues();
            })
                .catch((error) => {
                    console.log(error);
            });
            this.$bvToast.toast('Venue Deleted', {
                title: 'Success',
                variant: 'success',
                autoHideDelay: 5000,
                solid: true
            })
        },

        resetvenueform() {
            this.venueform.name = '';
            this.venueform.address = '';
            this.venueform.city = '';
            this.venueform.state = '';
            this.venueform.description = '';
            this.venueform.capacity = '';
            this.file = null;
        },
        
        reseteventform() {
            this.eventform.name = '';
            this.eventform.date = '';
            this.eventform.time = '';
            this.eventform.description = '';
            this.file = null;
        },

        modalshow() {
            this.showModal = true;
        },

        modalhide() {
            this.showModal = false;
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
                this.getvenues()
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

.venue{
    box-shadow:rgb(0, 0, 0) 22px 24px 65px;
    backdrop-filter: blur(5px);
}
.but{
   background: #838181;
box-shadow: inset 17px 17px 35px #555454,
            inset -17px -17px 35px #b1aeae;
}

.blur-content{
  filter: blur(5px); 
}
</style>
