import React, { Component } from 'react'
import MapView from 'react-native-maps'

const LATITUDE_DELTA = 0.01
const LONGITUDE_DELTA = 0.01
const initialRegion = {
  latitude: 50.0755,
  longitude: 14.4378,
  latitudeDelta: 0.0922,
  longitudeDelta: 0.0421,
}

class Map extends Component {
  constructor(props) {
    super(props)
    this.state = {
      region: initialRegion,
      flex: 0
    }
  }

  componentDidMount() {
    this.getCurrentPosition()
    setTimeout(() => this.setState({ flex: 1 }), 500);
  }

  getCurrentPosition() {
    try {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const region = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            latitudeDelta: LATITUDE_DELTA,
            longitudeDelta: LONGITUDE_DELTA,
          }
          this.setState({ region })
        },
        (error) => {
          console.log(error)
        }
      )
    } catch (e) {
      console.log(e)
    }
  }

  render() {
    return (
      <MapView
        style={{ flex: this.state.flex }}
        initialRegion={this.initialRegion}
        region={this.state.region}
        showsUserLocation
      />
    )
  }
}

export default Map
