var current_user_id = 0;
var current_to_id = 0;


function sayHello(name){
    alert("Hello "+ name);
}

function send_message(){
    content =$('#txtMessage').val();
    $.ajax({
            url:'/messages',
            type:'POST',
            contentType:'application/json',
        data: JSON.stringify({
            "content": content,
            "user_from_id": current_user_id,
            "user_to_id" : current_to_id
        }),
        dataType: 'json'
    });
    get_messages(current_user_id,current_to_id)
    $('#txtMessage').val("")
}

function get_messages(user_from,user_to) {
    $.getJSON("/users/"+user_to, function(data){
        $('#user-to').html(data[0]['name']+" "+data[0]['fullname'])
    });
    alert("user_from: "+user_from+"user_to: "+user_to);
    current_to_id = user_to;
    $('#boxMessageInput').empty();
    var url ="/messages/"+current_user_id+"/"+current_to_id;
    $.getJSON(url,function (data) {
        var i=0;
        $.each(data,function () {
            user_from = current_user_id;
            user_to = data[i]['id'];

            if (i%2==0) {
            e= '<li class="sent alert" role="alert" onclick="get_messages(\'+user_from+\',\'+user_to+\')">';
            e = e + '<img src="http://www.redcapitalmx.com/wp-content/uploads/2018/02/chumel-torres-facebook.jpg" alt="" />';
            e = e + '<p>' + data[i]['content'] + '</p>';
            e = e + '</li>';
            }else{
                e= '<li class="replies alert" role="alert" onclick="get_messages(\'+user_from+\',\'+user_to+\')">';
            e = e + '<img src="http://www.redcapitalmx.com/wp-content/uploads/2018/02/chumel-torres-facebook.jpg" alt="" />';
            e = e + '<p>' + data[i]['content'] + '</p>';
            e = e + '</li>';
            }
            i=i+1;
            $("#boxMessageInput").append(e);
        });
    })
}


$.getJSON("/current_user", function(data){
    //alert(data.username);
    current_user_id=data['id'];
    $('#current_username').html(data['name']+" "+data['fullname'])
});


$.getJSON("/users", function(data){
    var i = 0;
    $.each(data,function () {
        user_from=current_user_id;
        user_to=data[i]['id'];
        e = '<li class="contact" onclick="get_messages(' + user_from + ',' + user_to +')">';
        e = e + '<div class="wrap">';
        e = e + '<span class="contact-status busy"></span>';
        e = e + '<img src="/static/images/profile.png" />';
        e = e + '<div class="meta">';
        e = e + '<p class="name">'+ data[i]['username'] + data[i]['fullname']+ '</p>';
        e = e + '<p class="preview">Hola Chumel!</p>';
        e = e + '</div>';
        e = e + '</div>';
        e = e + '</li>';
        i = i+1;
        $("#user").append(e);
        //$('<li/>', {html:e}).appendTo("#user"); -->versión del profe

    });

});



/* $.getJSON("/users", function(data){
    var i = 0;
    $.each(data,function () {
    <div class="alert"
        e = '<div class="wrap">';
        e = e + '<span class="contact-status busy"></span>';
        e = e + '<img src="https://yt3.ggpht.com/-7GTCq2PbO3o/AAAAAAAAAAI/AAAAAAAAAAA/eo7lM2pihH4/s900-c-k-no-mo-rj-c0xffffff/photo.jpg" />';
        e = e + '<div class="meta">';
        e = e + '<p class="name">'+data[i]['username'] + '</p>';
        e = e + '<p class="preview">Hola Chumel!</p>';
        e = e +'</div>';
        e = e +'</div>';
        i = i+1;
        $('<div class="contact"/>', {html:e}).appendTo("#user");

    });


});*/