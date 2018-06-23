import React, { Component } from 'react'
import { Text, View, StyleSheet, TouchableOpacity } from 'react-native'
import { Constants, MapView, Location, Permissions } from 'expo'
import Markers from '../Markers/Markers'
import { getHost, processMarkers } from "../lib/utils";

const latitudeDelta = 0.01
const longitudeDelta = 0.01

export default class Map extends Component {
  constructor(props) {
    super(props)
    this.state = {
      mapRegion: null,
      hasLocationPermissions: false,
      locationResult: null,
      markers: []
    }
  }

  componentDidMount() {
    // this._initLocation()
  }

  componentDidUpdate() {
    if (this.state.locationResult && !this.state.markers.length) {
      // this._fetchMarkers()
    }
  }

  _checkPermissions = async () => {
    let { status } = await Permissions.askAsync(Permissions.LOCATION)
    if (status === 'granted') {
      this.setState({ hasLocationPermissions: true })
    }
  }

  _initLocation = async () => {
    await this._checkPermissions()
    await this._setCurrentPosition()
    this.setState({ locationResult: JSON.stringify(this.state.mapRegion) })
  }

  _setCurrentPosition = async () => {
    const { coords } = await Location.getCurrentPositionAsync({})
    this.setState({
      mapRegion: {
        latitude: coords.latitude,
        longitude: coords.longitude,
        latitudeDelta,
        longitudeDelta
      }
    })
  }

  _fetchMarkers = async () => {
    const { latitude, longitude } = this.state.mapRegion
    const fetchedMarkers = await fetch(`${getHost()}/rest/find-recommended?location=${latitude},${longitude}&radius=1000`)
    const data = await fetchedMarkers.json()
    if (data) {
      this.setState({ markers: processMarkers(data) })
    }
  }

  setMarker = (e) => {
    const { coordinate } = e.nativeEvent
    const markers = [...this.state.markers, {
      coords: {
        latitude: coordinate.latitude,
        longitude: coordinate.longitude
      }
    }]
    this.setState({ markers })
  }

  render() {
    const { locationResult, hasLocationPermissions, mapRegion, markers } = this.state

    return (
      <View style={styles.container}>
        <View
          style={{ width: '100%' }}
        >
          <MapView
            style={{ alignSelf: 'stretch', height: '100%' }}
            region={mapRegion}
            showsUserLocation={true}
            onLongPress={this.setMarker}
          >
            <Markers
              markers={markers}
            />
          </MapView>
          <TouchableOpacity
            style={styles.mapButton}
            onPress={this._setCurrentPosition}
          >
            <Text style={{ fontWeight: 'bold', color: 'black' }}>
              Me
            </Text>
          </TouchableOpacity>

        </View>
        {/*{*/}
        {/*locationResult === null ?*/}
        {/*<Text>Finding your current location...</Text> :*/}
        {/*hasLocationPermissions === false ?*/}
        {/*<Text>Location permissions are not granted.</Text> :*/}
        {/*mapRegion === null ?*/}
        {/*<Text>Map region doesn't exist.</Text> :*/}
        {/*<View*/}
        {/*style={{ width: '100%' }}*/}
        {/*>*/}
        {/*<MapView*/}
        {/*style={{ alignSelf: 'stretch', height: '100%' }}*/}
        {/*region={mapRegion}*/}
        {/*showsUserLocation={true}*/}
        {/*onLongPress={e => console.log(e)}*/}
        {/*>*/}
        {/*<Markers*/}
        {/*markers={markers}*/}
        {/*/>*/}
        {/*</MapView>*/}
        {/*<TouchableOpacity*/}
        {/*style={styles.mapButton}*/}
        {/*onPress={this._setCurrentPosition}*/}
        {/*>*/}
        {/*<Text style={{ fontWeight: 'bold', color: 'black' }}>*/}
        {/*Me*/}
        {/*</Text>*/}
        {/*</TouchableOpacity>*/}

        {/*</View>*/}
        {/*}*/}
      </View>

    )
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: Constants.statusBarHeight,
    backgroundColor: '#ecf0f1',
  },
  mapButton: {
    position: 'absolute',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    bottom: 30,
    right: 15,
    width: 40,
    height: 40,
    backgroundColor: '#fff',
    borderRadius: 50,
    opacity: 0.7
  }
})
