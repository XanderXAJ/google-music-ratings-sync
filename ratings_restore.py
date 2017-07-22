#!/usr/bin/env python3
"""Restore ratings and play counts from a backup of a Google Play Music account

A backup can be performed by running ratings_backup.py.
"""
import sys
from gmusicapi import Mobileclient
import ratings_sync_lib.cli as cli

def main():
    """Executes the restoration"""

    # Check we have at least one argument (the ratings file name).
    # Remember that the script name is one of the arguments, so we expect argv to
    # have two items.
    if len(sys.argv) <= 1:
        print('Argument missing.  Provide path to ratings backup.')
        sys.exit(1)

    ratings_file_name = sys.argv[1]

    # We have a valid ratings file, parse it
    ratings_file = open(ratings_file_name, mode='r', encoding='utf-8')
    tracks_to_rate = []

    for line in ratings_file:
        # The ratings file is expected to be a list of dictionaries, with one track
        # (and thus dictionary) per line.

        # Create the dictionary
        track = eval(line)

        # If the track is missing any data, discard it
        # Only one of playCount or rating is required
        if not ('title' in track and 'artist' in track and 'album' in track and ('rating' in track or ('playCount' in track and track['playCount'] > 0))):
            continue

        tracks_to_rate.append(track)

    ratings_file.close()
    print('Parsed', len(tracks_to_rate), 'tracks with ratings from backup')

    api = cli.login()

    # Get all tracks
    print('Getting library')
    gm_library = api.get_all_songs()
    print('Library retrieved:', len(gm_library), "tracks received")


    # For each track in ratings file, apply its rating and/or playCount

    # Keep a note of what happens to each track (for reporting)
    tracks_updated = []
    tracks_no_matches = []
    tracks_multiple_matches = []
    tracks_no_change_needed = []

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
            tracks_no_matches.append(ra_track)
            continue

        # If there is more than one track, skip
        if len(matched_tracks) > 1:
            match_info = {'track_to_match': ra_track, 'matched_tracks': matched_tracks}
            tracks_multiple_matches.append(match_info)
            continue

        # There is only one matching track, set the rating and or playCount
        track_changed = False

        matched_track = matched_tracks[0]

        # Update the rating, if needed
        if 'rating' in ra_track and matched_track['rating'] != ra_track['rating']:
            matched_track['rating'] = ra_track['rating']
            api.change_song_metadata(matched_track)
            track_changed = True

        # Update the play count, if needed
        if 'playCount' in ra_track and ra_track['playCount'] > 0:
            # We don't set the play count, rather we add plays.
            # That means we need the difference between the current play count
            # and the target play count, then we add that.
            play_count_difference = ra_track['playCount'] - matched_track['playCount']

        if play_count_difference > 0:
            api.increment_song_playcount(matched_track['id'], plays=play_count_difference)
            track_changed = True

        if track_changed:
            tracks_updated.append(matched_track)
        else:
            tracks_no_change_needed.append(matched_track)
            continue


    # print(out info about unmatched tracks)
    if len(tracks_no_matches) > 0:
        print('Tracks with no matches:')
        for track in tracks_no_matches:
            print(str(track))

    if len(tracks_multiple_matches) > 0:
        print('Tracks with multiple matches (therefore making update ambiguous):')
        for match_info in tracks_multiple_matches:
            print('Track:', str(match_info['track_to_match']))
        for match in match_info['matched_tracks']:
            print('Match:', str(match))
            print('')

    # Update all tracks on Google Play Music
    print('Updated', len(tracks_updated), 'tracks on Google Play Music')

main()
