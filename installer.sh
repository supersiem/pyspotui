echo "Making Python virtual environment for the installer..."
python3 -m venv installer_venv
source installer_venv/bin/activate
pip install rich
python installer_stage2.py