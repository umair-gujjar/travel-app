import React, { Component } from 'react'
import { TextInput, Text, StyleSheet, Button, Modal, View } from 'react-native'

export default class ModalView extends Component {
  state = {
    text: ''
  }

  render () {
    return (
      <Modal
        animationType="slide"
        transparent={false}
        visible={this.props.openModal}
        onRequestClose={this.props.closeModal}
      >
        <View
          style={styles.close}
        >
          <Button
            onPress={this.props.closeModal}
            title='x'
          />
        </View>
        <View style={styles.form}>
          <Text style={{fontWeight: 'bold'}}>Type Title</Text>
          <TextInput
            style={styles.input}
            onChangeText={(text) => this.setState({text})}
            value={this.state.text}
          />
          <Button
            onPress={() => this.state.text.length > 1 && this.props.submitMarker(this.state.text)}
            title='Submit'
          />
        </View>
      </Modal>
    )
  }
}

const styles = StyleSheet.create({
  close: {
    position: 'absolute',
    top: 10,
    right: 10,
    width: 40,
    height: 40,
    borderRadius: 100
  },
  form: {
    width: 300,
    marginTop: 100,
    alignSelf: 'center'
  },
  input: {
    height: 40,
    marginTop: 10,
    marginBottom: 10,
  }
})