export const getHost = () => 'http://03845847.ngrok.io'

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
    latitude: marker.coords.latitude,
    longitude: marker.coords.longitude
  },
  title: marker.title,
  types: marker.types,
  users: users[Math.floor(Math.random() * users.length)]
}))

export const getDistanceFromLatLonInKm = (lat1,lon1,lat2,lon2) => {
  const R = 6371; // Radius of the earth in km
  const dLat = deg2rad(lat2-lat1);  // deg2rad below
  const dLon = deg2rad(lon2-lon1);
  const a =
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
    Math.sin(dLon/2) * Math.sin(dLon/2)
  ;
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  const d = R * c; // Distance in km
  return d;
}

const deg2rad = (deg) => {
  return deg * (Math.PI/180)
}