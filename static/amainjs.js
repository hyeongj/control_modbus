$(document).ready(function(){

    namespace = '/test';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    
    //---update-10/15--------------------------------------------------------------------- 
    
    $('form#starton').submit(function(event) {
        socket.emit('start_request');
        return false;
        });

    $('form#init').submit(function(event) {
        socket.emit('init_request');
        return false;
        });	


    $('form#gain0').submit(function(event) {
        socket.emit('gain0_request');
        return false;
        });
    $('form#gain1').submit(function(event) {
        socket.emit('gain1_request');
        return false;
        });
        

    $('form#amp0').submit(function(event) {
        socket.emit('amp0_request');
        return false;
        });
    $('form#amp1').submit(function(event) {
        socket.emit('amp1_request');
        return false;
        });
        
            

    $('form#ttime0').submit(function(event) {
        socket.emit('ttime0_request');
        return false;
        });
    $('form#ttime1').submit(function(event) {
        socket.emit('ttime1_request');
        return false;
        });	

        $('form#sinterval0').submit(function(event) {
            socket.emit('sinterval0_request');
            return false;
            });
        $('form#sinterval1').submit(function(event) {
            socket.emit('sinterval1_request');
            return false;
            });	

    $('form#sinterval10').submit(function(event) {
        socket.emit('sinterval10_request');
        return false;
        });
    $('form#sinterval1000').submit(function(event) {
        socket.emit('sinterval1000_request');
        return false;
        });	

        // =======================
    $('form#rate0').submit(function(event) {
        socket.emit('rate0_request');
        return false;
        });
    $('form#rate1').submit(function(event) {
        socket.emit('rate1_request');
        return false;
        });
    $('form#rate2').submit(function(event) {
        socket.emit('rate2_request');
        return false;
        });
    $('form#rate3').submit(function(event) {
        socket.emit('rate3_request');
        return false;
        });

        $('form#BUFFER0').submit(function(event) {
            socket.emit('BUFFER0_request');
            return false;
            });
        $('form#BUFFER1').submit(function(event) {
            socket.emit('BUFFER1_request');
            return false;
            });
        $('form#BUFFER2').submit(function(event) {
            socket.emit('BUFFER2_request');
            return false;
            });
        $('form#BUFFER3').submit(function(event) {
            socket.emit('BUFFER3_request');
            return false;
            });

    $('form#ch0').submit(function(event) {
        socket.emit('ch0_request');
        return false;
        });
    $('form#ch1').submit(function(event) {
        socket.emit('ch1_request');
        return false;
        });
    $('form#ch2').submit(function(event) {
        socket.emit('ch2_request');
        return false;
        });
    $('form#ch3').submit(function(event) {
        socket.emit('ch3_request');
        return false;
        });

        

    // ===========================================
    $('form#graph').submit(function(event) {
        socket.emit('graph_request');
        return false;
        });	
    
    $('form#graphoff').submit(function(event) {
        socket.emit('graphoff_request');
        return false;
        });	
        
    $('form#REBOOT').submit(function(event) {
        socket.emit('REBOOT_request');
        return false;
        });	
        
    $('form#matplot').submit(function(event) {
        socket.emit('matplot_request');
        return false;
        });	
    
    $('form#SQLcon').submit(function(event) {
        socket.emit('SQL_request');
        return false;
        });	
    $('form#SQLdcon').submit(function(event) {
        socket.emit('SQL_d_request');
        return false;
        });	
//    ============================
 
        
    var myVar;

    $('form#liveon').submit(function(event) {
        socket.emit('liveon_request');
        myVar=setInterval(updateWAVE, 800);
        return false;
    });

    $('form#liveoff').submit(function(event) {
        socket.emit('liveoff_request');
        clearInterval(myVar);
        return false;
    });
 
 

$('form#emit').submit(function(event) {
    // modbus connection script get the value from the input from in html
    socket.emit('my_event_request', {data: $('#emit_data').val()});
    return false;
});

 


$('form#broadcast').submit(function(event) {
    socket.emit('my broadcast event', {data: $('#broadcast_data').val()});
    return false;
});


$('form#sqlsend').submit(function(event)
{
    socket.emit('sqlsend_event_request', {data: $('#sqlsend_data').val()});
    return false;
});


$('form#send').submit(function(event)
{
    // modbus write coil script
    socket.emit('send_event_request', {data: $('#send_data').val()});
    return false;
});
    
 

socket.on('my_send_response', function(msg) {
    $('#sendstate').html(msg.data);
    });


socket.on('my_sql_response', function(msg) {
    var sqlmessage=msg.data;
    $('#_sqlimage').html(msg.data); 
    url="data:image/png;base64,"+sqlmessage
    document.getElementById("img").setAttribute (
        'src', url
    );    
    });



socket.on('my_count_response', function(msg) {
    $('#countstate').html(msg.data);
    });
    

socket.on('modbus_response', function(msg) {
    var messageelement=msg.data;
    $('#modbusstate').html(msg.data); 
    if (messageelement === " On") {
        var elem = document.getElementById('demo');
        elem.style.color = 'green';
        elem.style.fontWeight = '900';
        elem.style.fontSize = '18px';
        var elem = document.getElementById('demo').innerHTML = " Connected";
    };
    if (messageelement === " Off") {
        var elem = document.getElementById('demo')
        elem.style.color = 'red';
        var elem = document.getElementById('demo').innerHTML = "";
    };


    });
    


$('form#database_emit').submit(function(event) {
    socket.emit('dbevent_pyrequest', {dbdatauser: $('#database_data1').val(),dbdatapw: $('#database_data2').val()});
    return false;
});


    socket.on('my_rate_response', function(msg) {
        $('#_speed').html(msg._speed);
        $('#_gain').html(msg._gain);
        $('#_time_in').html(msg._time_in);
        $('#_maxth').html(msg._maxth);
        $('#_rate').html(msg._rate);
        $('#_buffer').html(msg._buffer);
        $('#_sel_channel').html(msg._sel_channel);
        $('#_sel_amp').html(msg._sel_amp);
        $('#_height1').html(msg._height1);
        $('#_height2').html(msg._height2);
        $('#_height3').html(msg._height3);
        $('#_height4').html(msg._height4);
        $('#_humidity').html(msg._humidity);
        $('#_temp1').html(msg._temp1);
        $('#_temp2').html(msg._temp2);
        $('#_temp3').html(msg._temp3);
        $('#_CNT_THRESHOLD').html(msg._CNT_THRESHOLD);
        $('#_SQL_CONN').html(msg._SQL_CONN);
    });


  
});

