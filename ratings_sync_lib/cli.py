"""Handles command line interface (CLI) rendering and interactions"""
import sys
from . import login as login_api

def login():
    """Log in to Google Play Music"""
    print('Logging in to Google Play Music')
    try:
        api = login_api.login_for_library_management()
    except RuntimeError as error:
        print(error)
        sys.exit(1)
    print('Logged in successfully')
    return api
