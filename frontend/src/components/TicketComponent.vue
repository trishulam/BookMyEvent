<template>
    <div>
    <b-card class="m-1 " style="background-color: transparent ; backdrop-filter: blur(10px); color: #FCF5E5;  box-shadow:rgb(0, 0, 0) 22px 24px 65px;" :title="event.name" :img-src="getImageSrc(this.event.image)" img-alt="Image" img-left img-class="image">
        <b-card-text class="mt-5">
            <b-row>
                <b-col cols="6">
                    <b-card-text>
                        <b>Date:</b> <br> {{event.date}}
                    </b-card-text>
                </b-col>
                <b-col cols="6">
                    <b-card-text>
                        <b>Time:</b> <br> {{event.time}}
                    </b-card-text>
                </b-col>
            </b-row>
            <b-row>
                <b-col cols="6">
                    <b-card-text>
                        <b>Venue:</b> <br>{{ venue.name }}
                    </b-card-text>
                </b-col>
                <b-col cols="6">
                    <b-card-text>
                        <b>#Tickets:</b> <br> {{ticket.quantity}}
                    </b-card-text>
                </b-col>
            </b-row>
        </b-card-text>
        <div class="action row d-flex mt-5">
            <b-button @click="rateview" pill class="ml-2 shad"><img style="width: 20px; height: 20px;" src="../assets/rating.png" alt=""></b-button>
            <b-button @click="ticketdelete" class="ml-auto mr-1 shad" pill><img style="width:20px; height:20px;" src="../assets/icons8-delete-button-90.png" alt=""></b-button>
        </div>
    </b-card>
    <!-- modal to confirm ticketdelete -->
    <b-modal id="modal-1" ok-title="Confirm" title="Confirm Ticket Delete" @ok="ticketdeleteconfirm" @cancel="hideModal">
        <p>Are you sure you want to delete this ticket?</p>
    </b-modal>
    </div>
</template>

<script>
import axios from 'axios';
export default{
    name: 'TicketComponent',
    data() {
        return {
            event: {},
            dataLoading: true,
            file: null,
            venue: {}
        }
    },
    props: {
        ticket: {
            type: Object,
            required: true
        }
    },
    methods: {
        getImageSrc(imageData) {
            return `data:image/png;base64,${imageData}`
        },
        getevent() {
            axios.get('http://127.0.0.1:5000/events/' + this.ticket.event_id
            ).then((response) => {
                this.event = response.data.event;
                this.dataLoading = false;
                this.getvenue();
            })
                .catch((error) => {
                    console.log(error);
            });
        },
        ticketdelete() {
            this.$bvModal.show('modal-1')
        },
        ticketdeleteconfirm() {
            console.log("ticketdelete")
            axios.post('http://127.0.0.1:5000/deleteticket/' + this.ticket.id
            ).then((response) => {
                console.log(response.data.message)
                this.$emit('ticketdelete')
                this.dataLoading = false;
            })
            .catch((error) => {
                console.log(error);
            });
        },
        getvenue() {
            axios.get('http://127.0.0.1:5000/venue/' + this.event.venue_id
            ).then((response) => {
                console.log(response.data.venue)
                this.venue = response.data.venue;
                this.dataLoading = false;
            })
                .catch((error) => {
                    console.log(error);
                });
        },
        rateview() {
            this.$emit('ticketrate')
        }

    },
    mounted() {
        this.getevent();
    }


}

</script>
<style scoped>
.shad{
   background: #838181;
box-shadow: inset 17px 17px 35px #555454,
            inset -17px -17px 35px #b1aeae;
}
.card-img-left{
    height: 300px;
    width: 200px;
    object-fit: cover;
}


</style>
