#!/usr/bin/env python3
"""Back up ratings and play counts for a Google Play Music account"""
import json
import ratings_sync_lib.cli as cli


def write_tracks(filename, tracks):
    with open(filename, mode='w', encoding='utf-8') as dest:
        dest.write('\n'.join(tracks))

    print(len(tracks), "rated/listened tracks found, written to", filename)


def write_tracks_repr(filename, tracks):
    tracks = [repr(track) for track in tracks]
    write_tracks(filename, tracks)


def write_tracks_json(filename, tracks):
    with open(filename, mode='w', encoding='utf-8') as dest:
        json.dump(tracks, dest)


def main():
    """Executes the backup"""

    api = cli.login()

    # Get all tracks
    print('Getting library')
    library = api.get_all_songs()
    print('Library retrieved:', len(library), "tracks received")

    # Store tracks with ratings that aren't 0, or have been listened to at least once
    # Note that rating is a string.  Don't ask me why, ask Google.  playCount is a number.
    rated_tracks = [
        track for track in library if
        ('rating' in track and track['rating'] != '0')
        or ('playCount' in track and track['playCount'] > 0)
    ]

    # Output tracks
    write_tracks_repr('downloaded_ratings.txt', rated_tracks)
    write_tracks_json('downloaded_ratings.json', rated_tracks)

main()
