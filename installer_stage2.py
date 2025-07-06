import os
from helpers import UI, clear

clear()
print("""
██████╗ ██╗   ██╗███████╗██████╗  ██████╗ ████████╗██╗   ██╗██╗
██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝██║   ██║██║
██████╔╝ ╚████╔╝ ███████╗██████╔╝██║   ██║   ██║   ██║   ██║██║
██╔═══╝   ╚██╔╝  ╚════██║██╔═══╝ ██║   ██║   ██║   ██║   ██║██║
██║        ██║   ███████║██║     ╚██████╔╝   ██║   ╚██████╔╝██║
╚═╝        ╚═╝   ╚══════╝╚═╝      ╚═════╝    ╚═╝    ╚═════╝ ╚═╝
""")

def copy_to_config():
    """Copies the script to ~/.config/pyspotui/ and adds it to PATH."""
    config_dir = os.path.expanduser("~/.config/pyspotui/")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    script_path = os.path.abspath(__file__)
    
    # Files to copy
    files_to_copy = ['config.py', 'helpers.py', 'main.py', 'spotify_warper.py', 'pyspotui']
    script_dir = os.path.dirname(script_path)
    
    for file in files_to_copy:
        source_path = os.path.join(script_dir, file)
        if os.path.exists(source_path):
            dest_path = os.path.join(config_dir, file)
            with open(source_path, 'r') as src, open(dest_path, 'w') as dst:
                dst.write(src.read())
            print(f"Copied {file} to {config_dir}")

            # Make pyspotui executable
            if file == 'pyspotui':
                os.chmod(dest_path, 0o755)  # rwxr-xr-x permissions
                print(f"Made {file} executable.")

def add_to_path():
    """Adds ~/.config/pyspotui/ to PATH for various shells."""
    config_dir = os.path.expanduser("~/.config/pyspotui/")
    
    # Detect shell
    shell = os.environ.get('SHELL', '')
    
    if 'zsh' in shell:
        path_file = os.path.expanduser("~/.zshrc")
    elif 'bash' in shell:
        path_file = os.path.expanduser("~/.bashrc")
    elif 'fish' in shell:
        path_file = os.path.expanduser("~/.config/fish/config.fish")
        with open(path_file, 'a') as f:
            f.write(f'\nset -gx PATH $PATH {config_dir}\n')
            print(f"Added {config_dir} to PATH in {path_file}.")
            print(f"Please restart your terminal or run 'source {path_file}' to apply changes.")
        return
    else:
        # Default to .profile for unknown shells
        path_file = os.path.expanduser("~/.profile")
        print(f"Unknown shell detected. Adding to {path_file}. If this doesn't work, please add {config_dir} to your PATH manually.")
    
    # For bash, zsh, and others that use export syntax
    with open(path_file, 'a') as f:
        f.write(f'\nexport PATH="$PATH:{config_dir}"\n')
    
    print(f"Added {config_dir} to PATH in {path_file}.")
    print(f"Please restart your terminal or run 'source {path_file}' to apply changes.")

def askForCreds():
    """Asks for Spotify credentials and saves them to SECRETS.py."""
    client_id = input("Enter your Spotify Client ID: ").strip()
    client_secret = input("Enter your Spotify Client Secret: ").strip()
    redirect_uri = input("Enter your Spotify Redirect URI: ").strip()
    # Ensure config directory exists
    config_dir = os.path.expanduser("~/.config/pyspotui/")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    # Create SECRETS.py file
    secrets_path = os.path.join(config_dir, "SECRETS.py")
    with open(secrets_path, 'w') as f:
        f.write(f"""# Spotify API Credentials
CLIENT_ID = '{client_id}'
CLIENT_SECRET = '{client_secret}'
REDIRECT_URI = '{redirect_uri}'
""")
    print(f"Credentials saved to {secrets_path}")

def pip_install_and_venv():
    """Installs required packages in a virtual environment."""
    config_dir = os.path.expanduser("~/.config/pyspotui/")
    os.system(f"python3 -m venv {config_dir}pyspotui_venv")
    venv_pip = f"{config_dir}pyspotui_venv/bin/pip"
    requirements = [
        "rich",
        "spotipy",
        "requests",
    ]
    for package in requirements:
        os.system(f"{venv_pip} install {package}")
def install():
    """Installs the script by copying files and setting up the environment."""
    copy_to_config()
    askForCreds()
    pip_install_and_venv()
    add_to_path()
    print("Installation complete! You can now run the script using 'pyspotui' command. after restarting your terminal or sourcing your shell configuration file.")

def update():
    copy_to_config()
    pip_install_and_venv()
    print("Update complete! Please restart your terminal")

options = [
    {
        "name": "Install to ~/.config/pyspotui/ and add to PATH",
        "function": lambda: install(),
    },
    {
        "name": "uninstall from ~/.config/pyspotui/",
        "function": lambda: (print("Uninstalling..."), os.system("rm -rf ~/.config/pyspotui/"), print("Uninstallation complete.")),
    },
    {
        "name": "Update to latest version",
        "function": lambda: update(),
    },
    {
        "name": "Exit",
        "function": lambda: print("Exiting..."),
    },
]

ui = UI(menu_options=options, hotkeys=[], startText="Welcome to the Installer!", askForInputText="Please select an option: ") 
ui.display_menu()
ui.get_user_choice_and_run()