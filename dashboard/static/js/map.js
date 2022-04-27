window.onload=initmap;
/*window.onload=initpage
initpage(){
fetch("/GeoJSONDataCreation",{method:'GET'});
initmap();  
}
*/

function hideSidePanel(){
  document.getElementById("SidePanel").style.right="-350px";
}
function showSidePanel(){
  document.getElementById("SidePanel").style.visibility="visible";
document.getElementById("SidePanel").style.right="5px";
  }

function initmap(){
  //render base map

  const map = new ol.Map({
    view: new ol.View({
      center: ol.proj.fromLonLat([50.538699,26.180643]),
      zoom: 11,
      minZoom:11,
    }),
    layers:[
      new ol.layer.Tile({
        source: new ol.source.OSM()
      })
    ],
    target: 'map'
  })

//city source
var citysource = new ol.source.Vector({
  'projection': map.getView().getProjection(),
  format: new ol.format.GeoJSON(),
  'url': cityfile
});
//intersection source 
var intersectionsource = new ol.source.Vector({
  'projection': map.getView().getProjection(),
  format: new ol.format.GeoJSON(),
  'url': intersectionfile
});
//render heatmap
//customized gradient
const rainbow = [
  'rgba(102, 245, 66, 1.0)',
  'rgba(255, 247, 28, 1.0)',
  'rgba(255, 142, 28, 1.0)',
  'rgba(245, 25, 10, 1.0)',
  'rgba(143, 10, 245, 1.0)',
  'rgba(105, 9, 9, 1.0)',
]

const htlayer = new ol.layer.Heatmap({
  source: intersectionsource,
  blur: 30,
  gradient: rainbow,
  radius: 25,
  opacity:2,
  weight: function (feature) {
    // 2012_Earthquakes_Mag5.kml stores the magnitude of each earthquake in a
    // standards-violating <magnitude> tag in each Placemark.  We extract it from
    // the Placemark's name instead.
    var pinaqi = feature.get('avgAQI');
    console.log(pinaqi);
    const magnitude = (Number(160)/500);
    return magnitude;
    
  },
});
map.addLayer(htlayer);


//render intersection pins
var intersectionspinfunction =function(feature){
  var status=feature.get('OverallsensorStatus');
  if(status=='offline'){
    picstring=intersectionspinoffline;
  }
  else if(status=='online'){
    picstring=intersectionspinonline;
  }

  var retstyle=new ol.style.Style({
    image: new ol.style.Icon(({
      scale: [0.16, 0.16],
      src: picstring
    }))
  })
  return retstyle;
}
var intersectionsMarkerLayer = new ol.layer.Vector({
   minZoom:12,
   title:'intersectionsMarkerLayer',
  source: intersectionsource,
  style:intersectionspinfunction
});


map.addLayer(intersectionsMarkerLayer);
//change style of city pin based on AQI
var cityStyleFunction=function(feature){
  var aqi=feature.get('avgAQI');
  var picstring;
  if(aqi>0&&aqi<=50){
    picstring=goodpin;
  }
  else if(aqi>=51&&aqi<=100){
    picstring=moderatepin;
  }
  else if(aqi>=101&&aqi<=150){
    picstring=unhealthysgpin;
  }
  else if(aqi>=151&&aqi<=200){
    picstring=unhealthypin;
  }
  else if(aqi>=201&&aqi<=300){
    picstring=veryunhealthypin;
  }
  else if(aqi>=301){
    picstring=hazarduospin;
  }
  var retstyle=new ol.style.Style({
    image: new ol.style.Icon(({
      scale:[.13,.13],
      src: picstring
    }))
  })
  return retstyle;
}

//render city pins

var citiesMarkerLayer = new ol.layer.Vector({
  maxZoom:12,
  title:'citiesMarkerLayer',
  source: citysource,
  style:cityStyleFunction //used to change image source based on average AQI
});
map.addLayer(citiesMarkerLayer);

//Function to show pop up when intersection marker is clicked
const overlayContainerElement = document.querySelector('.overlay-container');
const overlayLayer = new ol.Overlay({
  element: overlayContainerElement
})
map.addOverlay(overlayLayer);
const overlayFeatureCityID=document.getElementById('FeatureCityID');
const overlayFeatureIntersectionID=document.getElementById('FeatureIntersectionID');
map.on('click',function(e){
  overlayLayer.setPosition(undefined);
    map.forEachFeatureAtPixel(e.pixel, function(feature,layer){
    if(feature.get('coordinateType')=='intersection'){
      let clickedFeatureCityID=feature.get('cityID');
    let clickedFeatureIntersectionID=feature.get('intersectionId');
    let clickedCoordinate = e.coordinate;
    overlayLayer.setPosition(clickedCoordinate);
   
    
    function createtable(){
      i=0;
      tstring='';
      tstring+='<table id="intersectionPopUpTable"><tr><th class="intersectionPopUpTableHeader">Sensor ID</th><th class="intersectionPopUpTableHeader">Status</th></tr>';
      const sensorsArray=feature.get('sensors');
      var noOfSensors=feature.get('noOfSensors');
      var statuscolor
      while(i<noOfSensors){
        if(sensorsArray[i]['sensorStatus']=="offline"){
          statuscolor="style='color:red'";
        }
        else if(sensorsArray[i]['sensorStatus']=="online"){
          statuscolor="style='color:green'";
        }
      tstring+= '<tr><td class="intersectionPopUpTableData">0'+(i+1)+'</td><td class="intersectionPopUpTableData"'+statuscolor+'>'+sensorsArray[i]["sensorStatus"]+'</td></tr>';
      i++;
    }  
    tstring+='</table>';
    console.log(tstring);

    const overlaytable=document.getElementById('overlay-container');
    overlaytable.innerHTML=tstring;
    }
    createtable(); }
  },
  {
    layerFilter: function(layerCandidate){ //ensures that pop up only appears when intersection layer is accessed
      return layerCandidate.get('title') ==='intersectionsMarkerLayer'
    }
  })
})


//function to show side panel when city marker is clicked
map.on('click',function(e){
    map.forEachFeatureAtPixel(e.pixel, function(feature,layer){
    if(feature.get('coordinateType')=='city'){

      const SidePanelTitle=document.getElementById('SidePanelTitle');
      const SidePanelAQI=document.getElementById('SidePanelAQI');
      const SidePanelWaitTime=document.getElementById('SidePanelWaitTime');
      const SidePanelNoOfVehicles=document.getElementById('SidePanelNoOfVehicles');
      let clickedFeatureCityName=feature.get('city');
      let clickedFeatureCityAQI=feature.get('avgAQI');
      let clickedFeatureCityWaitTime=feature.get('avgWaittime');
      let clickedFeatureNoOfVehicles=feature.get('sumOfVehicles');
      var AQIBorder='';
      var AQIColor='';

      function avgAQIElement(){
        var aqi=feature.get('avgAQI');
        if(aqi>0&&aqi<=50){
           AQIBorder='4px solid rgb(102, 245, 66)';
           AQIColor='rgb(102, 245, 66)';
        }
        else if(aqi>=51&&aqi<=100){
           AQIBorder='4px solid rgb(255, 247, 28)';
           AQIColor='rgb(255, 247, 28)';
        }
        else if(aqi>=101&&aqi<=150){
           AQIBorder='4px solid rgb(255, 142, 28)';
           AQIColor='rgb(255, 142, 28)';
        }
        else if(aqi>=151&&aqi<=200){
           AQIBorder='4px solid rgb(245, 25, 10)';
           AQIColor='rgb(245, 25, 10)';
        }
        else if(aqi>=201&&aqi<=300){
           AQIBorder='4px solid rgb(143, 10, 245)';
           AQIColor='rgb(143, 10, 245)';
        }
        else if(aqi>=301){
           AQIBorder='4px solid rgb(105, 9, 9)';
           AQIColor='rgb(105, 9, 9)';
        } 
      SidePanelAQI.style.color=AQIColor;
    SidePanelAQI.style.border=AQIBorder;
      }
      function cityTypeFunction(){
        if(feature.get('cityType')=="res"){
            return "Residential";
        }
      else if(feature.get('cityType')=="ind"){
        return "Industrial";
    }}
    avgAQIElement();
   
      SidePanelTitle.innerHTML=clickedFeatureCityName+' - '+cityTypeFunction();
      SidePanelAQI.innerHTML=clickedFeatureCityAQI;

      SidePanelWaitTime.innerHTML="Average Wait Time: "+ Math.round(((clickedFeatureCityWaitTime/60) + Number.EPSILON) * 100) / 100 + " Minutes"
      SidePanelNoOfVehicles.innerHTML="Total Number of Cars: "+clickedFeatureNoOfVehicles
      showSidePanel();
      } 
  },
  {
    layerFilter: function(layerCandidate){ //ensures that pop up only appears when intersection layer is accessed
      return layerCandidate.get('title') ==='citiesMarkerLayer'
    }
  })
})

} 

// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("SeeDetails");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
function  SeeDetailsPage(){
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
  function buttnClick(){ 
    fetch("/res",{method:'GET'}) 
    .then((data)=>{ 
    console.log(data.text) 
}) 
} 