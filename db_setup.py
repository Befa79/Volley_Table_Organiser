import sqlite3

connection = sqlite3.connect("tournaments.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tournaments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    teams INTEGER,
    fields INTEGER,
    start_time TEXT,
    end_time TEXT,
    tournament_type TEXT,
    game_mode TEXT
)
""")

connection.commit()
connection.close()

print("Database and table created.")
