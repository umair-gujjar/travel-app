export const getHost = () => 'http://d42b979b.ngrok.io'

export const getUserId = () => 1

const users = [
  [1, 2, 3, 4],
  [2, 3, 4],
  [3, 4],
  [4]
]

export const processMarkers = markers => markers.map(marker => ({
  id: marker.id,
  coords: {
    latitude: marker.geometry.location.lat,
    longitude: marker.geometry.location.lng
  },
  title: marker.name,
  types: marker.types,
  users: users[Math.floor(Math.random() * users.length)]
}))