"""Handles logins to Google Play Music
"""
import configparser
from gmusicapi import Mobileclient

CREDENTIALS_FILE = '.credentials'

def login_for_library_management():
    """Logs in to Google Play Music using the .credentials file"""

    config = configparser.ConfigParser()
    config.read(CREDENTIALS_FILE)

    email = config['login']['email']
    password = config['login']['password']
    device_id = config['login']['device_id']

    api = Mobileclient()
    if not api.login(email, password, device_id):
        raise RuntimeError('Failed to login')

    return api
