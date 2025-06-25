import main as pyspotui_actions

class home:
    titel = "Startpage"
    exittext = "Zie je later!"
    currentlyplaying = "Currently playing"
    noSesion = "No playback session found. Please start a playback session first."
    lijstStartText = "Wat wil je doen?"
    askForInputText = "Kies een optie: "
    playlist = "Playlists"
    artists = "Artists"

class artists_menu:
    header = "Artists"
    lijstStartText = "Kies de artiest die je wilt bekijken of afspelen:"
    askForInputText = "Kies een artiest: "

class artist_submenu:
    moreInfo = False
    header = "$name"
    lijstStartText = "Wat wil je doen?"
    askForInputText = "Kies een optie: "

class playlist_menu:
    header = "Playlists"
    lijstStartText = "Welk lied wil je spelen?"
    askForInputText = "Kies een lied: "

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
    search = 'zoeken'
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

class search_menu:
    askForQueryText = 'Enter your search query: '
    header = 'Search'
    songs = 'Songs'
    albums = 'Albums'
    artists = 'Artists'
    playlists = 'Playlists'
    lijstStartText = 'Hoe wil je zoeken?'
    askForInputText = 'Kies een optie: '

class search:
    askForInputText = 'Enter your search query: '
    header = 'Search results for: $query'
    no_results = 'No results found for: $query'
    lijstStartText = 'Dit hebben we gevonden: '
    askForInputText = 'Kies iets: '

welkome = "Welcome to Spotify Warper! This is a command line interface for Spotify. Enjoy your stay!"


keybinds = [
    {'combo': 'h', 'action': 'startpage'},
    {'combo': 'c', 'action': 'currently_playing'},
    {'combo': 'p', 'action': 'playlists'},
    {'combo': 'a', 'action': 'artists'},
    {'combo': 'q', 'action': 'exit'},
    {'combo': 's', 'action': 'search'},
    {'combo': 'st', 'action': 'search_songs'},
    # {'combo': 'sa', 'action': 'search_albums'},
    # {'combo': 'se', 'action': 'search_artists'},
    {'combo': 'sp', 'action': 'search_playlists'},
]