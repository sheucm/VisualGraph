var result = null
var areaLayers = []
var G_label_list = []
var ogc_fid_list = []
function display(geofile)
{
    $.getJSON(geofile, function(data){
            if (result != null){
                result.clearLayers();
            }
            result = L.geoJson(data).addTo(map);
    });
}



$(document).ready(function() {

    $('#checkbox_RuleC').change(function() {
        display("result_0927_1003_m5_i10000_k3.geojson")
    });
	

    $('.mycheckbox').change(function() {
        id = $(this).attr('interval').split('_'); 
        console.log(id)
    });
    $('#neighbors-checkbox').change(function() {
        console.log('here')
    });
    
    
    $('.dropdown-menu li').click(function() {
        id = $(this).parent().attr('aria-labelledby')
        changed_content = $(this).text()
        $('#'+id).attr('drop-value', changed_content)
        $('#'+id).text($(this).text())

    });


    // Unfinished
    $('#submit').click(function() {
        if ($(this).attr('class') == 'btn btn-primary disabled')
            return 
        
        var vars = get_SSB_var()  //method, table, max_nodes, iteration
        console.log(G_label_list)
        get_SSB({
            "method": vars[0], 
            "table": vars[1], 
            "max_nodes": vars[2], 
            "iteration": vars[3],
        })
    });
    $('#clear').click(function() {
        for (i=0; i<areaLayers.length; i++)
            map.removeLayer(areaLayers[i])
        for (i=0; i<G_label_list.length; i++){
            map.removeLayer(G_label_list[i])
        }
        areaLayers = []
        G_label_list = []
        ogc_fid_list = []
    });
});

function get_SSB_var(){
    var max_nodes = $('#number_of_blocks').val()
    var date_interval = $('#dropdownMenu1').attr('drop-value').split('~')
    var iteration = $('#iteration').val()
    var gte60 = $('#gte60-checkbox').is(':checked')
    var method = $('#dropdownMenu2').attr('drop-value')
    
    if (method == 'Greedy')  method = 'g'
    else if (method == 'Random Sample') method = 'r'
    else if (method == 'Montecarlo') method = 'm'

    var table = 'dengue_population_' + date_interval[0] + '_' + date_interval[1]
    if (gte60 == true)  table += '_gte60'


    return [method, table, max_nodes, iteration]
}

function get_SSB(submit_data){
    console.log('get_SSB')
    
    $('#submit').attr('class', 'btn btn-primary disabled')
    $.ajax({
        type: "GET",
        url: '/visual/get_SSB/',
        data: submit_data,
    })
    .done(function(geojsonFeature) {
        alert("成功"); 
        console.log(geojsonFeature)
        var areaLayer = L.geoJson(geojsonFeature, {
            onEachFeature: function (feature, layer) {
                label = layer.bindLabel(""+feature.properties.ogc_fid, { noHide: true });
            }
        }).addTo(map);
        console.log(areaLayer)
        areaLayers.push(areaLayer)
        

        // Show all labels in default
        features = geojsonFeature.features
        for (i=0; i<features.length; i++){
            lng = features[i].properties.centroid.lng
            lat = features[i].properties.centroid.lat
            content = features[i].properties.weight
            ogc_fid_list.append(features[i].properties.ogc_fid)
            label = new L.Label()
            label.setContent(""+content)
            label.setLatLng(L.latLng(lat, lng))
            map.showLabel(label);
            G_label_list.push(label)
        }
        
        $('#submit').attr('class', 'btn btn-primary active')

        // Neighbors
        

    })
    .fail(function() {
        alert("失敗");
        $('#submit').attr('class', 'btn btn-primary active')
    });
}


function get_neighbors(submit_data){
    $('#submit').attr('class', 'btn btn-primary disabled')
    $.ajax({
        type: "GET",
        url: '/visual/get_SSB/',
        data: submit_data,
    })
    .done(function(geojsonFeature) {
        alert("成功"); 
        console.log(geojsonFeature)
        var areaLayer = L.geoJson(geojsonFeature, {
            onEachFeature: function (feature, layer) {
                label = layer.bindLabel(""+feature.properties.ogc_fid, { noHide: true });
            }
        }).addTo(map);
        console.log(areaLayer)
        areaLayers.push(areaLayer)
        

        // Show all labels in default
        features = geojsonFeature.features
        for (i=0; i<features.length; i++){
            lng = features[i].properties.centroid.lng
            lat = features[i].properties.centroid.lat
            content = features[i].properties.weight
            ogc_fid_list.append(features[i].properties.ogc_fid)
            label = new L.Label()
            label.setContent(""+content)
            label.setLatLng(L.latLng(lat, lng))
            map.showLabel(label);
            G_label_list.push(label)
        }
        

        $('#submit').attr('class', 'btn btn-primary active')

    })
    .fail(function() {
        alert("失敗");
        $('#submit').attr('class', 'btn btn-primary active')
    });
}

