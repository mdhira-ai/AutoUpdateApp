import sys
import os
import requests
import subprocess

from tkinter import messagebox
from version import *


def check_for_updates():
    try:
        response = requests.get(REPO_URL, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            messagebox.showerror("Error", "Could not check for updates.")
            return

        data = response.json()
        latest_version = data["tag_name"].strip("v")
        
        if latest_version != CURRENT_VERSION:
            if messagebox.askyesno("Update Available", f"Version {latest_version} is available! Download now?"):
                download_and_install(data)
        else:
            messagebox.showinfo("Up to Date", "You are running the latest version.")
    except Exception as e:
        messagebox.showerror("Error", f"Update check failed: {e}")

def download_and_install(release_data):
    try:
        # Find the .exe asset
        download_url = None
        for asset in release_data.get("assets", []):
            if asset["name"].endswith(".exe"):
                download_url = asset["browser_download_url"]
                break
        
        if not download_url:
            messagebox.showerror("Error", "No installer executable found in the latest release.")
            return

        # Download installer
        installer_path = os.path.join(os.getenv("TEMP"), "mysetup_update.exe")
        response = requests.get(download_url, stream=True)
        with open(installer_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Run installer silently and close app
        # /VERYSILENT runs installer without windows
        # /CLOSEAPPLICATIONS closes your old app safely if specified in Inno
        # /RESTARTAPPLICATIONS reopens it post-install
        subprocess.Popen([installer_path, "/VERYSILENT", "/SUPPRESSMSGBOXES", "/CLOSEAPPLICATIONS", "/RESTARTAPPLICATIONS"])
        sys.exit(0)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to install update: {e}")
