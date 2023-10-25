import React, { Component } from 'react';
import { Collapse, Grid, Typography, Card, IconButton, LinearProgress } from '@material-ui/core';
import { Alert } from '@material-ui/lab';
import PlayArrowIcon from '@material-ui/icons/PlayArrow';
import PauseIcon from '@material-ui/icons/Pause';
import SkipNextIcon from '@material-ui/icons/SkipNext';

export default class MusicPlayer extends Component {
  constructor(props) {
    super(props);
    this.state = { error: false, message: '' };
  }

  pauseSong() {
    const requestOptions = { method: 'PUT', headers: { 'Content-Type': 'application/json' } };
    fetch('/spotify/pause/', requestOptions)
      .then((response) => {
        if (!response.ok) {
          this.setState({ error: true });
        } else {
          this.setState({ error: false });
        }
        return response.json();
      })
      .then((data) => this.setState({ message: data.message }));
  }

  playSong() {
    const requestOptions = { method: 'PUT', headers: { 'Content-Type': 'application/json' } };
    fetch('/spotify/play/', requestOptions)
      .then((response) => {
        if (!response.ok) {
          this.setState({ error: true });
        } else {
          this.setState({ error: false });
        }
        return response.json();
      })
      .then((data) => this.setState({ message: data.message }));
  }

  skipSong() {
    const requestOptions = { method: 'POST', headers: { 'Content-Type': 'application/json' } };
    fetch('/spotify/skip/', requestOptions)
      .then((response) => {
        if (!response.ok) {
          this.setState({ error: true });
        } else {
          this.setState({ error: false });
        }
        return response.json();
      })
      .then((data) => this.setState({ message: data.message }));
  }

  render() {
    const songProgress = (this.props.time / this.props.duration) * 100;

    return (
      <Card>
        <Grid container alignItems="center">
          <Grid item xs={12} align="center">
            <Collapse in={this.state.error === true}>
              <Alert
                severity="error"
                onClose={() => {
                  this.setState({ error: false });
                }}
              >
                {this.state.message}
              </Alert>
            </Collapse>
          </Grid>
          <Grid item xs={4} align="center">
            <img src={this.props.image_url} alt="Album Cover" height="100%" width="100%" />
          </Grid>
          <Grid item xs={8} align="center">
            <Typography component="h5" variant="h5">
              {this.props.title}
            </Typography>
            <Typography color="textSecondary" variant="subtitle1">
              {this.props.artists}
            </Typography>
            <div>
              <IconButton onClick={() => (this.props.is_playing ? this.pauseSong() : this.playSong())}>
                {this.props.is_playing ? <PauseIcon /> : <PlayArrowIcon />}
              </IconButton>
              <IconButton onClick={() => this.skipSong()}>
                {this.props.votes} / {this.props.votes_required}
                <SkipNextIcon />
              </IconButton>
            </div>
          </Grid>
        </Grid>
        <LinearProgress variant="determinate" value={songProgress} />
      </Card>
    );
  }
}
