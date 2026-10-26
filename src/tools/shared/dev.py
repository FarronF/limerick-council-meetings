"""Local live-reload server for the MkDocs and Pagefind site."""
import subprocess
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Resolve paths relative to repo root
ROOT_DIR = Path(__file__).resolve().parents[3]

def build():
    print("\n🔄 Rebuilding site & Pagefind index...")
    try:
        # 1. Compile static site
        subprocess.run(["mkdocs", "build"], check=True, cwd=ROOT_DIR)
        # 2. Build Pagefind index
        subprocess.run(["npx", "pagefind", "--site", "site"], check=True, cwd=ROOT_DIR)
        print("✅ Build complete! Refresh http://localhost:8000/search/\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build step failed: {e}\n")

class RebuildHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_rebuild = 0

    def on_modified(self, event):
        if event.src_path.endswith(('.md', '.py', '.yml', '.css', '.js')):
            now = time.time()
            if now - self.last_rebuild > 1.5:
                self.last_rebuild = now
                build()

if __name__ == "__main__":
    build()
    
    observer = Observer()
    observer.schedule(RebuildHandler(), path=str(ROOT_DIR / 'docs'), recursive=True)
    observer.schedule(RebuildHandler(), path=str(ROOT_DIR / 'src'), recursive=True)
    observer.start()

    print("🚀 Serving live site at http://localhost:8000/search/")
    try:
        subprocess.run(["python", "-m", "http.server", "8000", "--directory", "site"], cwd=ROOT_DIR)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()