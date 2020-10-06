$(document).ready(function(){

    namespace = '/test';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    
    //------------------------------------------------------------------------ 
        const aconfig={
                        
            type: 'line',
            data: {
                
                labels: [],
                datasets: [{
                    radius: 2, 
                    label: "Probe #1",
                    backgroundColor: 'rgb(145, 177, 191,0.5)',
                    borderColor: 'rgb(38, 27, 27)',
                    borderWidth: 1,
                    data: [],
                    
                    fill: false
                },{
                    radius: 2, 
                    label: "Probe #2",
                    backgroundColor: 'rgb(145, 177, 191,0.5)',
                    borderColor: 'rgb(100, 27, 27)',
                    borderWidth: 1,
                    data: [],
                    
                    fill: false
                },{
                    radius: 2, 
                    label: "Probe #3",
                    backgroundColor: 'rgb(145, 177, 191,0.5)',
                    borderColor: 'rgb(250, 27, 27)',
                    borderWidth: 1,
                    data: [],
                    
                    fill: false
                },{
                    radius: 2, 
                    label: "Probe #4",
                    backgroundColor: 'rgb(145, 177, 191,0.5)',
                    borderColor: 'rgb(38, 27, 250)',
                    borderWidth: 1,
                    data: [],
                    
                    fill: false
                }],
            },
            

            options: {
                responsive: true, 
                // maintainAspectRatio: false,
                 
                legend: {
                    display: true
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
                            labelString: 'Date/time (Timezone - GMT, -4 ET, -7 PT)'
                        }
                    }],
                    yAxes: [{
                        display: true,
                        ticks: {
                            fontSize: 10,
                            min: 0,
                            max: 15
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
                aconfig.data.datasets[0].data=results.HEIGHT1;
                aconfig.data.datasets[1].data=results.HEIGHT2;
                aconfig.data.datasets[2].data=results.HEIGHT3;
                aconfig.data.datasets[3].data=results.HEIGHT4;
                awaveChart.update();
                
            });

            }//end function			
 //------------------------------------------------------------------------ 



  //------------Transducer temperature data chart------------------------------------------------------------ 
  const TR_T_config={
                        
    type: 'line',
    data: {
        
        labels: [],
        datasets: [{
            radius: 2, 
            label: "NTC Sensor #1",
            backgroundColor: 'rgb(38, 27, 27)',
            borderColor: 'rgb(38, 27, 27)',
            data: [],
            fill: false,
            borderWidth:0.5
        },{
            radius: 2, 
            label: "NTC Sensor #2",
            backgroundColor: 'rgb(38, 27, 27)',
            borderColor: 'rgb(45, 230, 97)',
            data: [],
            fill: false,
            borderWidth:0.5
        }],
    },
    

    options: {
        responsive: true, 
        // maintainAspectRatio: false,
         
        legend: {
            display: true
        },
        title: {
            display: false,
            text: 'Temperature'
        },
        tooltips: {
            mode: 'index',
            intersect: true,
        },
        hover: {
            mode: 'nearest',
            intersect: true
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
                    labelString: 'Date/time (Timezone - GMT, -4 ET, -7 PT)'
                }
            }],
            yAxes: [{
                display: true,
                ticks: {
                    fontSize: 10,
                    min: 30,
                    max: 300
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Temperature (\u2103)'
                }}]
                }
                        
        }
        
    };


const TR_T_wavex = document.getElementById('TR_T_canvas').getContext('2d');
const TR_T_waveChart = new Chart(TR_T_wavex,TR_T_config );
Chart.defaults.global.defaultFontSize = 14;

var myChart = setInterval(TR_T_function, 1000);

function TR_T_function(){
    var getData = $.get('/historydata');
    getData.done(function(results){
        // 
        var xv=results.yvalue
        TR_T_config.data.labels=results.Date;
        TR_T_config.data.datasets[0].data=results.TRANS_TEMP1;
        TR_T_config.data.datasets[1].data=results.TRANS_TEMP2;
        TR_T_waveChart.update();
        
    });

    }//end function			
//------------------------------------------------------------------------ 

 //------------Humidity------------------------------------------------------------ 
 const H_config={
                        
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
  
        tooltips: {
            mode: 'index',
            intersect: true,
        },
        hover: {
            mode: 'nearest',
            intersect: true
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
                    labelString: 'Date/time (Timezone - GMT, -4 ET, -7 PT)'
                }
            }],
            yAxes: [{
                display: true,
                ticks: {
                    fontSize: 10,
                    min: 0,
                    max: 100
                },
                
                scaleLabel: {
                    display: true,
                    labelString: 'Humidity (%)'
                }}]
                }
                        
        }
        
    };


const H_wavex = document.getElementById('H_canvas').getContext('2d');
const H_waveChart = new Chart(H_wavex,H_config );
Chart.defaults.global.defaultFontSize = 14;

var myChart = setInterval(H_function, 1000);

function H_function(){
    var getData = $.get('/historydata');
    getData.done(function(results){
        // 
        var xv=results.yvalue
        H_config.data.labels=results.Date;
        H_config.data.datasets[0].data=results.HUMIDITY;
        H_waveChart.update();
        
    });

    }//end function			
//------------------------------------------------------------------------ 


 //------------------------------------------------------------------------ 
 const BOX_config={
                        
    type: 'line',
    data: {
        
        labels: [],
        datasets: [{
            radius: 1, 
            label: "Electronic Box",
            backgroundColor: 'rgb(145, 177, 191,0.5)',
            borderColor: 'rgb(38, 27, 27)',
            borderWidth: 1,
            data: [],
            
            fill: false
        },{
            radius: 2, 
            label: "SBC",
            backgroundColor: 'rgb(38, 27, 27)',
            borderColor: 'rgb(45, 51, 230)',
            data: [],
            fill: false,
            borderWidth:0.5
        }],
    },
    


    options: {
        responsive: true, 
        // maintainAspectRatio: false,
         
        legend: {
            display: true
        },
        title: {
            display: false,
            text: 'Temperature'
        },
        tooltips: {
            mode: 'index',
            intersect: true,
        },
        hover: {
            mode: 'nearest',
            intersect: true
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
                    labelString: 'Date/time (Timezone - GMT, -4 ET, -7 PT)'
                }
            }],
            yAxes: [{
                display: true,
                ticks: {
                    fontSize: 10,
                    min: 0,
                    // max: 9
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Temperature (\u2103)'
                }}]
                }
                        
        }
        
    };


const BOX_wavex = document.getElementById('BOX_canvas').getContext('2d');
const BOX_waveChart = new Chart(BOX_wavex,BOX_config );
Chart.defaults.global.defaultFontSize = 14;

var myChart = setInterval(BOX_function, 1000);

function BOX_function(){
    var getData = $.get('/historydata');
    getData.done(function(results){
        // 
        var xv=results.yvalue
        BOX_config.data.labels=results.Date;
        BOX_config.data.datasets[0].data=results.BOX_TEMP;
        BOX_config.data.datasets[1].data=results.SBC_TEMP;
        BOX_waveChart.update();
        
    });

    }//end function			
//------------------------------------------------------------------------ 
 

  
});

