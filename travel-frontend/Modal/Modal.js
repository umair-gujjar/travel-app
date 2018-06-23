import React, { Component } from 'react'
import { TextInput, Text, StyleSheet, Button, Modal } from 'react-native'

export default class ModalView extends Component {
  state = {
    text: ''
  }

  render () {
    return (
      <Modal
        style={styles.modal}
        animationType="slide"
        transparent={false}
        visible={this.props.openModal}
        onRequestClose={this.props.closeModal}
      >
        <Button
          onPress={this.props.closeModal}
          title='Close'
        />
        <Text>Type Title</Text>
        <TextInput
          style={{height: 40, borderColor: 'gray', borderWidth: 1}}
          onChangeText={(text) => this.setState({text})}
          value={this.state.text}
        />
        <Button
          onPress={() => this.props.submitMarker(this.state.text)}
          title='Submit'
        />
      </Modal>
    )
  }
}

const styles = StyleSheet.create({
  modal: {
    maxHeight: 300,
    maxWidth: 200
  }
})