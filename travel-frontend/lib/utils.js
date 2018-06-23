export const getHost = () => 'http://f0285c4d.ngrok.io'

export const processMarkers = markers => markers.map(marker => ({
  coords: {
    latitude: marker.geometry.location.lat,
    longitude: marker.geometry.location.lng
  },
  title: marker.name,
  types: marker.types
}))