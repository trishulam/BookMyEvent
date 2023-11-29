<template>
    <div>
        <canvas id="myChart"></canvas>
    </div>
</template>

<script>
import Chart from 'chart.js/auto';
import axios from 'axios';
export default{
    name: 'ChartComponent',
    data(){
        return{
            chart: null
        }
    },
    methods: {
        // get tags from backend as chart data
        gettags(){
            axios.get('http://127.0.0.1:5000/tags').
            then((response) => {
                let tags = response.data.tags;
                console.log(tags);
                let tag_names = [];
                let tag_counts = [];
                for (let i = 0; i < tags.length; i++){
                    tag_names.push(tags[i].name);
                    tag_counts.push(tags[i].count);
                }
                this.chart.data.labels = tag_names;
                this.chart.data.datasets[0].data = tag_counts;
                this.chart.update();
            })
                .catch((error) => {
                    console.log(error);
            });

        }
    },
    mounted(){
        this.gettags();
        this.chart = new Chart(document.getElementById('myChart'), {
            type: 'doughnut',
            data: {
                labels: [],
                datasets: [{
                    label: 'Tags',
                    data: [],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.5)',
                        'rgba(54, 162, 235, 0.5)',
                        'rgba(255, 206, 86, 0.5)',
                        'rgba(75, 192, 192, 0.5)',
                        'rgba(153, 102, 255, 0.5)',
                        'rgba(255, 159, 64, 0.5)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 0.5)',
                        'rgba(54, 162, 235, 0.5)',
                        'rgba(255, 206, 86, 0.5)',
                        'rgba(75, 192, 192, 0.5)',
                        'rgba(153, 102, 255, 0.5)',
                        'rgba(255, 159, 64, 0.5)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            color: 'white',
                            font: {
                                size: 15
                            }
                        }
                    },
                    title: {
                        display: true,
                        text: 'Events Genre Distribution',
                        color: 'white',
                        font: {
                            size: 20
                        }
                    }
                }
            }
        });
    }
}
</script>

<style scoped>

</style>