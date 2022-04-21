var map = new ol.Map({
    target: 'map',
    layers: [
      new ol.layer.Tile({
        source: new ol.source.OSM()
      })
    ],
    view: new ol.View({
      center: ol.proj.fromLonLat([50.538699,26.180643]),
      zoom: 11,
      minZoom:10,
      
    })
  });