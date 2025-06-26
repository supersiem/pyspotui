import rich
import spotify_warper as spotifylib
import SECRETS
from helpers import UI, clear, header, log, hotkey_action_function_matcher
import config as conf
import requests
import os
from pathlib import Path

def startpage(firstRun=False):
    if not firstRun:
        clear()
        header(conf.home.titel)
    playing = playback.get_current_playback()
    if playing:
        options = [
            {'name': conf.home.currentlyplaying, 'function': playback_menu},
            {'name': conf.home.playlist, 'function': playlist_menu},
            {'name':conf.home.artists, 'function': artists_menu},
            {'name': conf.generic.search, 'function': search_menu},
            {'name': "exit", 'function': lambda: (clear(), print(conf.home.exittext), exit(0))},
        ]
        startpage_menu = UI(options, REALhotkeys,conf.home.lijstStartText, conf.home.askForInputText)
        startpage_menu.display_menu()
        startpage_menu.get_user_choice_and_run()
    else:
        rich.print(
            conf.home.noSesion
        )

def search_menu():
    clear()
    header(conf.search_menu.header)
    search_options = [
        {'name': conf.generic.back, 'function': startpage},
        {'name': conf.search_menu.songs, 'function': lambda: search_songs(query=input(conf.search.askForInputText))},
        {'name': conf.search_menu.playlists, 'function': lambda: search_playlists(query=input(conf.search.askForInputText))},
    ]

    search_menu_ui = UI(search_options, REALhotkeys, conf.search_menu.lijstStartText, conf.search_menu.askForQueryText)
    search_menu_ui.display_menu()
    search_menu_ui.get_user_choice_and_run()

def search_songs(query):
    clear()
    header(conf.search.header.replace('$query', query))
    options = [
        {'name': conf.generic.back, 'function': search_menu},
    ]
    results = search.search_songs(query)
    log(results)
    if results and 'tracks' in results and results['tracks']['items']:
        for track in results['tracks']['items']:
            options.append({
                'name': f"{track['name']} - {', '.join(artist['name'] for artist in track['artists'])}",
                'function': lambda t=track: (playback.add_to_queue(t['uri']), playback_menu())
            })

        search_menu_ui = UI(options, REALhotkeys, conf.search.lijstStartText, conf.search.askForInputText)
        search_menu_ui.display_menu()
        search_menu_ui.get_user_choice_and_run()
    else:
        rich.print(conf.search.no_results)

def search_playlists(query):
    clear()
    header(conf.search.header.replace('$query', query))
    options = [
        {'name': conf.generic.back, 'function': search_menu},
    ]
    results = search.search_playlists(query)
    log(results)
    if results and 'playlists' in results and results['playlists']['items']:
        for playlist in results['playlists']['items']:
            if playlist and 'name' in playlist and 'uri' in playlist:  # Check if playlist is not None and has required fields
                options.append({
                    'name': playlist['name'],
                    'function': lambda p=playlist: (playlist_submenu(p['uri'], isFromSearch=True))
                })

        search_menu_ui = UI(options, REALhotkeys, conf.search.lijstStartText, conf.search.askForInputText)
        search_menu_ui.display_menu()
        search_menu_ui.get_user_choice_and_run()
    else:
        rich.print(conf.search.no_results)


def playlist_menu():
    clear()
    header(conf.playlist_menu.header)
    playlists = library.user_playlists()
    playlistAsOptions = [
        {'name':conf.generic.back, 'function': startpage},
    ]
    log(playlists['items'])
    if playlists and 'items' in playlists:
        for playlist in playlists['items']:
            playlistAsOptions.append({
                'name': playlist['name'],
                'function': lambda p=playlist: (playlist_submenu(p['uri']))
            })
    else:
        rich.print("No playlists found.")

    playlist_menu_ui = UI(playlistAsOptions,REALhotkeys, conf.playlist_menu.lijstStartText, conf.playlist_menu.askForInputText)
    playlist_menu_ui.display_menu()
    playlist_menu_ui.get_user_choice_and_run()

def playlist_submenu(uri, isFromSearch=False):
    clear()
    playlist = library.get_playlist(uri)
    header(playlist['name'])
    options = [
        {'name': conf.generic.play, 'function': lambda: (playback.play_playlist(uri), playback_menu())},
        {'name': conf.playlist_submenu.view, 'function': lambda: (view_playlist_tracks(uri, isFromSearch), playlist_menu())},
    ]
    if not isFromSearch:
        options.append({'name': conf.generic.back, 'function': playlist_menu})
    else:
        options.append({'name': conf.home.titel, 'function': lambda: (startpage())})
    playlistUI = UI(options,REALhotkeys, conf.playlist_submenu.lijstStartText, conf.playlist_submenu.askForInputText)
    playlistUI.display_menu()
    playlistUI.get_user_choice_and_run()

def view_playlist_tracks(playlist_id, isFromSearch=False):
    clear()
    playlist = library.get_playlist(playlist_id)
    header(conf.playlist_tracks.header.replace('%name', playlist['name']))
    options = [
        {'name': 'placeholder A', 'function': showplaylistOption(playlist, isFromSearch)}
    ]
    playlistUI = UI(options,REALhotkeys, conf.playlist_tracks.lijstStartText, conf.playlist_tracks.askForInputText)
    playlistUI.display_menu()
    playlistUI.get_user_choice_and_run()

def showplaylistOption(playlist, isFromSearch=False):
    clear()
    header(playlist['name'])
    rich.print(f"Owner: {playlist['owner']['display_name']}")
    rich.print(f"Description: {playlist['description']}")
    rich.print(f"Total tracks: {playlist['tracks']['total']}")
    options = [
        {'name': conf.generic.back, 'function': lambda: (playlist_submenu(playlist['uri'], isFromSearch))},
    ]
    for track in playlist['tracks']['items']:
        options.append({
            'name': f"{track['track']['name']} - {', '.join(artist['name'] for artist in track['track']['artists'])}",
            'function': lambda t=track: (playback.add_to_queue(t['track']['uri']), playback_menu())
        })

    showplaylistOptionUI = UI(options,REALhotkeys)
    showplaylistOptionUI.display_menu()
    showplaylistOptionUI.get_user_choice_and_run()


def playback_menu():
    clear()
    header(conf.playback_menu.header)
    playing = playback.get_current_playback()
    # Create cache directory if it doesn't exist
    cache_dir = Path.home() / '.config' / 'pyspotui'
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Get album art URL and cache it
    if playing and playing['item'] and playing['item']['album']['images']:
        album_id = playing['item']['album']['id']
        cache_file = cache_dir / f"{album_id}.jpg"

        if not cache_file.exists():
            # Download and cache the image
            images = playing['item']['album']['images']
            image_url = images[0]['url']
            try:
                response = requests.get(image_url)
                response.raise_for_status()
                with open(cache_file, 'wb') as f:
                    f.write(response.content)
            except requests.RequestException as e:
                log(f"Failed to download album art: {e}")
                rich.print("Failed to download album art.")
        else:
            os.system('timg ' + str(cache_file) if cache_file.exists() else '')

    # Display album art if available
    output = conf.playback_menu.text.replace('$name', playing['item']['name']).replace('$artists', ', '.join(artist['name'] for artist in playing['item']['artists'])).replace('$album', playing['item']['album']['name']).replace('$duration', str(playing['item']['duration_ms'] // 1000))
    rich.print(output)

    # TODO_ fix queue viewing and add volume control
    options = [
        {'name': "<==", 'function': lambda: (playback.skip_to_previous(), playback_menu())},
        {'name': "==>", 'function': lambda: (playback.skip_to_next(), playback_menu())},
        {'name': "play/pause", 'function': lambda: (playback.play_pause(), playback_menu())},
        # {'name': 'queue', 'function': lambda: (printQueue(), playback_menu())},
        # {'name': "set volume", 'function': lambda: set_volume_menu()},
        # {'name': "add to queue", 'function': lambda: add_to_queue_menu()},
        {'name': conf.generic.refresh, 'function': lambda: (playback_menu())},
        {'name': conf.generic.back, 'function': startpage},
    ]
    playback_menu_ui = UI(options, REALhotkeys)
    rich.print('1: <==  2: ==>')
    log(playing)
    if playing and not playing['is_playing']:
        rich.print(conf.generic.notPlaying)  # Play icon when not playing
    elif playing:
        rich.print(conf.generic.playing)  # Pause icon when playing
    rich.print('4: refresh')
    rich.print('5: terug')
    # playback_menu_ui.display_menu()
    playback_menu_ui.get_user_choice_and_run()

def artists_menu():
    clear()
    header(conf.artists_menu.header)
    artists = library.saved_artists()
    artistAsOptions = [
        {'name': conf.generic.back, 'function': startpage},
    ]
    if artists and 'artists' in artists:
        for artist in artists['artists']['items']:
            artistAsOptions.append({
                'name': artist['name'],
                'function': lambda a=artist: (artist_submenu(a['uri']))
            })

    artist_menu_ui = UI(artistAsOptions, REALhotkeys, conf.artists_menu.lijstStartText, conf.artists_menu.askForInputText)
    artist_menu_ui.display_menu()
    artist_menu_ui.get_user_choice_and_run()

def artist_submenu(artist_id):
    clear()
    artist = library.get_artist(artist_id)
    artistTT = library.get_artist_top_tracks(uri=artist_id)
    log('ARTIST START. '+str(artist))
    header(conf.artist_submenu.header.replace('$name', artist['name']))
    if conf.artist_submenu.moreInfo:
        rich.print(f"Followers: {artist['followers']['total']}")
        rich.print(f"Genres: {', '.join(artist['genres'])}")
        rich.print(f"Popularity: {artist['popularity']}")
    options = [
        {'name': conf.generic.back, 'function': artists_menu},
    ]
    if artistTT and 'tracks' in artistTT:
        for track in artistTT['tracks']:
            options.append({
                'name': f"{track['name']} - {', '.join(artist['name'] for artist in track['artists'])}",
                'function': lambda t=track: (playback.add_to_queue(t['uri']), playback_menu())
            })
    else:
        rich.print("No top tracks found for this artist.")

    artist_submenu_ui = UI(options, REALhotkeys, conf.artist_submenu.lijstStartText, conf.artist_submenu.askForInputText)
    artist_submenu_ui.display_menu()
    artist_submenu_ui.get_user_choice_and_run()

if __name__ == "__main__":
    clear()
    rich.print("Loading...")
    spotify = spotifylib.SpotifyWarper(SECRETS.CLIENT_ID, SECRETS.CLIENT_SECRET, SECRETS.REDIRECT_URI); playback = spotify.Playback(spotify); library = spotify.Library(spotify); search = spotify.search(spotify)
    REALhotkeys = hotkey_action_function_matcher(conf.keybinds, actions=[
        {'name': 'startpage', 'function': startpage},
        {'name': 'playlists', 'function': playlist_menu},
        {'name': 'currently_playing', 'function': playback_menu},
        {'name': 'artists', 'function': artists_menu},
        {'name': 'search', 'function': search_menu},
        {'name': 'search_songs', 'function': lambda: search_songs(query=input(conf.search_menu.askForQueryText))},
        # {'name': 'search_albums', 'function': lambda: search_albums(query=input(conf.search_menu.askForQueryText))},
        # {'name': 'search_artists', 'function': lambda: search_artists(query=input(conf.search_menu.askForQueryText))},
        {'name': 'search_playlists', 'function': lambda: search_playlists(query=input(conf.search_menu.askForQueryText))},
        {'name': 'exit', 'function': lambda: (clear(), print(conf.home.exittext), exit(0))}
    ])
    clear()
    rich.print(
        conf.welkome
    )
    startpage(True)
