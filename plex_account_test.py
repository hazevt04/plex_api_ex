#!/usr/bin/env python3

import uuid
import hashlib
import getpass

# Script for plex_account_test
from plexapi.myplex import MyPlexAccount

def get_correct_hash():
    f=open(".checkfile", "r")
    hashed_password_salt = f.read()
    return hashed_password_salt


def hash_password( password, salt ):
    return hashlib.sha512( salt.encode() + password.encode() ).hexdigest() + ':' + salt


def check_password( hashed_password, user_password ):
    password, salt = hashed_password.split(':')
    hashed_check_password = hashlib.sha512( salt.encode() + user_password.encode() ).hexdigest()
    return hashed_check_password == password


def prompt_user_info( hashed_correct_password_salt ):
    num_attempts = 0
    salt = hashed_correct_password_salt.split(":")[1]
    username = input("Username: ")
    while num_attempts < 2:
        trial_password = getpass.getpass()
        hashed_trial_password = hash_password( trial_password, salt )
        if check_password( hashed_correct_password_salt, trial_password ):
            return username, trial_password
        else:
            num_attempts += 1
    return username, ""


def plex_account_test( servername, username, password ):
    account = MyPlexAccount( username, password )
    # returns a PlexServer instance
    plex_server = account.resource(servername).connect()
    playlists = plex_server.playlists()
    for playlist in playlists:
        print("Playlist Title: {}".format( playlist.title ) )
        print("Playlist Items: {}".format( playlist.items ) )


if __name__ == '__main__':
    servername = "GlennimusMaximus"
   
    hashed_correct_password_salt = get_correct_hash()
    username, password = prompt_user_info( hashed_correct_password_salt )

    plex_account_test( servername, username, password )
    
