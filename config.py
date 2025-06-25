import main as pyspotui_actions

# NOT WORKING CORRECTLY!!! DO NOT USE YET
spotifyd_using_brew = False # KEEP DISABLED FOR NOW, IT IS NOT WORKING CORRECTLY

class home:
    titel = "Startpage"
    exittext = "Zie je later!"
    noSesion = "No playback session found. Please start a playback session first."
    lijstStartText = "Wat wil je doen?"
    askForInputText = "Kies een optie: "

class playlist_menu:
    header = "Playlists"
    lijstStartText = "Wat wil je doen?"
    askForInputText = "Kies een optie: "

class playlist_submenu:
    header = "Playlist opties"
    lijstStartText = "Wat wil je doen?"
    askForInputText = "Kies een optie: "
    view = "view"

class playlist_tracks:
    header = "%name"
    lijstStartText = ""
    askForInputText = "Kies een optie: "

class playback_menu:
    header = "Currently playing"
    lijstStartText = "Wat wil je doen?"
    askForInputText = "Kies een optie: "
    text = '$name \n[white]$artists[/white]'
    order = [
        'text',
        'albumArt',
        'progress'
    ]


class generic:
    header = "please add a header to this page from the config file"
    startText = 'Choose an option:'
    askForInputText = "Enter your choice: "
    back = 'terug'
    play = 'play'
    skip_next = "skip next"
    skip_previous = "skip previous"
    pause = "pause"
    resume = "resume"
    volume = "volume"
    queue = "queue"
    refresh = "refresh"
    notPlaying = "3: play"
    playing = "3: pause"

welkome = "Welcome to Spotify Warper! This is a command line interface for Spotify. Enjoy your stay!"


keybinds = [
    {'combo': 'h', 'action': 'startpage'},
    {'combo': 'c', 'action': 'currently_playing'},
    {'combo': 'p', 'action': 'playlists'},
]