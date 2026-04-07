"""Database module for SkillForge - SQLite Integration"""
import sqlite3
from typing import List, Dict
import json


class Database:
    def __init__(self, db_path: str = "skillforge.db"):
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            print(f"✓ Connected to SQLite: {self.db_path}")
        except Exception as e:
            print(f"⚠ DB connection failed: {e}")
            self.conn = None
    
    def create_tables(self):
        if not self.conn:
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    category TEXT NOT NULL,
                    skill_type TEXT NOT NULL,
                    progress REAL DEFAULT 0,
                    practice_hours REAL DEFAULT 0,
                    difficulty_level INTEGER,
                    real_world_applications INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skill_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_id INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    action TEXT NOT NULL,
                    description TEXT,
                    details TEXT,
                    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
                )
            """)
            self.conn.commit()
            cursor.close()
            print("✓ Tables ready")
        except Exception as e:
            print(f"✗ Error creating tables: {e}")
            self.conn.rollback()
    
    def is_connected(self) -> bool:
        return self.conn is not None
    
    def get_all_skills(self) -> List[Dict]:
        if not self.conn:
            return []
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM skills ORDER BY last_updated DESC")
            skills = cursor.fetchall()
            cursor.close()
            return [dict(skill) for skill in skills]
        except Exception as e:
            print(f"✗ Error fetching skills: {e}")
            return []
    
    def add_skill(self, skill_data: Dict) -> bool:
        if not self.conn:
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO skills 
                (name, category, skill_type, progress, practice_hours, 
                 difficulty_level, real_world_applications)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                skill_data['name'], skill_data['category'], skill_data['skill_type'],
                skill_data.get('progress', 0), skill_data.get('practice_hours', 0),
                skill_data.get('difficulty_level'), skill_data.get('real_world_applications')
            ))
            skill_id = cursor.lastrowid
            cursor.execute("""
                INSERT INTO skill_history (skill_id, action, description, details)
                VALUES (?, ?, ?, ?)
            """, (skill_id, 'created', 'Skill created',
                  json.dumps({'initial_progress': 0, 'initial_hours': 0})))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"✗ Error adding skill: {e}")
            self.conn.rollback()
            return False
    
    def update_skill_progress(self, name: str, progress: float) -> bool:
        if not self.conn:
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, progress FROM skills WHERE name = ?", (name,))
            result = cursor.fetchone()
            if not result:
                return False
            skill_id, old_progress = result['id'], result['progress']
            cursor.execute("UPDATE skills SET progress = ?, last_updated = CURRENT_TIMESTAMP WHERE name = ?",
                         (progress, name))
            cursor.execute("INSERT INTO skill_history (skill_id, action, description, details) VALUES (?, ?, ?, ?)",
                         (skill_id, 'progress_update', 'Progress updated',
                          json.dumps({'old_progress': old_progress, 'new_progress': progress,
                                    'progress_change': progress - old_progress})))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"✗ Error updating progress: {e}")
            self.conn.rollback()
            return False
    
    def log_practice_hours(self, name: str, hours: float) -> bool:
        if not self.conn:
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, practice_hours FROM skills WHERE name = ?", (name,))
            result = cursor.fetchone()
            if not result:
                return False
            skill_id, old_hours = result['id'], result['practice_hours']
            new_hours = old_hours + hours
            cursor.execute("UPDATE skills SET practice_hours = ?, last_updated = CURRENT_TIMESTAMP WHERE name = ?",
                         (new_hours, name))
            cursor.execute("INSERT INTO skill_history (skill_id, action, description, details) VALUES (?, ?, ?, ?)",
                         (skill_id, 'practice_logged', f'Logged {hours}h of practice',
                          json.dumps({'hours_added': hours, 'old_total_hours': old_hours,
                                    'new_total_hours': new_hours})))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"✗ Error logging hours: {e}")
            self.conn.rollback()
            return False
    
    def add_application(self, name: str) -> bool:
        if not self.conn:
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, real_world_applications FROM skills WHERE name = ? AND skill_type = 'soft'",
                         (name,))
            result = cursor.fetchone()
            if not result:
                return False
            skill_id, old_apps = result['id'], result['real_world_applications']
            new_apps = (old_apps or 0) + 1
            cursor.execute("UPDATE skills SET real_world_applications = ?, last_updated = CURRENT_TIMESTAMP WHERE name = ?",
                         (new_apps, name))
            cursor.execute("INSERT INTO skill_history (skill_id, action, description, details) VALUES (?, ?, ?, ?)",
                         (skill_id, 'application_logged', 'Real-world application added',
                          json.dumps({'old_applications': old_apps or 0, 'new_applications': new_apps})))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"✗ Error adding application: {e}")
            self.conn.rollback()
            return False
    
    def get_skill_history(self, name: str) -> List[Dict]:
        if not self.conn:
            return []
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT h.timestamp, h.action, h.description, h.details
                FROM skill_history h JOIN skills s ON h.skill_id = s.id
                WHERE s.name = ? ORDER BY h.timestamp DESC
            """, (name,))
            history = cursor.fetchall()
            cursor.close()
            return [{'timestamp': h['timestamp'], 'action': h['action'],
                    'description': h['description'],
                    'details': json.loads(h['details']) if h['details'] else {}}
                   for h in history]
        except Exception as e:
            print(f"✗ Error fetching history: {e}")
            return []
    
    def close(self):
        if self.conn:
            self.conn.close()
            print("✓ DB connection closed")
