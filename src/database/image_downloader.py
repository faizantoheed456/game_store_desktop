import os
import requests

class ImageDownloader:
    @staticmethod
    def download_image(url, filename):
        """Downloads an image from a URL and saves it to the assets folder."""
        if not os.path.exists("assets"):
            os.makedirs("assets")
            
        filepath = os.path.join("assets", filename)
        
        # If file already exists, don't download again
        if os.path.exists(filepath):
            return filepath
            
        try:
            print(f"Downloading image for {filename}...")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return filepath
        except Exception as e:
            print(f"Failed to download {filename}: {e}")
            
        return None
