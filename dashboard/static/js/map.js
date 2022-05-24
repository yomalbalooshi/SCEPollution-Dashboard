var map;
var view;
var overlayLayer; //pop up above intersection markers
var tempcord;
var intersectionJSON;
var seeDetailsArray;
var IntersectionDetailsArray;
// Get the modal
var intersectionmodal = document.getElementById("intersectionModal");
// Get the button that opens the modal
var btn = document.getElementById("SeeDetails");
// Get the <span> element that closes the modal
var intersectionspan = document.getElementById("intersectionModalClose");
// When the user clicks on the button, open the modal
// Get the modal
var comparisonmodal = document.getElementById("comparisonModal");
// Get the button that opens the modal
var cbtn = document.getElementById("comparsionButton");
// Get the <span> element that closes the modal
var cspan = document.getElementById("cspan");
// When the user clicks on the button, open the modal
//function  showComparisonModal(){
//  comparisonmodal.style.display = "block";
//}
//daterangepicker
src="https://cdn.jsdelivr.net/jquery/latest/jquery.min.js"
src="https://cdn.jsdelivr.net/momentjs/latest/moment.min.js"
src="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.min.js"
href="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.css"


view =new ol.View({
  center: ol.proj.fromLonLat([50.538699,26.180643]),
  zoom: 11,
  minZoom:11,
});

var source = new ol.source.XYZ({
  url: 'https://tile.thunderforest.com/atlas/{z}/{x}/{y}.png?apikey=177eb2f425eb49b385fffa16cc32440d' });
  map = new ol.Map({
    view: view,
    layers:[
      new ol.layer.Tile({
        source: source
      })
    ],
    target: 'map'
  }) 

function buttnClickPan(sensorarray,tempcord){//Panning+Zooming+Showing Overlay of intersection marker from See Details Page
intersectionmodal.style.display = "none";
 var sarray=sensorarray;
  var carray=ol.proj.fromLonLat(tempcord);
  view.animate({
    zoom:16,
    center: carray,
    duration: 1000,
    callback: showOverlaypop(sarray,carray),
  });
  
  
}
function AQITextColor(aqi){ //AQI color gradient
        if(aqi>0&&aqi<=50){
           AQIColor='rgb(102, 245, 66)';
        }
        else if(aqi>=51&&aqi<=100){
           AQIColor='rgb(255, 247, 28)';
        }
        else if(aqi>=101&&aqi<=150){
           AQIColor='rgb(255, 142, 28)';
        }
        else if(aqi>=151&&aqi<=200){
           AQIColor='rgb(245, 25, 10)';
        }
        else if(aqi>=201&&aqi<=300){
           AQIColor='rgb(143, 10, 245)';
        }
        else if(aqi>=301){
           AQIColor='rgb(105, 9, 9)';
        } 
        return AQIColor;
}

function printSensorStatus(sensorsArray){ //change sensor status circles' colors
  sensorstr='';
  for (let i = 0; i < sensorsArray.length; i++) {
    if(sensorsArray[i].sensorStatus=="offline")
    sensorstr+="<div class='dot' style='background-color:red;' title='Sensor ID: "+sensorsArray[i].sensorID+"'></div>";
    if(sensorsArray[i].sensorStatus=="online")
    sensorstr+="<div class='dot' style='background-color:#3ec742;' title='Sensor ID: "+sensorsArray[i].sensorID+"'></div>";
  }
  return sensorstr;
}
async function fetchFilterText(cityID) { //take JSON file and filter it for see details
  seeDetailsArray=[];
    let response = await fetch(intersectionfile);
    intersectionJSON = await response.json();
    var JSONfeatures = intersectionJSON['features'];
    let datatru=JSONfeatures;
    for (let i = 0; i < datatru.length; i++) {
      if(datatru[i].properties.cityID==cityID)
        seeDetailsArray.push(datatru[i]);
}
var vehicledictionary={};
var vehiclepercdictionary={};
var intersectionModalCityName=document.getElementById('intersectionModalCityName');
var intersectionModalTimeRange=document.getElementById('intersectionModalTimeRange');
function seeDetailsTypeFunction(){
  if(seeDetailsArray[0].properties.cityType=="res"){
      return "Residential";
  }
else if(seeDetailsArray[0].properties.cityType=="ind"){
  return "Industrial";
}}
intersectionModalCityName.innerHTML=seeDetailsArray[0].properties.city+" - "+seeDetailsTypeFunction();
intersectionModalTimeRange.innerHTML="TIMERANGE";
var sdstring='';
sdstring +='<table id="SeeDetailsTableContent"><tr><th class="seeDetailsHeader">Intersection</th><th class="seeDetailsHeader">AQI</th><th class="seeDetailsHeader">Sensors Status</th><th class="seeDetailsHeader">Wait Time</th><th class="seeDetailsHeader">Vehicle %</th><th class="seeDetailsHeader">Common Vehicle Type</th><th class="seeDetailsHeader">Show On Map</th></tr>';
for (let i = 0; i < seeDetailsArray.length; i++) {
      vehicledictionary== new Array();
      vehiclepercdictionary== new Array();
      const Car = {Cars:(Math.trunc(seeDetailsArray[i].properties.sumOfCars))};
      const Bus = {Busses:Math.trunc(seeDetailsArray[i].properties.sumOfBusses)};
      const Truck = {Trucks:Math.trunc(seeDetailsArray[i].properties.sumOfTrucks)};
      vehicledictionary={
    ...Car,
    ...Bus,
    ...Truck};
    const PercCar = {PercCar:((Math.trunc(seeDetailsArray[i].properties.sumOfCars))/Math.trunc(seeDetailsArray[i].properties.sumOfVehicles)*100).toFixed(3)};
    const PercBus = {PercBus:((Math.trunc(seeDetailsArray[i].properties.sumOfBusses))/Math.trunc(seeDetailsArray[i].properties.sumOfVehicles)*100).toFixed(3)};
    const PercTruck = {PercTruck:((Math.trunc(seeDetailsArray[i].properties.sumOfTrucks))/Math.trunc(seeDetailsArray[i].properties.sumOfVehicles)*100).toFixed(3)};
    vehiclepercdictionary={
    ...PercCar,
    ...PercBus,
    ...PercTruck};
      var sensorsarray=seeDetailsArray[i].properties.sensors;
      var sJSON=JSON.stringify(sensorsarray);
      console.log(sensorsarray);
      console.log(sJSON);
      var coordinatesarray =[seeDetailsArray[i].geometry.coordinates[0],seeDetailsArray[i].geometry.coordinates[1]];
      console.log(coordinatesarray);
      sdstring+="<tr>";
      sdstring+="<td class='seeDetailsData'>"+(i+1)+"</td>";
      sdstring+="<td class='seeDetailsData' style='color:"+AQITextColor(Math.trunc(seeDetailsArray[i].properties.averageAQI))+"'>"+Math.trunc(seeDetailsArray[i].properties.averageAQI)+"</td>";
      sdstring+="<td class='seeDetailsData'>"+printSensorStatus(seeDetailsArray[i].properties.sensors)+"</td>";
      sdstring+="<td class='seeDetailsData'>"+Math.round(((parseFloat(seeDetailsArray[i].properties.averageWaittime)/60) + Number.EPSILON) * 100) / 100 +" Minute(s)</td>";
      sdstring+="<td class='seeDetailsData'><div class='seeDetailsvehiclePercentageMainBar'><div class='sdsumOfBusses vehiclepart left' style='flex-basis:"+vehiclepercdictionary['PercBus']+"%' data-tip='Approx. "+vehiclepercdictionary['PercBus']+"% Busses'></div><div class='sdsumOfTrucks vehiclepart left'  style='flex-basis:"+vehiclepercdictionary['PercTruck']+"%' data-tip='Approx. "+vehiclepercdictionary['PercTruck']+"% Trucks'></div><div class='sdsumOfCars vehiclepart left'  style='flex-basis:"+vehiclepercdictionary['PercCar']+"%' data-tip='Approx. "+vehiclepercdictionary['PercCar']+"% Cars'></div></div></td>";
      sdstring+="<td class='seeDetailsData'>"+Object.keys(vehicledictionary).reduce(function(a, b){ return vehicledictionary[a] > vehicledictionary[b] ? a : b })+"</td>";
      sdstring+="<td><button class='showonmapbutton' onclick='buttnClickPan("+sJSON+",["+coordinatesarray+"])'>Show</td>";
      sdstring+="</tr>";
}
const SeeDetailsTable=document.getElementById('SeeDetailsTable');
sdstring+="</table>";
SeeDetailsTable.innerHTML=sdstring;
return 1;
}

function generateSeeDetailsInfo(cityID){
  fetchFilterText(cityID).then(generateSeeDetailsTable(seeDetailsArray));
}
function generateSeeDetailsTable(seeDetailsArray){ //temp 
  console.log(seeDetailsArray);

}

  function createSensorOverlaytable(sen){
    console.log("from table: "+JSON.stringify(sen));
    i=0;
    tstring='';
    tstring+='<table id="intersectionPopUpTable"><tr><th class="intersectionPopUpTableHeader">Sensor ID</th><th class="intersectionPopUpTableHeader">Status</th></tr>';
    var sensorsjsonArray=JSON.stringify(sen);
    var sensorsArray=JSON.parse(sensorsjsonArray);
    console.log("from sensorarray: "+sensorsArray[i]["sensorStatus"]);
    var noOfSensors=sensorsArray.length;
    var statuscolor
    while(i<noOfSensors){
      if(sensorsArray[i]["sensorStatus"]=="offline"){
        statuscolor="style='color:red'";
      }
      else if(sensorsArray[i]["sensorStatus"]=="online"){
        statuscolor="style='color:#3ec742'";
      }
    tstring+= '<tr><td class="intersectionPopUpTableData">0'+(i+1)+'</td><td class="intersectionPopUpTableData"'+statuscolor+'>'+sensorsArray[i]["sensorStatus"]+'</td></tr>';
   console.log(i);
    i++;
  }  
  tstring+='</table>';
  const overlaytable=document.getElementById('overlay-container');
  overlaytable.innerHTML=tstring;
  }
  
function showOverlaypop(featuresensorsarray,coord){
  var sarraytemp=featuresensorsarray;
  createSensorOverlaytable(sarraytemp);
  var featurecoord=coord;
  overlayLayer.setPosition(featurecoord);
  console.log("from overlay project:");
  console.log(featurecoord);
  console.log(sarraytemp);
   
}


function hideSidePanel(){
  document.getElementById("SidePanel").style.right="-350px";
  document.getElementById("SidePanel").style.display="none";

}
function showSidePanel(){
  document.getElementById("SidePanel").style.display="block";
document.getElementById("SidePanel").style.right="5px";
  }

function initmap(){
  //render base map
  
 view =new ol.View({
  center: ol.proj.fromLonLat([50.538699,26.180643]),
  zoom: 11,
  minZoom:11,
});

var source = new ol.source.XYZ({
  url: 'https://tile.thunderforest.com/atlas/{z}/{x}/{y}.png?apikey=177eb2f425eb49b385fffa16cc32440d' });
  map = new ol.Map({
    view: view,
    layers:[
      new ol.layer.Tile({
        source: source
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
//customized gradient for heatmap
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
  blur: 35,
  gradient: rainbow,
  radius: 20,
  opacity:2,
  weight: function (feature) {
    return feature.get("magnitude");
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
      scale: [0.45, 0.45],
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
  var picstring;
    picstring=citypin;
  var retstyle=new ol.style.Style({
    image: new ol.style.Icon(({
      scale:[.35,.35],
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
overlayLayer = new ol.Overlay({
  element: overlayContainerElement

})
map.addOverlay(overlayLayer);
const overlayFeatureCityID=document.getElementById('FeatureCityID');
const overlayFeatureIntersectionID=document.getElementById('FeatureIntersectionID');



map.on('click',function(e){
  overlayLayer.setPosition(undefined);
    map.forEachFeatureAtPixel(e.pixel, function(feature,layer){
    if(feature.get('coordinateType')=='intersection'){
      showOverlaypop(feature.get('sensors'),feature.getGeometry().getCoordinates());
     }
  },
  {
    layerFilter: function(layerCandidate){ //ensures that pop up only appears when intersection layer is accessed
      return layerCandidate.get('title') ==='intersectionsMarkerLayer'
    }
  })
})

view.on('change:resolution',function(e){
  if (view.getZoom()<=12){
    overlayLayer.setPosition(undefined);
  }
} )

//function to show side panel when city marker is clicked
map.on('click',function(e){
    map.forEachFeatureAtPixel(e.pixel, function(feature,layer){
    if(feature.get('coordinateType')=='city'){

      var SidePanelTitle=document.getElementById('SidePanelTitle');
      var SidePanelAQI=document.getElementById('SidePanelAQI');
      var SidePanelWaitTime=document.getElementById('SidePanelWaitTime');
      var SidePanelNoOfVehicles=document.getElementById('SidePanelNoOfVehicles');
      var SidePanelAQIChart=document.getElementById('AQIChart');
      document.getElementById("SeeDetailsLink").value=feature.get('city')+ " - " +feature.get('cityType');
      console.log("valueofseedetails:"+document.getElementById("SeeDetailsLink").value);
      document.getElementById("AddToCompareButton").value=feature.get('city')+ " - " +feature.get('cityType');

      let clickedFeatureCityName=feature.get('city');
      let clickedFeatureCityAQI=Math.trunc(feature.get('averageAQI'));
      let clickedFeatureCityWaitTime=Number(feature.get('averageWaittime'));
      let clickedFeatureNoOfVehicles=feature.get('sumOfVehicles');
      let clickedFeatureAvgAQIList=feature.get('avgHourlyAQI');
      var AQIBorder='';
      var AQIColor='';

function GenerateAQIGraph(AQIList){
  renderstring='';
  barhourstring='';
  var barHeight=0;
  for (let i = 0; i < AQIList.length; i++) {
    barHeight=(Number(AQIList[i]['averageAQI'])/500)*100;
    barcolor=AQITextColor(Number(AQIList[i]['averageAQI']));
    barhourstring=AQIList[i]['hourOfDay']+":00:00 and "+AQIList[i]['hourOfDay']+":59:59";
    renderstring+='<div class="singleBar"><div class="bar"><div class="value moveleft" style="height:'+barHeight+'%; background-color:'+barcolor+';" data-tip="Average AQI between '+barhourstring+" is "+Number(AQIList[i]['averageAQI'])+'""></div></div></div>';
    console.log(barHeight);
  }
  return renderstring;
}


      function avgAQIElement(){
        var aqi=Number(feature.get('averageAQI'));
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
   SidePanelAQIChart.innerHTML=GenerateAQIGraph(clickedFeatureAvgAQIList);
      SidePanelTitle.innerHTML=clickedFeatureCityName+" - "+cityTypeFunction();
      SidePanelAQI.innerHTML=clickedFeatureCityAQI;

      SidePanelWaitTime.innerHTML="Average Wait Time: "+ Math.round(((clickedFeatureCityWaitTime/60) + Number.EPSILON) * 100) / 100 + " Minutes"
      SidePanelNoOfVehicles.innerHTML="Sum of Vehicles: "+clickedFeatureNoOfVehicles
      
      showSidePanel();
      generateSeeDetailsInfo(feature.get('cityID'));
      } 
  },
  {
    layerFilter: function(layerCandidate){ //ensures that pop up only appears when intersection layer is accessed
      return layerCandidate.get('title') ==='citiesMarkerLayer'
    }
  })
})

} 


//function  SeeDetailsPage(){
//  intersectionmodal.style.display = "block";
//}
// When the user clicks on <span> (x), close the modal
intersectionspan.onclick = function() {
  intersectionmodal.style.display = "none";
}
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == intersectionmodal) {
    intersectionmodal.style.display = "none";
  }
}

// When the user clicks on <span> (x), close the modal
cspan.onclick = function() {
  comparisonmodal.style.display = "none";
  citiestoCompare = [];
  document.getElementById('comp').innerHTML = '';
  document.getElementById('comparisonFooterDiv').style.display = "none";



}
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == comparisonmodal) {
    citiestoCompare = [];
    comparisonmodal.style.display = "none";
    document.getElementById('comp').innerHTML = '';
    document.getElementById('comparisonFooterDiv').style.display = "none";



  }
}
  function getMainDashboardElements(){ //used to get Main table and GeoJSON files
    var mainDashboardCitiesTableDiv = document.getElementById('mainDashboardCitiesTable');
	        fetch("/res",{method:'GET',mode: "no-cors",}) 
	        .then((response) => { return response.text(); })
            .then((content) => { 
              mainDashboardCitiesTableDiv.innerHTML = content; });

} 

