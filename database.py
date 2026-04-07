"""
Database module for SkillForge - PostgreSQL Integration
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Optional
import json
from datetime import datetime


class Database:
    """PostgreSQL database handler for SkillForge"""
    
    def __init__(self):
        self.conn = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            # Get database URL from environment variable (Render provides this)
            database_url = os.environ.get('DATABASE_URL')
            
            if database_url:
                # Render uses postgres:// but psycopg2 needs postgresql://
                if database_url.startswith('postgres://'):
                    database_url = database_url.replace('postgres://', 'postgresql://', 1)
                
                self.conn = psycopg2.connect(database_url)
                print("✓ Connected to PostgreSQL database")
            else:
                # Fallback to JSON file if no database URL
                print("⚠ No DATABASE_URL found, using JSON file storage")
                self.conn = None
        except Exception as e:
            print(f"⚠ Database connection failed: {e}")
            print("  Using JSON file storage as fallback")
            self.conn = None
    
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        if not self.conn:
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Skills table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) UNIQUE NOT NULL,
                    category VARCHAR(255) NOT NULL,
                    skill_type VARCHAR(50) NOT NULL,
                    progress FLOAT DEFAULT 0,
                    practice_hours FLOAT DEFAULT 0,
                    difficulty_level INTEGER,
                    real_world_applications INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # History table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skill_history (
                    id SERIAL PRIMARY KEY,
                    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    action VARCHAR(100) NOT NULL,
                    description TEXT,
                    details JSONB
                )
            """)
            
            self.conn.commit()
            cursor.close()
            print("✓ Database tables ready")
        except Exception as e:
            print(f"✗ Error creating tables: {e}")
            self.conn.rollback()
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self.conn is not None
    
    def get_all_skills(self) -> List[Dict]:
        """Get all skills from database"""
        if not self.conn:
            return []
        
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT * FROM skills ORDER BY last_updated DESC
            """)
            skills = cursor.fetchall()
            cursor.close()
            return [dict(skill) for skill in skills]
        except Exception as e:
            print(f"✗ Error fetching skills: {e}")
            return []
    
    def add_skill(self, skill_data: Dict) -> bool:
        """Add a new skill to database"""
        if not self.conn:
            return False
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO skills 
                (name, category, skill_type, progress, practice_hours, 
                 difficulty_level, real_world_applications)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                skill_data['name'],
                skill_data['category'],
                skill_data['skill_type'],
                skill_data.get('progress', 0),
                skill_data.get('practice_hours', 0),
                skill_data.get('difficulty_level'),
                skill_data.get('real_world_applications')
            ))
            
            skill_id = cursor.fetchone()[0]
            
            # Add creation history entry
            cursor.execute("""
                INSERT INTO skill_history (skill_id, action, description, details)
                VALUES (%s, %s, %s, %s)
            """, (
                skill_id,
                'created',
                'Skill created',
                json.dumps({'initial_progress': 0, 'initial_hours': 0})
            ))
            
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"✗ Error adding skill: {e}")
            self.conn.rollback()
            return False
    
    def update_skill_progress(self, name: str, progress: float) -> bool:
        """Update skill progress"""
        if not self.conn:
            return False
        
        try:
            cursor = self.conn.cursor()
            
            # Get current progress
            cursor.execute("SELECT id, progress FROM skills WHERE name = %s", (name,))
            result = cursor.fetchone()
            if not result:
                return False
            
            skill_id, old_progress = result
            
            # Update progress
            cursor.execute("""
                UPDATE skills 
                SET progress = %s, last_updated = CURRENT_TIMESTAMP
                WHERE name = %s
            """, (progress, name))
            
            # Add history entry
            cursor.execute("""
                INSERT INTO skill_history (skill_id, action, description, details)
                VALUES (%s, %s, %s, %s)
            """, (
                skill_id,
                'progress_update',
                'Progress updated',
                json.dumps({
                    'old_progress': old_progress,
                    'new_progress': progress,
                    'progress_change': progress - old_progress
                })
            ))
            
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"✗ Error updating progress: {e}")
            self.conn.rollback()
            return False
    
    def log_practice_hours(self, name: str, hours: float) -> bool:
        """Log practice hours"""
        if not self.conn:
            return False
        
        try:
            cursor = self.conn.cursor()
            
            # Get current hours
            cursor.execute("SELECT id, practice_hours FROM skills WHERE name = %s", (name,))
            result = cursor.fetchone()
            if not result:
                return False
            
            skill_id, old_hours = result
            new_hours = old_hours + hours
            
            # Update hours
            cursor.execute("""
                UPDATE skills 
                SET practice_hours = %s, last_updated = CURRENT_TIMESTAMP
                WHERE name = %s
            """, (new_hours, name))
            
            # Add history entry
            cursor.execute("""
                INSERT INTO skill_history (skill_id, action, description, details)
                VALUES (%s, %s, %s, %s)
            """, (
                skill_id,
                'practice_logged',
                f'Logged {hours}h of practice',
                json.dumps({
                    'hours_added': hours,
                    'old_total_hours': old_hours,
                    'new_total_hours': new_hours
                })
            ))
            
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"✗ Error logging hours: {e}")
            self.conn.rollback()
            return False
    
    def add_application(self, name: str) -> bool:
        """Add real-world application for soft skill"""
        if not self.conn:
            return False
        
        try:
            cursor = self.conn.cursor()
            
            # Get current applications
            cursor.execute("""
                SELECT id, real_world_applications 
                FROM skills 
                WHERE name = %s AND skill_type = 'soft'
            """, (name,))
            result = cursor.fetchone()
            if not result:
                return False
            
            skill_id, old_apps = result
            new_apps = (old_apps or 0) + 1
            
            # Update applications
            cursor.execute("""
                UPDATE skills 
                SET real_world_applications = %s, last_updated = CURRENT_TIMESTAMP
                WHERE name = %s
            """, (new_apps, name))
            
            # Add history entry
            cursor.execute("""
                INSERT INTO skill_history (skill_id, action, description, details)
                VALUES (%s, %s, %s, %s)
            """, (
                skill_id,
                'application_logged',
                'Real-world application added',
                json.dumps({
                    'old_applications': old_apps or 0,
                    'new_applications': new_apps
                })
            ))
            
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"✗ Error adding application: {e}")
            self.conn.rollback()
            return False
    
    def get_skill_history(self, name: str) -> List[Dict]:
        """Get history for a specific skill"""
        if not self.conn:
            return []
        
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT h.timestamp, h.action, h.description, h.details
                FROM skill_history h
                JOIN skills s ON h.skill_id = s.id
                WHERE s.name = %s
                ORDER BY h.timestamp DESC
            """, (name,))
            history = cursor.fetchall()
            cursor.close()
            
            # Convert to list of dicts with formatted timestamp
            return [{
                'timestamp': h['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
                'action': h['action'],
                'description': h['description'],
                'details': h['details']
            } for h in history]
        except Exception as e:
            print(f"✗ Error fetching history: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✓ Database connection closed")
