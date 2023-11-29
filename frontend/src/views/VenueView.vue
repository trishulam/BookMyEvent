<template>
    <div>
        <div :class="{ 'blur-content': showModal }">
        <NavComponent :user="user" :other="true" :prof="false" />
        <div class="d-flex mt-2">
            <b-form v-if="showsearch" class="ml-auto" style="width: 50%;" @submit.prevent="search">
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
            <TagsDrop class="ml-auto" style="width: 50%;" @input="tags" v-else/>
            <!-- dropdown -->
            <b-dropdown id="ddown1" text="Sort By" class="mr-auto ml-2">
                <b-dropdown-item @click="showsearch = true">Name</b-dropdown-item>
                <b-dropdown-item @click="showsearch = false">tags</b-dropdown-item>
            </b-dropdown>
        </div>
        <b-container class="rounded mt-3 p-0 venue" style="width: 100%; height: 300px;">
            <div class="d-flex">
                <div class="col-md-8 p-0">
                <img style="width: 100%; height: 300px; object-fit: cover; border-top-right-radius: 30%; border-bottom-right-radius: 30%; border-top-left-radius: 2%; border-bottom-left-radius: 2%;" :src="getImageSrc(venue.image)" alt="">
                </div>
                <!-- display venue details -->
                <div class="col-md-3 d-flex ml-5" id="venuedetails">
                <div class="my-auto rounded details" style="flex-grow: 1; color: #FCF5E5;">
                    <h2>{{ venue.name }}</h2>
                    <p>{{ venue.description }}</p>
                    <p>Address: {{ venue.address }}</p>
                    <p>City: {{ venue.city }}</p>
                    <p>State: {{ venue.state }}</p>
                    <p>Capacity: {{ venue.capacity }}</p>
                </div>
                </div>
            </div>
        </b-container>
        <div class="flex-row d-flex justify-content-around mb-5">
            <div class="col-md-4 d-flex mt-4" v-for="(event, index) in events" :key="index">
            <b-card
                class="mx-auto d-flex details"
                overlay
                :img-src=getImageSrc(event.image)
                img-alt="Card Image"
                img-height="400px"
                text-variant="white"
                :style="{ width: '270px' }"
            >
                <b-card-body class="event-details">
                    <div @click="eventview(event)">
                    <b-card-title>{{ event.name }}</b-card-title>
                    <b-card-text>
                        {{ event.description }}
                    </b-card-text>
                    <b-form-rating style="background-color: transparent; border-color: transparent; color: white;" inline v-model="event.rating" readonly show-value precision="2"></b-form-rating>
                    </div>
                </b-card-body>
            </b-card>
            </div>
        </div>
        </div>
        <b-modal class="modalneu" @hide="showModal = false" ok-title="Book" v-if="selectedevent && user" id="event-view" :title="selectedevent.name" @ok="book">
            <div class="d-flex flex-column align-items-center">
                <b-button disabled class="mb-3 neu" pill>Available Tickets: {{ this.ticketsavailable }}</b-button>
                <div class="row">
                <div class="col-md-6 d-flex">
                    <h6>Date:</h6>
                    <p class="ml-1">{{ selectedevent.date }}</p>
                </div>
                <div class="col-md-6 d-flex">
                    <h6 class="ml-5">Time:</h6>
                    <p class="ml-2">{{ selectedevent.time }}</p>
                </div>
                </div>
                <div class="row">
                <div class="col-md-12" style="text-align: center;">
                    <h6>Description:</h6>
                    <p>{{ selectedevent.description }}</p>
                </div>
                </div>
                <div class="row">
                <div class="col-md-12 d-flex">
                    <h6>Price:</h6>
                    <p class="ml-2">₹ {{ selectedevent.price }}</p>
                </div>
                </div>
                <div class="row">
                    <div class="col-md-12 d-flex">
                    <h6 class="mt-3">Tags:</h6>
                    <b-form-tags
                    input-id="tags-pills"
                    v-model="selectedevent.tags"
                    tag-variant="primary"
                    tag-pills
                    size="lg"
                    separator=" "
                    disabled
                    disableAddButton
                    placeholder=" "
                    style="font-style: transparent; background-color: transparent; border-color: transparent;"
                    ></b-form-tags>
                    </div>
                </div>    
            </div>
        </b-modal>

        <b-modal @hide="showModal = false" ok-title="Confirm" id="book-confirm" @ok="bookconfirm">
            <b-form>
                <b-form-group id="input-group-1" label="Number of Tickets:" label-for="input-1">
                    <b-form-input @input="price" id="input-1" v-model="tickets" type="number" placeholder="Enter Number of Tickets" min="1" :max="ticketsavailable"
                        required></b-form-input>
                </b-form-group>
                <div class="row">
                <div class="col-md-12 d-flex">
                    <h6>Total Price:</h6>
                    <p class="ml-2">₹ {{ showprice }}</p>
                </div>
                </div>
            </b-form>
            <b-form>
            
            </b-form>
        </b-modal>
    </div>
</template>

<script>
import NavComponent from '@/components/NavComponent.vue';
import TagsDrop from '@/components/TagsDrop.vue';
import axios from 'axios';
import { mapGetters } from 'vuex'
export default {
    name: 'VenueView',
    components: {
        NavComponent,
        TagsDrop
    },
    data() {
        return {
            user: {},
            venue: {},
            events: [],
            genre: [],
            showsearch: true,
            selectedevent: {},
            ticketsavailable: null,
            showprice: 0,
            tickets: 0,
            searchTerm: '',
            showModal: false
        }
    },
    methods: {
        eventview(event) {
            this.selectedevent = event
            this.$bvModal.show('event-view')
            this.showModal = true
            this.getavailabletickets()
        },
        getavailabletickets() {
            axios.get('http://127.0.0.1:5000/availabletickets/' + this.selectedevent.id
            ).then((response) => {
                console.log(response.data);
                this.ticketsavailable = response.data.available;
            })
                // if admin call admin dashboard
                // else call user dashboard
                .catch((error) => {
                    console.log(error);
                });
        },
        book() {
            console.log("book event")
            this.$bvModal.hide('event-view');
            this.$bvModal.show('book-confirm');
            this.showModal = true
        },
        tags(tags) {
            this.genre = tags
            console.log(this.genre)
            this.filtertags()
        },
        filtertags() {
            if (this.genre.length === 0) {
                // If this.genre is empty, show all events without filtering
                this.getevents(); // Fetch all events again
            } else {
                this.events = this.events.filter((event) => {
                    // Check if event.tags is null or not an array
                    if (!Array.isArray(event.tags)) {
                        return false; // Skip events with no tags
                    }
                    return event.tags.some((tag) => {
                        return this.genre.includes(tag);
                    });
                });
            }
        },
        
        bookconfirm() {
            console.log("book confirmed")
            axios.post('http://127.0.0.1:5000/book',
                {
                    event_id: this.selectedevent.id,
                    user_id: this.user.id,
                    tickets: this.tickets
                }
            ).then((response) => {
                console.log(response.data);
                this.$bvModal.hide('book-confirm');
                this.showModal = false
            })
                .catch((error) => {
                    console.log(error);
                });
        },

        price() {
            this.showprice = this.tickets * this.selectedevent.price;
        },

        search(val) {
            console.log(val);
            this.searchTerm = val;
            if (this.searchTerm === '') {
                this.getevents();
            }
            this.events = this.events.filter((event) => {
                return event.name.toLowerCase().includes(this.searchTerm.toLowerCase());
            });
        },

        getImageSrc(imageData) {
            return `data:image/png;base64,${imageData}`
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
        async getvenue() {
            this.dataLoading = true;
            await axios.get('http://127.0.0.1:5000/venue/' + this.venue_id
            ).then((response) => {
                this.venue = response.data.venue;
                this.dataLoading = false;
                this.getevents();
            })
                .catch((error) => {
                    console.log(error);
            });
        },
        
        async getevents() {
            await axios.get('http://127.0.0.1:5000/venueevents/' + this.venue.id
            ).then((response) => {
                this.events = response.data.events;
                console.log(this.events);
            })
                .catch((error) => {
                    console.log(error);
                });

        }
    },
    mounted() {
        this.getuser();
        this.getvenue();
    },
    // created() {
    //     // Fetch venue details using this.venueId or perform any other operations
    //     this.venue_id = this.$route.params.id;
    // },
    // Rest of the component code
    computed: {
        ...mapGetters({
            user_id: 'USER_ID',
            venue_id: 'VENUE_ID',
            token: 'TOKEN'
        })
    }
};
</script>

<style>
.venue{
    box-shadow:rgb(0, 0, 0) 22px 24px 65px;
    backdrop-filter: blur(5px);
}

.card-img{
    object-fit: cover;
}

.event-details {
  /* Apply gradual circular gradient background and backdrop blur effect */
  background-image: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.3) 0%,
    rgba(255, 255, 255, 0.2) 25%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0.05) 75%,
    rgba(255, 255, 255, 0) 100%
  );
  backdrop-filter: blur(5px); /* Set the blur radius, adjust as needed */
  padding: 10px; /* Optional: Add padding to the element */
  border-radius: 50%; /* Optional: Add a circular border-radius to the element */
  margin-top: 230px;
}

.blur-content{
  filter: blur(5px); 
}

.placeholder-white::placeholder {
  color: white;
}

.details{
    backdrop-filter: blur(7px);
    box-shadow:rgba(0, 0, 0, 0.867) 13px 39px 88px;
}
</style>