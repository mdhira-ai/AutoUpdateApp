import os
import sys
import platform
import subprocess
import requests
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox
from PySide6.QtCore import QThread, Signal

CURRENT_VERSION = "1.0.2"
GITHUB_REPO = "mdhira-ai/qtapp"

class UpdateCheckerThread(QThread):
    update_available = Signal(str, str)  # version, download_url
    no_update = Signal()

    def run(self):
        try:
            # Query GitHub Releases API
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                latest_version = data["tag_name"].strip("v")
                
                # Simple semantic version check
                if latest_version != CURRENT_VERSION:
                    system = platform.system().lower()
                    download_url = None
                    
                    # Match appropriate asset format per OS
                    for asset in data.get("assets", []):
                        name = asset["name"].lower()
                        if system == "windows" and "mysetup.exe" in name:
                            download_url = asset["browser_download_url"]
                        elif system == "darwin" and (".dmg" in name or ".pkg" in name or "mac" in name):
                            download_url = asset["browser_download_url"]
                        elif system == "linux" and ("appimage" in name or "linux" in name):
                            download_url = asset["browser_download_url"]
                    
                    if download_url:
                        self.update_available.emit(latest_version, download_url)
                        return
            self.no_update.emit()
        except Exception:
            self.no_update.emit()

class DownloaderThread(QThread):
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url, stream=True, timeout=15)
            total_size = int(response.headers.get('content-length', 0))
            
            # Determine filename and platform-specific temp path
            filename = self.url.split("/")[-1]
            temp_dir = os.environ.get("TMPDIR") or os.environ.get("TEMP") or "/tmp"
            local_path = os.path.join(temp_dir, filename)
            
            downloaded = 0
            with open(local_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            self.progress.emit(int((downloaded / total_size) * 100))
            
            self.finished.emit(local_path)
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cross-Platform Qt App")
        self.resize(300, 150)

        layout = QVBoxLayout()
        self.lbl_version = QLabel(f"Current Version: {CURRENT_VERSION}")
        self.btn_update = QPushButton("Check for Updates")
        self.btn_update.clicked.connect(self.check_for_updates)

        layout.addWidget(self.lbl_version)
        layout.addWidget(self.btn_update)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def check_for_updates(self):
        self.btn_update.setEnabled(False)
        self.btn_update.setText("Checking...")
        self.checker = UpdateCheckerThread()
        self.checker.update_available.connect(self.prompt_update)
        self.checker.no_update.connect(self.up_to_date)
        self.checker.start()

    def up_to_date(self):
        self.btn_update.setEnabled(True)
        self.btn_update.setText("Check for Updates")
        QMessageBox.information(self, "No Updates", "You are running the latest version.")

    def prompt_update(self, version, url):
        self.btn_update.setEnabled(True)
        self.btn_update.setText("Check for Updates")
        reply = QMessageBox.question(
            self, "Update Available", 
            f"Version {version} is available. Download and install now?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.download_update(url)

    def download_update(self, url):
        self.btn_update.setEnabled(False)
        self.btn_update.setText("Downloading 0%...")
        self.downloader = DownloaderThread(url)
        self.downloader.progress.connect(lambda p: self.btn_update.setText(f"Downloading {p}%..."))
        self.downloader.error.connect(self.download_failed)
        self.downloader.finished.connect(self.apply_update)
        self.downloader.start()

    def download_failed(self, err):
        self.btn_update.setEnabled(True)
        self.btn_update.setText("Check for Updates")
        QMessageBox.critical(self, "Error", f"Download failed: {err}")

    def apply_update(self, path):
        self.btn_update.setText("Applying update...")
        system = platform.system().lower()
        
        if system == "windows":
            # Run Inno Setup silently
            subprocess.Popen([path, "/VERYSILENT", "/CLOSEAPPLICATIONS"])
            
        elif system == "darwin":  # macOS
            # If using a .pkg payload file, run installer via AppleScript prompt
            if path.endswith(".pkg"):
                script = f'do shell script "installer -pkg {path} -target /" with administrator privileges'
                subprocess.Popen(["osascript", "-e", script])
            # If using a raw binary app container zip/tar, a script handles swapout
            
        elif system == "linux":
            # Make downloaded AppImage executable and launch it to replace this process
            os.chmod(path, 0o755)
            subprocess.Popen([path])
            
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
