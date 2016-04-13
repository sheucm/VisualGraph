var result = null
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
    
    
    $('.dropdown-menu li').click(function() {
        id = $(this).parent().attr('aria-labelledby')
        $('#'+id).text($(this).text())
    });


    // Unfinished
    $('#submit').click(function() {
        //Get points
        var submit_data = {
                "date1": '20150910', 
                "date2": '20150920', 
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
    });
});
