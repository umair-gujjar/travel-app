import React, { Component } from 'react'
import { Marker } from 'react-native-maps'

export default Markers = (props) => {
  if (props.markers) {
    return props.markers.map((marker, idx) => {
      return (
        <Marker key={idx} coordinate={marker.coords} />
      )
    })
  }
  return null
}