var map = new BMap.Map("my_map");
map.centerAndZoom(new BMap.Point(114.218316, 22.692316), 20);
//单击获取点击的经纬度
var spots = [];
map.addEventListener("click", function (e) {
    spots.push([e.point.lng, e.point.lat])
    alert(e.point.lng + "," + e.point.lat);
});

// function send() {
//     $.ajax({
//         url: "127.0.0.1/receive_data",
//         type: "POST",
//         dataType: "json",
//         success: function (data) {
//             console.log(data)
//         }
//     })
// }


$(document).ready(function () {
    $('#upload').click(function () {
        $.post('/web_data', {data: JSON.stringify(spots)});
        spots = [];
    });


    var socket = io.connect('http://' + document.domain + ':' + location.port + '/data');

    socket.on('message', function (msg) {
        console.log(msg);
    })
    $('#clear').click(function () {
        // socket.emit('clear', "clear data");
        $.post('/clear');
    });

    // 假如搜索功能
    var ac = new BMap.Autocomplete(    //建立一个自动完成的对象
        {
            "input": "suggestId"
            , "location": map
        });

    ac.addEventListener("onhighlight", function (e) {  //鼠标放在下拉列表上的事件
        var str = "";
        var _value = e.fromitem.value;
        var value = "";
        if (e.fromitem.index > -1) {
            value = _value.province + _value.city + _value.district + _value.street + _value.business;
        }
        str = "FromItem<br />index = " + e.fromitem.index + "<br />value = " + value;

        value = "";
        if (e.toitem.index > -1) {
            _value = e.toitem.value;
            value = _value.province + _value.city + _value.district + _value.street + _value.business;
        }
        str += "<br />ToItem<br />index = " + e.toitem.index + "<br />value = " + value;
        G("searchResultPanel").innerHTML = str;
    });

    var myValue;
    ac.addEventListener("onconfirm", function (e) {    //鼠标点击下拉列表后的事件
        var _value = e.item.value;
        myValue = _value.province + _value.city + _value.district + _value.street + _value.business;
        G("searchResultPanel").innerHTML = "onconfirm<br />index = " + e.item.index + "<br />myValue = " + myValue;

        setPlace();
    });

    function G(id) {
        return document.getElementById(id);
    }

    function setPlace() {
        map.clearOverlays();    //清除地图上所有覆盖物
        function myFun() {
            var pp = local.getResults().getPoi(0).point;    //获取第一个智能搜索的结果
            map.centerAndZoom(pp, 20);
            map.addOverlay(new BMap.Marker(pp));    //添加标注
        }

        var local = new BMap.LocalSearch(map, { //智能搜索
            onSearchComplete: myFun
        });
        local.search(myValue);
    }


})
//
// $('.upload').click(function () {
//         $.post('/web_data', {data: JSON.stringify(spots)})
//     });
//     $('.clear').click(function () {
//         $.post('/clear',{})
//     });


