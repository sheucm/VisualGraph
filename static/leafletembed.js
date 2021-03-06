var map;
var ajaxRequest;
var plotlist;
var plotlayers=[];

function initmap() {
    // set up the map
    map = new L.Map('map');

    // create the tile layer with correct attribution
    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMapa> contributors';
    var osm = new L.TileLayer(osmUrl, {minZoom: 9, maxZoom: 18, attribution: osmAttrib});
    
    map.setView(new L.LatLng(23.01823,120.219646),12);
    map.addLayer(osm);

    //Get points
    var submit_data = {
            "date1": '20150927', 
            "date2": '20151003', 
            "gte60": 'f', 
        };
    $.ajax({
        type: "GET",
        url: '/visual/get_real_dengue_by_date/',
        data: submit_data,
    })
    .done(function(results) {   
        addPoints(results.points)
    })
    .fail(function() {
        alert("失敗");
    });


    
    
}



function addPoints(rows){
    for (var i=0;i<rows.length;i++){
        row = rows[i]
        var circle = L.circle([parseFloat(row[1]),parseFloat(row[0])],3, {
                        "color": ' #663333',
                        "fillColor": '#f03',
                        "fill-opacity": 0.9
                    }).addTo(map); 
    } 
}

function readTextFile(file)
{
    var rawFile = new XMLHttpRequest();
    var allText;
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                allText = rawFile.responseText;
                //console.log(allText);

            }
        }
    }
    rawFile.send(null);
    return allText;
}