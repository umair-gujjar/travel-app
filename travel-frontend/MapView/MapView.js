import React, { Component } from 'react'
import { Text, View, StyleSheet, TouchableOpacity } from 'react-native'
import { Constants, MapView, Location, Permissions } from 'expo'
import Markers from '../Markers/Markers'
import ModalView from '../Modal/Modal'
import { getHost, processMarkers, getUserId, getDistanceFromLatLonInKm } from "../lib/utils";
import axios from 'axios'

const latitudeDelta = 0.01
const longitudeDelta = 0.01

export default class Map extends Component {
  constructor(props) {
    super(props)
    this.state = {
      currentLocation: null,
      oldLocation: null,
      hasLocationPermissions: false,
      locationResult: null,
      markers: [],
      openModal: false
    }
  }

  componentDidMount() {
    this._initLocation()

    setTimeout(() => {
      if (this.state.locationResult && this.state.oldLocation) {
        const {
          currentLocation: {
            latitude,
            longitude
          },
          oldLocation: {
            latitude: oldLat,
            longitude: oldLng,
          }
        } = this.state
        const distance = getDistanceFromLatLonInKm(latitude, longitude, oldLat, oldLng)
        if (distance > 0.1) {
          console.log('test')
          this._fetchMarkers()
        }
      }
    }, 10000);
  }

  componentDidUpdate() {
    if (this.state.locationResult && !this.state.markers.length) {
      this._fetchMarkers()
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
    this.setState({ locationResult: JSON.stringify(this.state.currentLocation) })
  }

  _setCurrentPosition = async () => {
    const { coords } = await Location.getCurrentPositionAsync({})
    if (this.state.currentLocation) {
      this.setState({
        oldLocation: {
          latitude: this.state.currentLocation.latitude,
          longitude: this.state.currentLocation.longitude
        }
      })
    }
    this.setState({
      currentLocation: {
        latitude: coords.latitude,
        longitude: coords.longitude
      }
    })
  }

  _fetchMarkers = async () => {
    const { latitude, longitude } = this.state.currentLocation
    const url = `${getHost()}/rest/find-recommended?location=${latitude},${longitude}&radius=1000`
    try {
      const { data } = await axios.get(url)
      if (data) {
        this.setState({ markers: processMarkers(data) })
      }
    } catch (e) {
      console.log(e)
    }
  }

  setMarker = (title) => {
    const { currentCoords } = this.state
    const newMarker = {
      coords: {
        latitude: currentCoords.latitude,
        longitude: currentCoords.longitude
      },
      title,
      types: [],
      users: [getUserId()]
    }
    const markers = [...this.state.markers, newMarker]
    this.setState({ markers })
    const url = `${getHost()}/rest/add-location`
    axios.post(url, JSON.stringify(newMarker))
  }

  openModal = (e) => {
    const { coordinate } = e.nativeEvent
    this.setState({ openModal: true, currentCoords: coordinate })
  }

  closeModal = () => {
    this.setState({ openModal: false })
  }

  submitMarker = (title) => {
    this.setMarker(title)
    this.closeModal()
  }

  likeMarker = (id) => {
    const newMarkers = this.state.markers.map(marker => marker.id !== id ? marker : {
      ...marker,
      users: !marker.users.includes(id) ? [...marker.users, id] : marker.users
    })
    this.setState({ markers: newMarkers })
  }

  render() {
    const { locationResult, hasLocationPermissions, currentLocation, markers, openModal } = this.state

    return (
      <View style={styles.container}>
        {
          locationResult === null ?
            <Text>Finding your current location...</Text> :
            hasLocationPermissions === false ?
              <Text>Location permissions are not granted.</Text> :
              currentLocation === null ?
                <Text>Map region doesn't exist.</Text> :
                <View
                  style={{ width: '100%' }}
                >
                  <MapView
                    style={{ alignSelf: 'stretch', height: '100%' }}
                    region={{
                      ...currentLocation,
                      latitudeDelta,
                      longitudeDelta
                    }}
                    showsUserLocation={true}
                    onLongPress={this.openModal}
                  >
                    <Markers
                      markers={markers}
                      likeMarker={this.likeMarker}
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
                  {openModal && <ModalView
                    openModal={openModal}
                    closeModal={this.closeModal}
                    submitMarker={this.submitMarker}
                  />}
                </View>
        }
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
