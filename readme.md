# Pyspotui

A Spotify terminal user interface written in Python.

## demo

If you want to try it, run demo.sh. This will create a venv, install dependencies, ask for credentials, and run the TUI. This will only work if you have Python installed. I have only tested this on macOS. Make sure you have a spotify premium account, and a active spotify client running.

## Installation

Run the installer script to set up Pyspotui and its dependencies. The installer will create a virtual environment, copy necessary files to the configuration directory, and set up the environment for you to use Pyspotui:

```bash
bash installer.sh
```

or if you use a different you can replace the `bash` with your shell of choice, like `zsh` or `fish`.

## Usage

After installation, you can run Pyspotui by executing the following command:

```bash
pyspotui
```

## Requirements

- Python idk what versions work but I have tested it with Python 3.9
- pip (Python package installer)
- Spotify premium account (not tested with free accounts)
- A terminal
- A web browser (for the initial Spotify authentication)
- A Spotify client ID and secret (you can get these by registering your application on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications))

## configauration

You can configure Pyspotui by editing the `config.py` file in the `~/.config/pyspotui/` directory. Its very specific to your needs, so you can change the settings to your liking. The default settings should work for most users.

## Contributing

If you want to contribute to Pyspotui, feel free to open an issue or a pull request. Contributions are welcome!

## License

I forgot so unlicensed

## Disclaimer

bad code

## Roadmap

- [ ] full read and playback support for Spotify
- [X] Add support for searching for songs, albums, and artists
- [ ] Write to Spotify playlists
- [ ] Intagrate spotifyd to play music without the need for a Spotify client
- [ ] MORE CONFIGURATION OPTIONS. 119 LINES OF CONFIG IS NOT ENOUGH!!!
- [ ] Document `config.py`
  
bye!
