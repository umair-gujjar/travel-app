export const getHost = () => 'http://5b684a58.ngrok.io'

export const processMarkers = markers => markers.map(marker => ({
  coords: {
    latitude: marker.geometry.location.lat,
    longitude: marker.geometry.location.lng
  },
  name: marker.name
}))