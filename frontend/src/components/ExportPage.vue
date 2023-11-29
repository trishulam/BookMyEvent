<template>
    <div>
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Export Data</h5>
                <p class="card-text">Export your data in either PDF or CSV format</p>
                <div class="d-flex justify-content-between">
                    <a href="#" @click="updateFlag(1)" class="btn btn-primary">Export as PDF</a>
                    <a href="#" @click="updateFlag(0)" class="btn btn-primary">Export as CSV</a>
                </div>
            </div>
        </div>
        <div v-if="(flag === 1)" id="divToPrint" class="mt-5">
            <h4>Venue Event Details</h4>
            <div class="table-responsive">
                <table style="background-color: white;" class="table table-bordered" @click="printDocument()">

                    <thead>
                        <tr>
                            <th>Event ID</th>
                            <th>Event Name</th>
                            <th>Venue Name</th>
                            <th>Date</th>
                            <th>Time</th>
                            <th>Description</th>
                            <th>Price</th>
                            <th>Tags</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(event,index) in events" :key="index">
                            <td>{{ event.id }}</td>
                            <td>{{ event.name }}</td>
                            <td>{{ venue.name }}</td>
                            <td>{{ event.date }}</td>
                            <td>{{ event.time }}</td>
                            <td>{{ event.description }}</td>
                            <td>{{ event.price }}</td>
                            <td>{{ event.tags }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div v-if="(flag === 0)" class="mt-5 text-center">
            <h2>Export data to CSV</h2>
            <button class="btn btn-primary" @click="exportData">Download CSV file</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { excelParser } from '../excel-parser'
import pdfMake from 'pdfmake';
import pdfFonts from 'pdfmake/build/vfs_fonts';
import htmlToPdfmake from 'html-to-pdfmake';
export default {
    props: {
        venue: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            flag: -1,
            events: [],
            // likesCount: null,
            // mutableBlogDetails: this.blogDetails
        }
    },

    methods: {
        updateFlag(data) {
            this.flag = data
        },
        getevents() {
            axios.get('http://127.0.0.1:5000/venueevents/' + this.venue.id
            ).then((response) => {
                this.events = response.data.events;
            })
                .catch((error) => {
                    console.log(error);
                });

        },

        printDocument() {
            const pdfTable = document.getElementById('divToPrint');
            var html = htmlToPdfmake(pdfTable.innerHTML);

            const documentDefinition = { content: html };
            pdfMake.vfs = pdfFonts.pdfMake.vfs;
            pdfMake.createPdf(documentDefinition).open();

        },
        exportData() {
            let cevents = this.events
            for (let i = 0; i < cevents.length; i++) {
                delete cevents[i].image
            }
            excelParser().exportDataFromJSON(cevents, "exported-data", "csv");
        }
    },

    async created() {
        this.getevents()
        // await this.getLikes()

        // this.getLikeCount()
    }
}
</script>

<style></style>