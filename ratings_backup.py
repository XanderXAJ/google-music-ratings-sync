#!/usr/bin/env python3
"""Back up ratings and play counts for a Google Play Music account"""
import ratings_sync_lib.cli as cli


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
        repr(track) for track in library if
        ('rating' in track and track['rating'] != '0')
        or ('playCount' in track and track['playCount'] > 0)
    ]

    # Output tracks
    ratings_file_name = 'downloaded_ratings.txt'
    ratings_file = open(ratings_file_name, mode='w', encoding='utf-8')

    ratings_file.write('\n'.join(rated_tracks))

    ratings_file.close()

    print(len(rated_tracks), "rated/listened tracks found, written to", ratings_file_name)


main()
