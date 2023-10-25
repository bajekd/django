import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import {
  Button,
  Collapse,
  Grid,
  Typography,
  TextField,
  FormHelperText,
  FormControl,
  Radio,
  RadioGroup,
  FormControlLabel
} from '@material-ui/core/';
import { Alert } from '@material-ui/lab';

export default class CreateRoomPage extends Component {
  static defaultProps = {
    update: false,
    roomCode: null,
    votesToSkip: 1,
    guestCanPause: false,
    updateCallback: () => {}
  };

  constructor(props) {
    super(props);
    this.state = {
      votesToSkip: this.props.votesToSkip,
      guestCanPause: this.props.guestCanPause,
      successMsg: '',
      errorMsg: ''
    };

    this.handleVotesChange = this.handleVotesChange.bind(this);
    this.handleGuestCanPauseChange = this.handleGuestCanPauseChange.bind(this);
    this.handleCreateRoomButtonPressed = this.handleCreateRoomButtonPressed.bind(this);
    this.handleUpdateRoomButtonPressed = this.handleUpdateRoomButtonPressed.bind(this);
  }

  handleVotesChange(e) {
    this.setState({
      votesToSkip: e.target.value
    });
  }

  handleGuestCanPauseChange(e) {
    this.setState({
      guestCanPause: e.target.value === 'true' ? true : false
    });
  }

  handleCreateRoomButtonPressed() {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        votes_to_skip: this.state.votesToSkip,
        guest_can_pause: this.state.guestCanPause
      })
    };
    fetch('/api/create/', requestOptions)
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error(response.status);
        }
      })
      .then((data) => this.props.history.push(`/room/${data.room_code}`))
      .catch((error) => {
        if (error.toString() === 'Error: 409') {
          this.setState({ errorMsg: 'You  already are host of the room!' });
        } else {
          this.setState({ errorMsg: 'Bad Request! Please fill all required fields' });
        }
      });
  }

  handleUpdateRoomButtonPressed() {
    const requestOptions = {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        room_code: this.props.roomCode,
        guest_can_pause: this.state.guestCanPause,
        votes_to_skip: this.state.votesToSkip
      })
    };
    fetch('/api/update/', requestOptions).then((response) => {
      if (response.ok) {
        this.setState({ successMsg: 'Room updated successfully!' });
      } else {
        this.setState({ errorMsg: 'Error occurred while updating room!' });
      }

      this.props.updateCallback();
    });
  }

  renderCreateButtons() {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Button variant="contained" color="primary" onClick={this.handleCreateRoomButtonPressed}>
            Create a Room
          </Button>
        </Grid>
        <Grid item xs={12} align="center">
          <Button variant="contained" color="secondary" to="/" component={Link}>
            Back
          </Button>
        </Grid>
      </Grid>
    );
  }

  renderUpdateButtons() {
    return (
      <Grid item xs={12} align="center">
        <Button variant="contained" color="primary" onClick={this.handleUpdateRoomButtonPressed}>
          Update a Room
        </Button>
      </Grid>
    );
  }

  render() {
    const title = this.props.update ? 'Update Room' : 'Create a Room';

    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Collapse in={this.state.successMsg != '' || this.state.errorMsg != ''}>
            {this.state.successMsg != '' ? (
              <Alert
                severity="success"
                onClose={() => {
                  this.setState({ successMsg: '' });
                }}
              >
                {this.state.successMsg}
              </Alert>
            ) : (
              <Alert
                severity="error"
                onClose={() => {
                  this.setState({ errorMsg: '' });
                }}
              >
                {this.state.errorMsg}
              </Alert>
            )}
          </Collapse>
        </Grid>
        <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
            {title}
          </Typography>
        </Grid>

        <Grid item xs={12} align="center">
          <FormControl component="fieldset">
            <FormHelperText variant="filled">Guest Control of Playback State</FormHelperText>
            <RadioGroup
              row
              defaultValue={this.props.guestCanPause.toString()}
              onChange={this.handleGuestCanPauseChange}
            >
              <FormControlLabel
                value="true"
                control={<Radio color="primary" />}
                label="Play/Pause"
                labelPlacement="bottom"
              />
              <FormControlLabel
                value="false"
                control={<Radio color="secondary" />}
                label="No Control"
                labelPlacement="bottom"
              />
            </RadioGroup>
          </FormControl>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl>
            <TextField
              error={this.state.errorMsg.includes('Bad Request!') ? true : false}
              type="number"
              onChange={this.handleVotesChange}
              defaultValue={this.state.votesToSkip}
              inputProps={{
                min: 1,
                style: { textAlign: 'center' }
              }}
            />
            <FormHelperText>Votes Required to Skip Song</FormHelperText>
          </FormControl>
        </Grid>
        {this.props.update ? this.renderUpdateButtons() : this.renderCreateButtons()}
      </Grid>
    );
  }
}
