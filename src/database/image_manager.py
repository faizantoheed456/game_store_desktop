import os
import requests
import threading
from PIL import Image
import customtkinter as ctk

class ImageManager:
    _cache = {}
    _lock = threading.Lock()

    @staticmethod
    def preload_images(games):
        """Triggers downloads for a list of games in parallel."""
        for game in games:
            # game[11] is remote_url, game[5] is local_name
            threading.Thread(target=ImageManager.get_image, 
                             args=(game[11], game[5]), 
                             daemon=True).start()

    @staticmethod
    def get_image(url, filename, size=(300, 170), callback=None):
        """
        Returns an image if cached/local, otherwise downloads in a background 
        thread and executes a callback when ready.
        """
        filepath = os.path.join("assets", filename)
        
        # 1. Check Memory Cache
        if filename in ImageManager._cache:
            return ImageManager._cache[filename]

        # 2. Check Local Disk
        if os.path.exists(filepath):
            try:
                img = ImageManager._load_and_cache(filepath, filename, size)
                return img
            except Exception:
                pass

        # 3. Download Asynchronously
        if url:
            threading.Thread(target=ImageManager._async_download, 
                             args=(url, filepath, filename, size, callback), 
                             daemon=True).start()
        
        return None # Return None while loading

    @staticmethod
    def _load_and_cache(filepath, filename, size):
        pil_img = Image.open(filepath)
        ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=size)
        with ImageManager._lock:
            ImageManager._cache[filename] = ctk_img
        return ctk_img

    @staticmethod
    def _async_download(url, filepath, filename, size, callback):
        try:
            if not os.path.exists("assets"):
                os.makedirs("assets")
            
            # Use a slightly more robust download approach
            headers = {'User-Agent': 'Mozilla/5.0'}
            
            try:
                response = requests.get(url, headers=headers, timeout=10)
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                # Fallback URL if Steam CDN is blocked/down
                if "steamstatic.com" in url:
                    fallback_url = url.replace("cdn.akamai.steamstatic.com", "shared.fastly.steamstatic.com")
                    response = requests.get(fallback_url, headers=headers, timeout=10)
                else:
                    raise

            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                ctk_img = ImageManager._load_and_cache(filepath, filename, size)
                if callback:
                    callback(ctk_img)
        except Exception:
            # Silently fail for a better UX, or log to a file instead of console
            pass
