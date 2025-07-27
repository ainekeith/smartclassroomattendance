import sqlite3
from datetime import datetime
from pathlib import Path


class DatabaseService:
    def __init__(self, db_path='attendance.db'):
        self.db_path = Path(__file__).parent.parent / db_path
        self._init_db()
        
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS attendance
                    (id INTEGER PRIMARY KEY,
                     student_id TEXT,
                     timestamp REAL,
                     image_path TEXT,
                     emotion TEXT)''')
        conn.commit()
        conn.close()
        
    def get_daily_stats(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Get today's date string
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Count today's attendance
        c.execute(
            ("SELECT COUNT(*) FROM attendance "
             "WHERE date(timestamp, 'unixepoch') = ?"),
            (today,)
        )
        count = c.fetchone()[0]
        
        # Get latest entry
        c.execute("SELECT * FROM attendance ORDER BY timestamp DESC LIMIT 1")
        latest = c.fetchone()
        
        conn.close()
        
        return {
            'total_today': count,
            'latest_entry': latest
        }