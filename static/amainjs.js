$(document).ready(function(){

    namespace = '/test';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    
    //----------------------------- 
        const aconfig={
                        
            type: 'line',
            data: {
                
                labels: [],
                datasets: [{
                    radius: 1, 
                    backgroundColor: 'rgb(145, 177, 191,0.5)',
                    borderColor: 'rgb(38, 27, 27)',
                    borderWidth: 1,
                    data: [],
                    
                    fill: true
                }],
            },
            

            options: {
                responsive: true, 
                // maintainAspectRatio: false,
                 
                legend: {
                    display: false
                },
                title: {
                    display: false,
                    text: 'Water Height Data'
                },
                plugins: {
                    datalabels: {
                        display:false,

                    },
                
                },

             
                scales: {
                    xAxes: [{
                        display: true,
                        ticks: {
                            fontSize: 10,
                            autoSkip: true,
                            maxTicksLimit:15
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Date/time (Timezone - UTC, -4 ET, -7 PT)'
                        }
                    }],
                    yAxes: [{
                        display: true,
                        ticks: {
                            fontSize: 10,
                            min: 0,
                            max: 9
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Water height (in)'
                        }}]
                        }
                                
                }
                
            };


        const awavex = document.getElementById('acanvas').getContext('2d');
        const awaveChart = new Chart(awavex,aconfig );
        Chart.defaults.global.defaultFontSize = 14;

        var myChart = setInterval(aupdateWAVE, 1000);

        function aupdateWAVE(){
            var getData = $.get('/historydata');
            getData.done(function(results){
                // 
                var xv=results.yvalue
                aconfig.data.labels=results.Date;
                aconfig.data.datasets[0].data=results.height;
                awaveChart.update();
                
            });
            // document.getElementById("demo").innerHTML = xv;

            }//end function			
 
 
 


});

