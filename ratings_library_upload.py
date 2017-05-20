#!/usr/bin/env python3
"""Uploads ratings and play counts from a specially-formatted library file

The ratings file is expected to be in the format:
title :: artist :: album :: track number :: disc number :: rating
"""
import sys
import string
import getpass # Get a password from standard in in a secure fashion
import codecs  # Read Unicode from a file
from gmusicapi import Mobileclient

def main():
    """Executes the library upload"""

    # Check we have at least one argument (the ratings file name).
    # Remember that the script name is one of the arguments, so we expect argv to
    # have two items.
    if len(sys.argv) <= 1:
        print('Argument missing.  Provide path to ratings file.')
        sys.exit(1)

    ratings_file_name = sys.argv[1]

    # We have a valid ratings file, parse it
    ratings_file = codecs.open(ratings_file_name, mode='r', encoding='utf-8')
    tracks_to_rate = []

    for line in ratings_file:
        # The ratings file is expected to be in the format:
        # title :: artist :: album :: track number :: disc number :: rating

        # Strip any line break from the line
        line = line.rstrip('\n')

        # Get metadata
        title, artist, album, track_no, disc_no, rating = string.split(line, ' :: ')
        track = {
            'title': title,
            'artist': artist,
            'album': album,
            'trackNumber': track_no,
            'discNumber': disc_no,
            'rating': rating
        }

        # If number fields are empty, init to zero
        if track['trackNumber'] == '': track['trackNumber'] = 0
        if track['discNumber'] == '': track['discNumber'] = 0

        tracks_to_rate.append(track)

    ratings_file.close()
    print('Parsed', len(tracks_to_rate), 'tracks with ratings')

    # Log in to Google Play Music
    print('Logging in to Google Play Music')
    try:
        client = login.login_for_library_management()
    except RuntimeError as error:
        print(error)
        sys.exit(1)
    print('Logged in successfully')

    # Get all tracks
    print('Getting library')
    gm_library = mc.get_all_songs()
    print('Library retrieved:', len(gm_library), "tracks received")

    # For each track in ratings file, apply its rating
    tracks_to_update = []

    for ra_track in tracks_to_rate:
        # Find the track we are looking for
        #track = next(gm_track for gm_track in gm_library if gm_track['title'] == ra_track['title'])
        # or (potentially returns multiple tracks)
        matched_tracks = [
            gm_track for gm_track in gm_library if
            gm_track['title'] == ra_track['title']
            and gm_track['artist'] == ra_track['artist']
            and gm_track['album'] == ra_track['album']
            and gm_track['trackNumber'] == int(ra_track['trackNumber'])
            and gm_track['discNumber'] == int(ra_track['discNumber'])
        ]

        # If there is no track, skip
        if len(matched_tracks) == 0:
            print('No track matched.  Skipping:')
            print(str(ra_track))
            continue

        # If there is more than one track, skip
        if len(matched_tracks) > 1:
            print('Multiple tracks matched, ambiguous which should be updated.  Skipping:')
            print(str(ra_track))
            print(str(matched_tracks))
            continue

        # There is only one matching track, set the rating
        matched_track = matched_tracks[0]
        if matched_track['rating'] != ra_track['rating']:
            matched_track['rating'] = ra_track['rating']

            # Enqueue update
            tracks_to_update.append(matched_track)
        else:
            print('Track rating already up to date.  Skipping.')
            print(str(ra_track))
            continue

    # Update all tracks on Google Play Music
    print('Updating', len(tracks_to_update), 'tracks on Google Play Music')

    for track in tracks_to_update:
        print(str(track))

    if len(tracks_to_update) > 0:
        mc.change_song_metadata(tracks_to_update)

main()
