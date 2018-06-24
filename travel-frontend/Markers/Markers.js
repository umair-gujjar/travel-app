import React, { Component } from 'react'
import { Text, View, StyleSheet, FlatList } from 'react-native'
import { Marker, Callout } from 'react-native-maps'
import { Badge } from 'react-native-elements'

const tagColors = ['#EF5350', '#EC407A', '#AB47BC', '#1E88E5', '#7E57C2', '#009688', '#E64A19']

export default Markers = (props) => {
  if (props.markers) {
    return props.markers.map((marker, idx) => {
      return (
        <Marker
          key={idx}
          coordinate={marker.coords}
          onPress={e => console.log(e.nativeEvent)}
        >
          <Callout style={styles.tooltip}>
            <View style={styles.title}>
              <Text
                style={{
                  fontWeight: 'bold',
                  fontSize: 16
                }}
              >{marker.title}</Text>
            </View>
            <FlatList
              data={marker.types}
              renderItem={({ item }) => {
                return (
                  <Badge
                    containerStyle={[styles.category, { backgroundColor: tagColors[Math.floor(Math.random() * tagColors.length)] }]}
                  >
                    <Text
                      style={{ color: '#fff', fontSize: 12 }}
                    >
                      {item}
                    </Text>
                  </Badge>
                )
              }}
              style={styles.categories}
            />
          </Callout>
        </Marker>
      )
    })
  }
  return null
}

const styles = StyleSheet.create({
  tooltip: {
    minWidth: 100,
    maxWidth: 200
  },
  category: {
    alignSelf: 'flex-start',
    marginBottom: 3
  },
  categories: {
    padding: 5,
    maxWidth: 200,
  },
  title: {
    alignSelf: 'center',
    marginBottom: 5
  }
})