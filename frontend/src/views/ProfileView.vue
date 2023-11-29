<template>
    <div>
        <NavComponent :user="user" :prof="true" />
    <div v-if="!dataLoading" class="row flex-row d-flex justify-content-around">
        <div class="col-md-4 mt-4" v-for="(ticket, index) in tickets" :key=index >
            <TicketComponent :ticket="ticket" @ticketdelete="gettickets" @ticketrate="rateview(ticket)"/>
        </div>
        <!-- check if no tickets -->
        <div v-if="tickets.length == 0" class="d-flex justify-content-center">
            <h3 style="color: white; margin-top: 50%;">No tickets Booked!!!</h3>
        </div>
    </div>
    <div v-else class="d-flex justify-content-center">
        <b-spinner class="m-5" label="Spinning" variant="primary"></b-spinner>
    </div>
    <!-- modal to rate ticket -->
    <div>
        <b-modal id="rate" title="Rate Movie" hide-footer>
            <div class="d-block text-center">
                <b-form>
                    <!-- range slider to get rating input indicating rating -->
                    <b-form-rating v-model="value"></b-form-rating>
                    <b-form-group id="textarea-group" class="mt-2" label-for="textarea">
                        <b-form-textarea
                            id="textarea"
                            v-model="comment"
                            placeholder="Enter your comment here..."
                            rows="3"
                            max-rows="6"
                        ></b-form-textarea>
                    </b-form-group>
                    <b-button class="mt-2" @click="onSubmit" variant="success">Submit</b-button>
                </b-form>
            </div>
        </b-modal>
    </div>
    </div>
</template>
<script>
import NavComponent from '@/components/NavComponent.vue';
import TicketComponent from '@/components/TicketComponent.vue';
import axios from 'axios';
import { mapGetters } from 'vuex'

export default {
    name: 'UserProfile',
    components: {
        NavComponent,
        TicketComponent
    },

    data() {
        return {
            showModal: false,
            user: {},
            tickets: [],
            ticket: null,
            value: null,
            comment: null,
            dataLoading: true,
            file: null
        }
    },
    methods: {
        onSubmit() {
            console.log('rating')
            axios.post('http://127.0.0.1:5000/addrating',
                {
                    user_id:this.user.id,
                    event_id:this.ticket.event_id,
                    rating:this.value
                }
            ).then((response) => {
                console.log(response.data)
                this.$bvModal.hide('rate')
            })
            .catch((error) => {
                    console.log(error);
            });

        },
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
        async getuser() {
            await axios.get('http://127.0.0.1:5000/users/' + this.user_id,
            {
                headers: { 'x-access-token': localStorage.getItem('token') }
            }
            ).then((response) => {
                this.user = response.data.user;
                this.dataLoading = false;
            })
            .catch((error) => {
                console.log(error);
            });
        
        },
        async gettickets() {
            await axios.get('http://127.0.0.1:5000/mytickets/' + this.user_id
            ).then((response) => {
                this.tickets = response.data.tickets;
                this.dataLoading = false;
            })
                .catch((error) => {
                    console.log(error);
            });
        },

        rateview(ticket) {
            this.$bvModal.show('rate')
            this.ticket = ticket;
        },

    },

    async mounted() {
        console.log("mounted")
        this.dataLoading=true;
        if (localStorage.getItem('token') === null) {
            this.$router.push('/');
        }
        await this.gettickets();
        await this.getuser();
        this.dataLoading=false;

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

</style>
