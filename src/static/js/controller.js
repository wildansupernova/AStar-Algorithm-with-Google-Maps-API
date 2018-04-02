var markerCollection = [];
var ajasensiList = [];
var idGenerate = 0;
var selectStatus = false;
var selectedPin;

var goal =-1;
var start = -1;

function distance(lat1,lon1,lat2,lon2) {
    var R = 6371; // earth radius , assumption: the earth is like sphere or ball, mountains not counted or other else curve
    var theta1 = lat1 * Math.PI / 180;
    var theta2 = lat2 * Math.PI / 180;
    var ohm1 = lon1 * Math.PI / 180;
    var ohm2 = lon2 * Math.PI / 180;
    
    var r1x = R*Math.cos(theta1)*Math.cos(ohm1);
    var r1y = R*Math.cos(theta1)*Math.sin(ohm1);
    var r1z = R*Math.sin(theta1);

    var r2x = R*Math.cos(theta2)*Math.cos(ohm2);
    var r2y = R*Math.cos(theta2)*Math.sin(ohm2);
    var r2z = R*Math.sin(theta2);
    var d = Math.sqrt( ((r1x-r2x)*(r1x-r2x)) + ((r1y-r2y)*(r1y-r2y)) + ((r1z-r2z)*(r1z-r2z)))
    //Keluaran dalam meter
    return Math.round(d*1000);
}


function markerAddListener(marker,map){
    marker.addListener('dblclick',function(){
        if(selectStatus){
            if(marker.id!=markerCollection[selectedPin].id){
                selectStatus = false;
                var rulerpoly = new google.maps.Polyline({
                    path: [markerCollection[selectedPin].position, marker.position] ,
                    strokeColor: "#82e008",
                    strokeOpacity: .7,
                    strokeWeight: 7
                });
                rulerpoly.setMap(map);


                //Add to ajasensi list
                ajasensiList[marker.id].push(markerCollection[selectedPin].id);
                ajasensiList[markerCollection[selectedPin].id].push(marker.id);
                // End

                /// Code for add distance label


                var inBetween = google.maps.geometry.spherical.interpolate(marker.position, markerCollection[selectedPin].position, 0.5);
                var labelPoly = new Label({ 
                    map: map,
                    position: inBetween
                });
                labelPoly.set('text',distance( marker.getPosition().lat(), marker.getPosition().lng(), markerCollection[selectedPin].getPosition().lat(),markerCollection[selectedPin].getPosition().lng())+" meter");
                
                ///End
            }
        } else{
            
            selectStatus = true;
            selectedPin = marker.id;
        }
        updateShow();
    });
    //Double clicl select start node
    marker.addListener('click',function(){
        // marker.setIcon('http://wildandicky.me/FrontEnd/assets/purple.png')
        //alert('lol');
        if(start==-1){
            marker.setIcon('http://wildandicky.me/FrontEnd/assets/purple.png');
            start = marker.id;
        } else{
            markerCollection[start].setIcon('https://maps.gstatic.com/mapfiles/api-3/images/spotlight-poi-dotless2.png');
            marker.setIcon('http://wildandicky.me/FrontEnd/assets/purple.png');
            start = marker.id;            
        }
    });


    //Right click set goal
    marker.addListener('rightclick',function(){
        // marker.setIcon('http://wildandicky.me/FrontEnd/assets/purple.png')
        //alert('lol');
        if(goal==-1){
            marker.setIcon('http://wildandicky.me/FrontEnd/assets/yellow.png');
            goal = marker.id;
        } else{
            markerCollection[goal].setIcon('https://maps.gstatic.com/mapfiles/api-3/images/spotlight-poi-dotless2.png');
            marker.setIcon('http://wildandicky.me/FrontEnd/assets/yellow.png');
            goal = marker.id;            
        }
    });
}
function addMarker(position,map){
    var marker = new google.maps.Marker({
        position: position,
        map: map,
        label: idGenerate.toString(),
        id:idGenerate,
    });
    //marker.setIcon('http://maps.google.com/mapfiles/ms/icons/green.png')
    idGenerate++;
    markerCollection.push(marker);
    markerAddListener(marker,map);
    ajasensiList.push([]);
    return marker;
}

function hasilID(){
    var i;
    var str="";
    for(i=0;i<idGenerate;i++){
        str = str + " "+ markerCollection[i].label;
    }
    return str;
}


function makeTabelDiv(){
    var str = "";
    var i;
    var j;
    str = '<table class="table table-bordered">';
    str += '<tbody>';
    //Initiate the body table
    //UpHead Section
    str+= '<tr>';
    str+= '<td>from / to</td>'
    for(i=0;i<idGenerate;i++){
        str+='<td>';
        str+=i.toString();
        str+='</td>';
    }
    str+= '</tr>';
    //End Section

    //Partial Body Section
    for(i=0;i<idGenerate;i++){
        str+='<tr>';
        //Left Head section
        str+='<td>'+i.toString()+'</td>';
        //End Section

        //Body real section
        for(j=0;j<idGenerate;j++){
            str+='<td>';
            if (ajasensiList[i].indexOf(j)!=-1){
                str+=distance( markerCollection[i].getPosition().lat(), markerCollection[i].getPosition().lng(), markerCollection[j].getPosition().lat(),markerCollection[j].getPosition().lng())+" meter";
            } else{
                str+='undefined';
            }
            str+='</td>';
        }
        //End Section
        str+='</tr>';
    }
    //End body table
   
    str += '</tbody>';
    str = str + '</table>';
    return str;
}


function updateShow(){
    document.getElementById("hasil").innerHTML = hasilID();
    document.getElementById("tabelMatrix").innerHTML = makeTabelDiv();
}
function initializeMapVariabel() {
	var myOptions = {
	  zoom: 17,
	  center:  new google.maps.LatLng(-6.891161, 107.610633) ,
	  mapTypeId: google.maps.MapTypeId.ROADMAP,
	  mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU}

	};
	
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
    initSearchBox(map);
    map.addListener('click', function(e) {
        addMarker(e.latLng, map);
        updateShow();

        
        
    });
}





function initSearchBox(map){
    // Create the search box and link it to the UI element.
    
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);
    
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function() {
    searchBox.setBounds(map.getBounds());
    });

    var markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function() {
    var places = searchBox.getPlaces();

    if (places.length == 0) {
        return;
    }

    // Clear out the old markers.
    markers.forEach(function(marker) {
        marker.setMap(null);
    });
    markers = [];

    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(place) {
        if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
        }
        var icon = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25)
        };

        // Create a marker for each place.
        markers.push(new google.maps.Marker({
        map: map,
        icon: icon,
        title: place.name,
        position: place.geometry.location
        }));

        if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
        } else {
        bounds.extend(place.geometry.location);
        }
    });
    map.fitBounds(bounds);
    });
}


function requestFlask(){


    var dataMasukan = {};
    var i;
    var j;
    // dataMasukan.email = ["wildan@gmail.com","lol@gmail.com"]
    dataMasukan.size = idGenerate;
    //Masukan data node latitude and longitude
    dataMasukan.node = [];
    for(i=0;i<idGenerate;i++){
        var position = {
            "latitude" : markerCollection[i].getPosition().lat(),
            "longitude" : markerCollection[i].getPosition().lng()
        }
        dataMasukan.node.push(position);
    }

    //Masukan Ajasensi list

    dataMasukan.adj=[]

    for(i=0;i<idGenerate;i++){
        var listAdj =[];
        for(j=0;j<ajasensiList[i].length;j++){
            listAdj.push(ajasensiList[i][j]);
        }
        dataMasukan.adj.push(listAdj);
    }

    //////



    //Masukan start node and goal
    dataMasukan.start  = start;
    dataMasukan.goal = goal;

    //

    var xhr = new XMLHttpRequest();
    var url = "/compute";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var json = JSON.parse(xhr.responseText);
            //console.log(json.email + ", " + json.password);
            var n = json.path.length;
            var i;
            console.log(json.cost);
            console.log(n);
            for(i=0;i<n-1;i++){
                var rulerpoly = new google.maps.Polyline({
                    path: [markerCollection[json.path[i]].position, markerCollection[json.path[i+1]].position] ,
                    strokeColor: "#f93b3b",
                    strokeOpacity: .7,
                    strokeWeight: 7
                
                });
                rulerpoly.setMap(map);
                
            }
        }
    };

    var data = JSON.stringify(dataMasukan);
    xhr.send(data);
}



function restartAll(){
    markerCollection = [];
    ajasensiList = [];
    idGenerate = 0;
    selectStatus = false;
    goal =-1;
    start = -1;
    var div = document.createElement("INPUT");
    div.setAttribute("type", "text");
    div.setAttribute("placeholder", "Search here..");
    div.setAttribute("class", "controls");
    div.setAttribute("id", "pac-input");

	document.body.appendChild(div);

    initializeMapVariabel();
    updateShow();
}