import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { TextField, Button, Grid, Typography } from '@material-ui/core';

export default class RoomJoinPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      error_msg: '',
      roomCode: '',
    };
    this.handleTextFieldChange = this.handleTextFieldChange.bind(this);
    this.roomButtonPressed = this.roomButtonPressed.bind(this);
  }

  handleTextFieldChange(e) {
    this.setState({
      roomCode: e.target.value,
    });
  }

  roomButtonPressed() {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        room_code: this.state.roomCode,
      }),
    };
    fetch('/api/join/', requestOptions)
      .then((response) => {
        if (response.ok) {
          this.props.history.push(`/room/${this.state.roomCode}/`);
        } else {
          this.setState({ error_msg: 'Room Not Found!' });
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }

  render() {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="Center">
          <Typography variant="h4" component="h4">
            Join a Room
          </Typography>
        </Grid>
        <Grid item xs={12} align="Center">
          <TextField
            error={this.state.error_msg === '' ? false : true}
            helperText={this.state.error_msg}
            placeholder="Enter Room Code"
            value={this.state.roomCode}
            variant="outlined"
            onChange={this.handleTextFieldChange}
          ></TextField>
        </Grid>
        <Grid item xs={12} align="Center">
          <Button
            variant="contained"
            color="primary"
            onClick={this.roomButtonPressed}
          >
            Enter Room
          </Button>
        </Grid>
        <Grid item xs={12} align="Center">
          <Button variant="contained" color="secondary" to="/" component={Link}>
            Back
          </Button>
        </Grid>
      </Grid>
    );
  }
}
