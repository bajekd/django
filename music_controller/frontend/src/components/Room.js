import React, { Component } from 'react';
import { Grid, Button, Typography } from '@material-ui/core';
import CreateRoomPage from './CreateRoomPage';
import MusicPlayer from './MusicPlayer';

export default class Room extends Component {
  constructor(props) {
    super(props);
    this.state = {
      votesToSkip: 1,
      guestCanPause: false,
      isHost: false,
      showSettings: false,
      spotifyAuthenticated: false,
      song: {}
    };

    this.roomCode = this.props.match.params.roomCode;

    this.leaveButtonPressed = this.leaveButtonPressed.bind(this);
    this.updateShowSettings = this.updateShowSettings.bind(this);
    this.renderSettingsButton = this.renderSettingsButton.bind(this);
    this.renderSettings = this.renderSettings.bind(this);
    this.getRoomDetails = this.getRoomDetails.bind(this);
    this.spotifyAuthenticate = this.spotifyAuthenticate.bind(this);
    this.getCurrentSong = this.getCurrentSong.bind(this);

    this.getRoomDetails();
  }

  componentDidMount() {
    this.interval = setInterval(this.getCurrentSong, 200);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  leaveRoom() {
    this.props.leaveRoomCallback();
    this.props.history.push('/');
  }

  getRoomDetails() {
    fetch(`/api/room/${this.roomCode}`)
      .then((response) => {
        if (!response.ok) {
          this.leaveRoom();
        }

        return response.json();
      })
      .then((data) => {
        this.setState({
          votesToSkip: data.votes_to_skip,
          guestCanPause: data.guest_can_pause,
          isHost: data.is_host
        });
        if (this.state.isHost) {
          this.spotifyAuthenticate();
        }
      });
  }

  spotifyAuthenticate() {
    fetch('/spotify/is-authenticated/')
      .then((response) => response.json())
      .then((data) => {
        this.setState({ spotifyAuthenticated: data.is_authenticated });
        if (!data.is_authenticated) {
          fetch('/spotify/get-auth-url/')
            .then((response) => response.json())
            .then((data) => {
              window.location.replace(data.url);
            });
        }
      });
  }

  getCurrentSong() {
    fetch('/spotify/current-song/')
      .then((response) => {
        if (!response.ok) {
          return {};
        } else {
          return response.json();
        }
      })
      .then((data) => {
        this.setState({ song: data });
      });
  }

  leaveButtonPressed() {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    };
    fetch('/api/leave_room/', requestOptions).then((_) => {
      this.leaveRoom();
    });
  }

  updateShowSettings(boolean) {
    this.setState({
      showSettings: boolean
    });
  }

  renderSettingsButton() {
    return (
      <Grid item xs={12} align="center">
        <Button
          variant="contained"
          color="primary"
          onClick={() => {
            this.updateShowSettings(true);
          }}
        >
          Settings
        </Button>
      </Grid>
    );
  }

  renderSettings() {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <CreateRoomPage
            update={true}
            roomCode={this.roomCode}
            votesToSkip={this.state.votes_to_skip}
            guestCanPause={this.state.guestCanPause}
            updateCallback={this.getRoomDetails}
          />
        </Grid>
        <Grid item xs={12} align="center">
          <Button
            variant="contained"
            color="secondary"
            onClick={() => {
              this.updateShowSettings(false);
            }}
          >
            Close
          </Button>
        </Grid>
      </Grid>
    );
  }

  render() {
    if (this.state.showSettings) {
      return this.renderSettings();
    }
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Typography variant="h3" component="h3">
            Room code: {this.roomCode}
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <MusicPlayer {...this.state.song} />
        </Grid>
        {this.state.isHost ? this.renderSettingsButton() : null}
        <Grid item xs={12} align="center">
          <Button variant="contained" color="secondary" onClick={this.leaveButtonPressed}>
            Leave a Room
          </Button>
        </Grid>
      </Grid>
    );
  }
}
