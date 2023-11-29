<template>
    <div>
        <b-carousel id="carousel-1" v-model="slide" :interval="4000" controls indicators background="#ababab"
             style="text-shadow: 1px 1px 2px #333;" @sliding-start="onSlideStart"
            @sliding-end="onSlideEnd" class="carousel">
        <div v-if="events.length != 0">
        <b-carousel-slide
            class="carousel-item"
            v-for="(event,index) in events" :key="index"
        >
            <template #img>
              <img
                class="image"
                :src="getImageSrc(event.image)"
                alt="image slot"
              >
            </template>
            <div class="event-details">
            <div class="blur-overlay"></div>
            <div class="event-content" @click="eventview(event)">
                <h2>{{ event.name }}</h2>
                <p>{{ event.description }}</p>
                <b-form-rating style="background-color: transparent; border-color: transparent; color: white;" inline v-model="event.rating" readonly show-value precision="2"></b-form-rating>
            </div>
          </div>
        </b-carousel-slide>
        </div>
        <b-carousel-slide
            v-else
        >   
            <template #img>
                  <img
                    class="image"
                    src="https://picsum.photos/1024/480/?image=54"
                    alt="image slot"
                  >
            </template>
            <h2>No Shows</h2>
        </b-carousel-slide>

        </b-carousel>
        <!-- modal to show admin event view -->
        <b-modal @hide="modalhide" ok-title="Edit" v-if="selectedevent && !user" id="event-view" :title="selectedevent.name" @ok="editview">
            <b-tabs content-class="mt-3" fill>
                <b-tab title="Event Details" active>
                    <div class="d-flex flex-column align-items-center">
                    <b-button v-if="this.ticketsavailable === 0" disabled class="mb-3 but" pill>HOUSEFUL!!!</b-button>
                    <b-button v-else disabled class="mb-3 but" pill>Available Tickets: {{ this.ticketsavailable }}</b-button>
                    <div class="row">
                    <div class="col-md-6 d-flex">
                        <h6>Date:</h6>
                        <p class="ml-2">{{ selectedevent.date }}</p>
                    </div>
                    <div class="col-md-6 d-flex">
                        <h6 class="ml-5">Time:</h6>
                        <p class="ml-2">{{ selectedevent.time }}</p>
                    </div>
                    </div>
                    <div class="row">
                    <div class="col-md-12">
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
                    <div>
                    <b-button @click="eventdelete" class="ml-auto mt-1 but" variant="danger" pill><img style="width:20px; height:20px;" src="../assets/icons8-delete-button-90.png" alt=""></b-button>
                    </div>
                    </div>
                    </div>    
                </div>
                </b-tab>
                <b-tab title="Venue Details">
                    <div class="d-flex flex-column align-items-center">
                    <div class="row">
                    <div class="col-md-12 d-flex">
                        <h6>Venue:</h6>
                        <p class="ml-2">{{ venue.name }}</p>
                    </div>
                    </div>
                    <div class="row">
                    <div class="col-md-12 d-flex">
                        <h6>Address:</h6>
                        <p class="ml-2">{{ venue.address }}</p>
                    </div>
                    </div>
                    <div class="row">
                    <div class="col-md-12 d-flex">
                        <h6>City:</h6>
                        <p class="ml-2">{{ venue.city }}</p>
                    </div>
                    </div>
                    <div class="row">
                    <div class="col-md-12 d-flex">
                        <h6>State:</h6>
                        <p class="ml-2">{{ venue.state }}</p>
                    </div>
                    </div>
                    </div>

                </b-tab>
            </b-tabs>
        </b-modal>
        <!-- modal to show event details with image and button to book tickets -->
        <b-modal class="modal" @hide="modalhide" ok-title="Book" v-if="selectedevent && user" id="event-view" :title="selectedevent.name" @ok="book">
            <div class="d-flex flex-column align-items-center">
                <b-button v-if="this.ticketsavailable===0" disabled class="mb-3 but" pill>HOUSEFUL!!!</b-button>
                <b-button v-else disabled class="mb-3 but" pill>Available Tickets: {{ this.ticketsavailable }}</b-button>
                <div class="row">
                <div class="col-md-6 d-flex">
                    <h6>Date:</h6>
                    <p class="ml-2">{{ selectedevent.date }}</p>
                </div>
                <div class="col-md-6 d-flex">
                    <h6 class="ml-5">Time:</h6>
                    <p class="ml-2">{{ selectedevent.time }}</p>
                </div>
                </div>
                <div class="row">
                <div class="col-md-12">
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

        <!-- modal to edit event -->
        <b-modal ok-title="Submit" v-if="selectedevent" id="event-edit" :title="selectedevent.name" @ok="editevent">
            <b-form>
                <b-form-group id="input-group-1" label="Event Name:" label-for="input-1">
                    <b-form-input id="input-1" v-model="selectedevent.name" type="text"
                        required></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-2" label="Date:" label-for="input-2">
                    <b-form-input id="input-2" v-model="selectedevent.date" type="date" 
                        required></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-3" label="Time:" label-for="input-3">
                    <b-form-input id="input-3" v-model="selectedevent.time" type="time"
                        required></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-4" label="Description:" label-for="input-4">
                    <b-form-textarea id="input-4" v-model="selectedevent.description" 
                        required></b-form-textarea>
                </b-form-group>
                <TagsDrop @input="tags"/>
            </b-form>
        </b-modal>
        <!-- modal to confirm tickets -->
        <b-modal ok-title="Confirm" id="book-confirm" @ok="bookconfirm">
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
import TagsDrop from './TagsDrop.vue'
import axios from 'axios'
export default {
    data() {
        return {
            slide: 0,
            sliding: null,
            selectedevent: null,
            ticketsavailable: null,
            events: [],
            genre: [],
            showprice: 0,
            tickets: 0
        }
    },
    props: ['venue', 'user'],
    components: {
        TagsDrop
    },

    methods: {
        getImageSrc(imageData) {
            return `data:image/png;base64,${imageData}`
        },
        onSlideStart() {
            this.sliding = true
        },
        onSlideEnd() {
            this.sliding = false
        },
        tags(tags) {
            this.genre = tags
            console.log(this.genre)
        },
        eventview(event) {
            this.selectedevent = event
            this.$bvModal.show('event-view') 
            this.getavailabletickets()
            this.modalshow()
        },
        editview() {
            console.log("edit event")
            this.$bvModal.hide('event-view')
            this.$bvModal.show('event-edit')
        },
        editevent() {
            console.log("event edited")
            axios.post('http://127.0.0.1:5000/updateevent',
                {
                    id: this.selectedevent.id,
                    name: this.selectedevent.name,
                    date: this.selectedevent.date,
                    time: this.selectedevent.time,
                    description: this.selectedevent.description,
                    tags: this.genre,
                    venue_id: this.selectedevent.venue_id
                }
            ).then((response) => {
                console.log(response.data);
                this.$emit('event-changed');
                this.getevents();
                this.$bvModal.hide('event-edit');
                this.modalhide();
            })
            .catch((error) => {
                console.log(error);
            });
        },
        eventdelete(){
            console.log("delete event")
            axios.post('http://127.0.0.1:5000/deleteevent',
                {
                    id: this.selectedevent.id
                }
            ).then((response) => {
                console.log(response.data);
                this.getevents();
                this.$emit('event-changed');
                this.$bvModal.hide('event-view');
            })
            .catch((error) => {
                console.log(error);
            });
        },
        getavailabletickets(){
            axios.get('http://127.0.0.1:5000/availabletickets/'+this.selectedevent.id
            ).then((response) => {
                console.log(response.data);
                this.ticketsavailable = response.data.available;
            })
            .catch((error) => {
                console.log(error);
            });


        },
        modalshow() {
            this.$emit('modal-show');
        },
        modalhide() {
            this.$emit('modal-hide');
        },

        book(){
            console.log("book event")
            if (this.ticketsavailable===0){
                alert("No tickets available")
                return
            }
            this.$bvModal.hide('event-view');
            this.$bvModal.show('book-confirm');
        },

        bookconfirm(){
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
            })
            .catch((error) => {
                console.log(error);
            });
        },

        price(){
            this.showprice=this.tickets*this.selectedevent.price;
        },

        getevents() {
            axios.get('http://127.0.0.1:5000/venueevents/'+this.venue.id,
            {
                headers: { 'x-access-token': localStorage.getItem('token')}
            }
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
        this.getevents();
    }
}
</script>

<style>
.carousel{
    height:309px;
}
.image{
    width: 100%;
    height: 309px;
    object-fit: cover;
}

.but {
    background: #838181;
    box-shadow: inset 17px 17px 35px #555454,
        inset -17px -17px 35px #b1aeae;
}

.modal-content {
    background-color: transparent;
    border: none;
    backdrop-filter: blur(40px); /* Add the blur effect */
    border-color: transparent;                        
    color: white;
    margin: 0 auto; 
}
.modal-footer{
 justify-content: center;
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
}
</style>