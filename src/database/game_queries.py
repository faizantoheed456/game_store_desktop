from src.database.connection import DatabaseConnection

class GameQueries:
    @staticmethod
    def get_trending_games(limit=10):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM games WHERE is_trending = 1 ORDER BY rating DESC LIMIT ?", (limit,))
        return cursor.fetchall()

    @staticmethod
    def search_games(query):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        search_val = f'%{query}%'
        if query.lower() == "free":
            sql = "SELECT * FROM games WHERE price = 0.00 ORDER BY rating DESC"
            cursor.execute(sql)
        else:
            sql = """
                SELECT * FROM games 
                WHERE title LIKE ? OR genre LIKE ? OR platform LIKE ?
                ORDER BY is_trending DESC, rating DESC
            """
            cursor.execute(sql, (search_val, search_val, search_val))
        return cursor.fetchall()

    @staticmethod
    def get_games_by_genre(genre, limit=10):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM games WHERE genre = ? ORDER BY rating DESC LIMIT ?", (genre, limit))
        return cursor.fetchall()

    @staticmethod
    def add_sample_games():
        db = DatabaseConnection()
        cursor = db.get_cursor()
        
        # Check if games already exist
        cursor.execute("SELECT COUNT(*) FROM games")
        if cursor.fetchone()[0] > 0:
            return # Data already exists, skip
        
        # Format: Title, Genre, Price, Description, Local_Img, Year, Platform, Rating, Is_Trending, URL, Remote_Img
        games = [
            # --- TRENDING (Top 5) ---
            ("Cyberpunk 2077", "RPG", 59.99, "Night City.", "cp2077.jpg", 2020, "Steam", 4.5, 1, "https://store.steampowered.com/app/1091500/", "https://cdn.akamai.steamstatic.com/steam/apps/1091500/header.jpg"),
            ("Elden Ring", "Action", 59.99, "Lands Between.", "elden.jpg", 2022, "Steam", 4.9, 1, "https://store.steampowered.com/app/1245620/", "https://cdn.akamai.steamstatic.com/steam/apps/1245620/header.jpg"),
            ("Valorant", "FPS", 0.00, "Tactical Shooter.", "val.jpg", 2020, "Riot Games", 4.2, 1, "https://playvalorant.com/", "https://images2.alphacoders.com/106/thumb-1920-1060931.jpg"),
            ("God of War", "Action", 49.99, "Dad of War.", "gow.jpg", 2022, "Steam", 4.9, 1, "https://store.steampowered.com/app/1593500/", "https://cdn.akamai.steamstatic.com/steam/apps/1593500/header.jpg"),
            ("GTA V", "Action", 29.99, "Crime life.", "gtav.jpg", 2013, "Rockstar", 4.9, 1, "https://www.rockstargames.com/gta-v", "https://media-rockstargames-com.akamaized.net/rockstargames-newsite/img/global/games/fob/640/V.jpg"),

            # --- FPS (5+) ---
            ("Counter-Strike 2", "FPS", 0.00, "Classic shooter.", "cs2.jpg", 2023, "Steam", 4.8, 0, "https://store.steampowered.com/app/730/", "https://cdn.akamai.steamstatic.com/steam/apps/730/header.jpg"),
            ("Apex Legends", "FPS", 0.00, "Battle Royale.", "apex.jpg", 2019, "Steam", 4.3, 0, "https://store.steampowered.com/app/1172470/", "https://cdn.akamai.steamstatic.com/steam/apps/1172470/header.jpg"),
            ("Destiny 2", "FPS", 0.00, "Sci-fi MMO.", "destiny2.jpg", 2017, "Steam", 4.1, 0, "https://store.steampowered.com/app/1085660/", "https://cdn.akamai.steamstatic.com/steam/apps/1085660/header.jpg"),
            ("Doom Eternal", "FPS", 39.99, "Rip and tear.", "doom.jpg", 2020, "Steam", 4.8, 0, "https://store.steampowered.com/app/782330/", "https://cdn.akamai.steamstatic.com/steam/apps/782330/header.jpg"),
            ("Halo Infinite", "FPS", 59.99, "Master Chief.", "halo.jpg", 2021, "Steam", 4.1, 0, "https://store.steampowered.com/app/1240440/", "https://cdn.akamai.steamstatic.com/steam/apps/1240440/header.jpg"),
            ("Overwatch 2", "FPS", 0.00, "Hero shooter.", "ow2.jpg", 2022, "Battle.net", 3.5, 0, "https://overwatch.blizzard.com/", "https://images.igdb.com/igdb/image/upload/t_cover_big/co5908.jpg"),

            # --- HORROR & SURVIVAL (5+) ---
            ("Resident Evil 4", "Horror", 59.99, "Survival horror.", "re4.jpg", 2023, "Steam", 4.8, 0, "https://store.steampowered.com/app/2050650/", "https://cdn.akamai.steamstatic.com/steam/apps/2050650/header.jpg"),
            ("Dead Space", "Horror", 59.99, "Sci-fi horror.", "deadspace.jpg", 2023, "Steam", 4.7, 0, "https://store.steampowered.com/app/1693980/", "https://cdn.akamai.steamstatic.com/steam/apps/1693980/header.jpg"),
            ("Phasmophobia", "Horror", 13.99, "Ghost hunting.", "phasmo.jpg", 2020, "Steam", 4.6, 0, "https://store.steampowered.com/app/739630/", "https://cdn.akamai.steamstatic.com/steam/apps/739630/header.jpg"),
            ("Dying Light 2", "Horror", 59.99, "Stay Human.", "dyinglight2.jpg", 2022, "Steam", 4.3, 0, "https://store.steampowered.com/app/534380/", "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/534380/header.jpg"),
            ("Outlast Trials", "Horror", 39.99, "Coop horror.", "outlast.jpg", 2024, "Steam", 4.3, 0, "https://store.steampowered.com/app/1304930/", "https://cdn.akamai.steamstatic.com/steam/apps/1304930/header.jpg"),
            ("Amnesia: Bunker", "Horror", 24.99, "WWI Horror.", "amnesia.jpg", 2023, "Steam", 4.5, 0, "https://store.steampowered.com/app/1944430/", "https://cdn.akamai.steamstatic.com/steam/apps/1944430/header.jpg"),

            # --- STRATEGY & SIM (5+) ---
            ("Civilization VI", "Strategy", 59.99, "One more turn.", "civ6.jpg", 2016, "Steam", 4.6, 0, "https://store.steampowered.com/app/289070/", "https://cdn.akamai.steamstatic.com/steam/apps/289070/header.jpg"),
            ("Hearts of Iron IV", "Strategy", 39.99, "WWII Strategy.", "hoi4.jpg", 2016, "Steam", 4.5, 0, "https://store.steampowered.com/app/394360/", "https://cdn.akamai.steamstatic.com/steam/apps/394360/header.jpg"),
            ("Cities: Skylines", "Strategy", 29.99, "City builder.", "cities.jpg", 2015, "Steam", 4.7, 0, "https://store.steampowered.com/app/255710/", "https://cdn.akamai.steamstatic.com/steam/apps/255710/header.jpg"),
            ("Stellaris", "Strategy", 39.99, "Space strategy.", "stellaris.jpg", 2016, "Steam", 4.4, 0, "https://store.steampowered.com/app/281990/", "https://cdn.akamai.steamstatic.com/steam/apps/281990/header.jpg"),
            ("Manor Lords", "Strategy", 39.99, "Medieval sim.", "manor.jpg", 2024, "Steam", 4.8, 0, "https://store.steampowered.com/app/1363080/", "https://cdn.akamai.steamstatic.com/steam/apps/1363080/header.jpg"),
            ("Frostpunk 2", "Strategy", 44.99, "Frozen survival.", "frostpunk.jpg", 2024, "Steam", 4.7, 0, "https://store.steampowered.com/app/1601580/", "https://cdn.akamai.steamstatic.com/steam/apps/1601580/header.jpg"),

            # --- RACING & SPORTS (5+) ---
            ("Forza Horizon 5", "Racing", 59.99, "Mexico festival.", "forza5.jpg", 2021, "Steam", 4.7, 0, "https://store.steampowered.com/app/1551360/", "https://cdn.akamai.steamstatic.com/steam/apps/1551360/header.jpg"),
            ("F1 24", "Racing", 69.99, "Formula 1.", "f124.jpg", 2024, "Steam", 3.8, 0, "https://store.steampowered.com/app/2488620/", "https://cdn.akamai.steamstatic.com/steam/apps/2488620/header.jpg"),
            ("Assetto Corsa", "Racing", 19.99, "Real sim racing.", "ac.jpg", 2014, "Steam", 4.9, 0, "https://store.steampowered.com/app/244210/", "https://cdn.akamai.steamstatic.com/steam/apps/244210/header.jpg"),
            ("FC 24", "Racing", 69.99, "Football.", "fc24.jpg", 2023, "Steam", 3.2, 0, "https://store.steampowered.com/app/2195250/", "https://cdn.akamai.steamstatic.com/steam/apps/2195250/header.jpg"),
            ("Gran Turismo 7", "Racing", 69.99, "The real sim.", "gt7.jpg", 2022, "PS5", 4.8, 0, "https://www.playstation.com/games/gran-turismo-7/", "https://images.igdb.com/igdb/image/upload/t_cover_big/co4968.jpg"),
            ("Dirt 5", "Racing", 59.99, "Off-road racing.", "dirt5.jpg", 2020, "Steam", 4.0, 0, "https://store.steampowered.com/app/1038250/", "https://cdn.akamai.steamstatic.com/steam/apps/1038250/header.jpg"),

            # --- INDIE (5+) ---
            ("Hades", "Indie", 24.99, "Roguelike.", "hades.jpg", 2020, "Steam", 4.9, 0, "https://store.steampowered.com/app/1145360/", "https://cdn.akamai.steamstatic.com/steam/apps/1145360/header.jpg"),
            ("Hollow Knight", "Indie", 14.99, "Metroidvania.", "hollow.jpg", 2017, "Steam", 4.9, 0, "https://store.steampowered.com/app/367520/", "https://cdn.akamai.steamstatic.com/steam/apps/367520/header.jpg"),
            ("Stardew Valley", "Indie", 14.99, "Farm life.", "stardew.jpg", 2016, "Steam", 4.9, 0, "https://store.steampowered.com/app/294100/", "https://cdn.akamai.steamstatic.com/steam/apps/294100/header.jpg"),
            ("Lethal Company", "Indie", 9.99, "Coop scrap.", "lethal.jpg", 2023, "Steam", 4.8, 0, "https://store.steampowered.com/app/1966720/", "https://cdn.akamai.steamstatic.com/steam/apps/1966720/header.jpg"),
            ("Palworld", "Indie", 29.99, "Monster survival.", "palworld.jpg", 2024, "Steam", 4.5, 0, "https://store.steampowered.com/app/1623730/", "https://cdn.akamai.steamstatic.com/steam/apps/1623730/header.jpg"),
            ("Cult of the Lamb", "Indie", 24.99, "Unclean cult.", "lamb.jpg", 2022, "Steam", 4.8, 0, "https://store.steampowered.com/app/1313140/", "https://cdn.akamai.steamstatic.com/steam/apps/1313140/header.jpg")
        ]
        
        cursor.executemany(
            "INSERT INTO games (title, genre, price, description, cover_image, release_year, platform, rating, is_trending, website_url, remote_image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            games
        )
        db.commit()

    @staticmethod
    def get_collection_status(user_id, game_id):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("SELECT is_favorite, is_installed FROM user_library WHERE user_id = ? AND game_id = ?", (user_id, game_id))
        result = cursor.fetchone()
        return result if result else (0, 0)

    @staticmethod
    def update_collection_status(user_id, game_id, is_favorite, is_installed):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        try:
            if not is_favorite and not is_installed:
                cursor.execute("DELETE FROM user_library WHERE user_id = ? AND game_id = ?", (user_id, game_id))
            else:
                cursor.execute("""
                    INSERT INTO user_library (user_id, game_id, is_favorite, is_installed)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(user_id, game_id) DO UPDATE SET
                    is_favorite = excluded.is_favorite,
                    is_installed = excluded.is_installed
                """, (user_id, game_id, is_favorite, is_installed))
            db.commit()
            return True
        except Exception as e:
            print(f"Error updating collection status: {e}")
            return False

    @staticmethod
    def get_user_favorites(user_id):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("""
            SELECT g.* FROM games g
            JOIN user_library ul ON g.id = ul.game_id
            WHERE ul.user_id = ? AND ul.is_favorite = 1
            ORDER BY ul.added_date DESC
        """, (user_id,))
        return cursor.fetchall()

    @staticmethod
    def get_user_installed(user_id):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("""
            SELECT g.* FROM games g
            JOIN user_library ul ON g.id = ul.game_id
            WHERE ul.user_id = ? AND ul.is_installed = 1
            ORDER BY ul.added_date DESC
        """, (user_id,))
        return cursor.fetchall()

    @staticmethod
    def get_user_library(user_id):
        """Returns all games in user's collection (either favorite or installed)"""
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("""
            SELECT g.* FROM games g
            JOIN user_library ul ON g.id = ul.game_id
            WHERE ul.user_id = ?
            ORDER BY ul.added_date DESC
        """, (user_id,))
        return cursor.fetchall()

    @staticmethod
    def get_user_stats(user_id):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM user_library ul
            JOIN games g ON ul.game_id = g.id
            WHERE ul.user_id = ? AND ul.is_favorite = 1
        """, (user_id,))
        fav_count = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM user_library ul
            JOIN games g ON ul.game_id = g.id
            WHERE ul.user_id = ? AND ul.is_installed = 1
        """, (user_id,))
        installed_count = cursor.fetchone()[0]
        
        return {
            "wishlist": fav_count,
            "installed": installed_count
        }

    @staticmethod
    def get_all_games():
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM games")
        return cursor.fetchall()

    @staticmethod
    def delete_game(game_id):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        try:
            # Delete from libraries first
            cursor.execute("DELETE FROM user_library WHERE game_id = ?", (game_id,))
            cursor.execute("DELETE FROM games WHERE id = ?", (game_id,))
            db.commit()
            return True
        except Exception as e:
            print(f"Error deleting game: {e}")
            return False
