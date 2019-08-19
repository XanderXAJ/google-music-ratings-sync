# Ratings Sync for Google Play Music

Allows backing up and restoring ratings and play counts for Google Play Music accounts.

Written in Python 3 using [Unofficial Google Music API][gmusicapi].

[gmusicapi]: https://github.com/simon-weber/gmusicapi

## Installation

Clone this repository then install all requirements:

```bash
pipenv install
```

## Usage

Create a `.credentials` file in the same directory as the scripts containing the account's e-mail address, a generated app password, and [a valid `android_id` as specified by Unofficial Google Music API][android_id]:

```
[login]
email=valid.email@gmail.com
password=abcdefghijklmnop
android_id=1234567890abcdef
```

Once this is done, you can then run the script of your choosing.

[android_id]: http://unofficial-google-music-api.readthedocs.io/en/latest/reference/mobileclient.html#gmusicapi.clients.Mobileclient.login

## TODO

- `Mobileclient.rate_songs()` supports multiple rating multiple songs at once with a single rating. Therefore, bucket songs in to destination ratings (if an update is needed) to reduce the number of API calls required.
- Several things as a result of this being one of my early Python projects:
    - Add proper option parsing
    - Break down code in to smaller chunks
    - Add proper testing
    - Add proper logging with levels