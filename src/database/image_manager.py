import os
import requests
from PIL import Image
import customtkinter as ctk
from concurrent.futures import ThreadPoolExecutor

class ImageManager:
    _cache = {}
    _executor = ThreadPoolExecutor(max_workers=4)

    @staticmethod
    def preload_images(games):
        """Triggers downloads for a list of games in parallel using a thread pool."""
        for game in games:
            # game[11] is remote_url, game[5] is local_name
            ImageManager._executor.submit(ImageManager.get_image, game[11], game[5])

    @staticmethod
    def get_image(url, filename, size=(300, 170), callback=None, master=None):
        """
        Returns an image if cached. Otherwise, loads from disk or downloads 
        in a background thread and executes a callback when ready.
        Thread-safe: Uses master.after if master is provided.
        """
        filepath = os.path.join("assets", filename)
        
        # 1. Check Memory Cache
        if filename in ImageManager._cache:
            return ImageManager._cache[filename]

        # 2. Asynchronous Loading (Disk or Download)
        ImageManager._executor.submit(ImageManager._load_task, url, filepath, filename, size, callback, master)
        return None 

    @staticmethod
    def _load_task(url, filepath, filename, size, callback, master):
        try:
            # Check Local Disk
            if os.path.exists(filepath):
                ImageManager._load_and_cache(filepath, filename, size, callback, master)
                return

            # Download if not on disk
            if url:
                ImageManager._async_download(url, filepath, filename, size, callback, master)
        except Exception:
            pass

    @staticmethod
    def _load_and_cache(filepath, filename, size, callback=None, master=None):
        try:
            pil_img = Image.open(filepath)
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=size)
            ImageManager._cache[filename] = ctk_img
            
            if callback:
                if master:
                    master.after(0, lambda: callback(ctk_img))
                else:
                    callback(ctk_img) # Fallback if no master provided
            return ctk_img
        except Exception:
            return None

    @staticmethod
    def _async_download(url, filepath, filename, size, callback, master):
        try:
            if not os.path.exists("assets"):
                os.makedirs("assets")
            
            headers = {'User-Agent': 'Mozilla/5.0'}
            try:
                response = requests.get(url, headers=headers, timeout=10)
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                if "steamstatic.com" in url:
                    fallback_url = url.replace("cdn.akamai.steamstatic.com", "shared.fastly.steamstatic.com")
                    response = requests.get(fallback_url, headers=headers, timeout=10)
                else:
                    raise

            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                ImageManager._load_and_cache(filepath, filename, size, callback, master)
        except Exception:
            pass
