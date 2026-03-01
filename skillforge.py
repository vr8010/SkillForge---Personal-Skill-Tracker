"""
SkillForge - Personal Skill Tracker
A console-based skill management system using advanced OOP principles
"""

from abc import ABC, abstractmethod
from datetime import datetime
import json
import os
from typing import List, Dict, Optional


# ============================================================================
# ABSTRACT BASE CLASS - Abstraction
# ============================================================================

class SkillBase(ABC):
    """
    Abstract base class for all skill types.
    Demonstrates: Abstraction, Encapsulation
    """
    
    def __init__(self, name: str, category: str):
        self.__name = name  # Private attribute - Encapsulation
        self.__category = category
        self._progress = 0.0  # Protected attribute
        self._practice_hours = 0.0
        self._created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._last_updated = self._created_at
    
    # Getters - Encapsulation
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def category(self) -> str:
        return self.__category
    
    @property
    def progress(self) -> float:
        return self._progress
    
    @property
    def practice_hours(self) -> float:
        return self._practice_hours
    
    # Abstract methods - must be implemented by child classes
    @abstractmethod
    def calculate_mastery_score(self) -> float:
        """Calculate mastery score based on skill type"""
        pass
    
    @abstractmethod
    def get_skill_type(self) -> str:
        """Return the type of skill"""
        pass
    
    def update_progress(self, progress: float) -> None:
        """Update skill progress with validation"""
        if not 0 <= progress <= 100:
            raise ValueError("Progress must be between 0 and 100")
        self._progress = progress
        self._last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def log_practice_hours(self, hours: float) -> None:
        """Log practice hours with validation"""
        if hours < 0:
            raise ValueError("Practice hours cannot be negative")
        self._practice_hours += hours
        self._last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        """Convert skill object to dictionary for serialization"""
        return {
            'name': self.__name,
            'category': self.__category,
            'progress': self._progress,
            'practice_hours': self._practice_hours,
            'created_at': self._created_at,
            'last_updated': self._last_updated,
            'skill_type': self.get_skill_type()
        }
    
    def __str__(self) -> str:
        """String representation of skill"""
        mastery = self.calculate_mastery_score()
        return (f"{self.get_skill_type()}: {self.__name}\n"
                f"  Category: {self.__category}\n"
                f"  Progress: {self._progress}%\n"
                f"  Practice Hours: {self._practice_hours}h\n"
                f"  Mastery Score: {mastery:.2f}/100\n"
                f"  Last Updated: {self._last_updated}")


# ============================================================================
# CONCRETE CLASSES - Inheritance & Polymorphism
# ============================================================================

class TechnicalSkill(SkillBase):
    """
    Technical skill implementation with specific mastery calculation.
    Demonstrates: Inheritance, Polymorphism (method overriding)
    """
    
    def __init__(self, name: str, category: str, difficulty_level: int = 5):
        super().__init__(name, category)
        self.__difficulty_level = min(max(difficulty_level, 1), 10)  # 1-10 scale
    
    def calculate_mastery_score(self) -> float:
        """
        Technical skills mastery formula:
        Mastery = (Progress * 0.5) + (Practice_Hours * 0.3) + (Difficulty_Bonus * 0.2)
        Higher difficulty gives bonus points for same effort
        """
        difficulty_bonus = (self.__difficulty_level / 10) * 100
        practice_factor = min((self._practice_hours / 100) * 100, 100)
        
        mastery = (
            (self._progress * 0.5) +
            (practice_factor * 0.3) +
            (difficulty_bonus * 0.2)
        )
        return min(mastery, 100.0)
    
    def get_skill_type(self) -> str:
        return "Technical Skill"
    
    def to_dict(self) -> Dict:
        data = super().to_dict()
        data['difficulty_level'] = self.__difficulty_level
        return data
    
    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str}\n  Difficulty Level: {self.__difficulty_level}/10"


class SoftSkill(SkillBase):
    """
    Soft skill implementation with different mastery calculation.
    Demonstrates: Inheritance, Polymorphism (method overriding)
    """
    
    def __init__(self, name: str, category: str, real_world_applications: int = 0):
        super().__init__(name, category)
        self.__real_world_applications = max(real_world_applications, 0)
    
    def calculate_mastery_score(self) -> float:
        """
        Soft skills mastery formula:
        Mastery = (Progress * 0.4) + (Practice_Hours * 0.3) + (Applications * 0.3)
        Real-world applications are crucial for soft skills
        """
        practice_factor = min((self._practice_hours / 50) * 100, 100)
        application_factor = min((self.__real_world_applications / 20) * 100, 100)
        
        mastery = (
            (self._progress * 0.4) +
            (practice_factor * 0.3) +
            (application_factor * 0.3)
        )
        return min(mastery, 100.0)
    
    def get_skill_type(self) -> str:
        return "Soft Skill"
    
    def add_real_world_application(self) -> None:
        """Increment real-world application count"""
        self.__real_world_applications += 1
        self._last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        data = super().to_dict()
        data['real_world_applications'] = self.__real_world_applications
        return data
    
    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str}\n  Real-World Applications: {self.__real_world_applications}"


# ============================================================================
# MANAGER CLASS - Composition
# ============================================================================

class SkillForgeManager:
    """
    Manager class that uses composition to manage skill objects.
    Demonstrates: Composition, Exception Handling, File Handling
    """
    
    def __init__(self, storage_file: str = "skillforge_data.txt"):
        self.__skills: List[SkillBase] = []  # Composition - contains skill objects
        self.__storage_file = storage_file
        self.__load_skills()
    
    def add_technical_skill(self, name: str, category: str, difficulty: int) -> None:
        """Add a new technical skill"""
        if self.__skill_exists(name):
            raise ValueError(f"Skill '{name}' already exists!")
        
        skill = TechnicalSkill(name, category, difficulty)
        self.__skills.append(skill)
        print(f"✓ Technical skill '{name}' added successfully!")
    
    def add_soft_skill(self, name: str, category: str, applications: int = 0) -> None:
        """Add a new soft skill"""
        if self.__skill_exists(name):
            raise ValueError(f"Skill '{name}' already exists!")
        
        skill = SoftSkill(name, category, applications)
        self.__skills.append(skill)
        print(f"✓ Soft skill '{name}' added successfully!")
    
    def update_skill_progress(self, name: str, progress: float) -> None:
        """Update progress for a specific skill"""
        skill = self.__find_skill(name)
        if skill:
            skill.update_progress(progress)
            print(f"✓ Progress updated for '{name}'")
        else:
            raise ValueError(f"Skill '{name}' not found!")
    
    def log_practice_hours(self, name: str, hours: float) -> None:
        """Log practice hours for a specific skill"""
        skill = self.__find_skill(name)
        if skill:
            skill.log_practice_hours(hours)
            print(f"✓ Logged {hours} hours for '{name}'")
        else:
            raise ValueError(f"Skill '{name}' not found!")
    
    def add_soft_skill_application(self, name: str) -> None:
        """Add real-world application for soft skill"""
        skill = self.__find_skill(name)
        if skill and isinstance(skill, SoftSkill):
            skill.add_real_world_application()
            print(f"✓ Application logged for '{name}'")
        elif skill:
            raise TypeError(f"'{name}' is not a soft skill!")
        else:
            raise ValueError(f"Skill '{name}' not found!")
    
    def display_all_skills(self) -> None:
        """Display all skills with their details"""
        if not self.__skills:
            print("\n📭 No skills tracked yet. Start adding some!")
            return
        
        print("\n" + "="*70)
        print("🎯 YOUR SKILL PORTFOLIO")
        print("="*70)
        
        # Sort by mastery score
        sorted_skills = sorted(
            self.__skills,
            key=lambda s: s.calculate_mastery_score(),
            reverse=True
        )
        
        for idx, skill in enumerate(sorted_skills, 1):
            print(f"\n[{idx}] {skill}")
            print("-" * 70)
    
    def get_statistics(self) -> None:
        """Display overall statistics"""
        if not self.__skills:
            print("\n📊 No statistics available yet.")
            return
        
        total_skills = len(self.__skills)
        tech_skills = sum(1 for s in self.__skills if isinstance(s, TechnicalSkill))
        soft_skills = sum(1 for s in self.__skills if isinstance(s, SoftSkill))
        avg_mastery = sum(s.calculate_mastery_score() for s in self.__skills) / total_skills
        total_hours = sum(s.practice_hours for s in self.__skills)
        
        print("\n" + "="*70)
        print("📊 SKILLFORGE STATISTICS")
        print("="*70)
        print(f"Total Skills Tracked: {total_skills}")
        print(f"  ├─ Technical Skills: {tech_skills}")
        print(f"  └─ Soft Skills: {soft_skills}")
        print(f"Average Mastery Score: {avg_mastery:.2f}/100")
        print(f"Total Practice Hours: {total_hours:.1f}h")
        print("="*70)
    
    def save_skills(self) -> None:
        """Save all skills to file"""
        try:
            data = {
                'skills': [skill.to_dict() for skill in self.__skills],
                'last_saved': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            with open(self.__storage_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✓ Skills saved to '{self.__storage_file}'")
        except Exception as e:
            print(f"✗ Error saving skills: {e}")
    
    def __load_skills(self) -> None:
        """Load skills from file (private method)"""
        if not os.path.exists(self.__storage_file):
            return
        
        try:
            with open(self.__storage_file, 'r') as f:
                data = json.load(f)
            
            for skill_data in data.get('skills', []):
                skill_type = skill_data.get('skill_type')
                
                if skill_type == "Technical Skill":
                    skill = TechnicalSkill(
                        skill_data['name'],
                        skill_data['category'],
                        skill_data.get('difficulty_level', 5)
                    )
                elif skill_type == "Soft Skill":
                    skill = SoftSkill(
                        skill_data['name'],
                        skill_data['category'],
                        skill_data.get('real_world_applications', 0)
                    )
                else:
                    continue
                
                skill._progress = skill_data['progress']
                skill._practice_hours = skill_data['practice_hours']
                skill._created_at = skill_data['created_at']
                skill._last_updated = skill_data['last_updated']
                
                self.__skills.append(skill)
            
            print(f"✓ Loaded {len(self.__skills)} skills from storage")
        except Exception as e:
            print(f"⚠ Could not load previous data: {e}")
    
    def __skill_exists(self, name: str) -> bool:
        """Check if skill already exists (private method)"""
        return any(skill.name.lower() == name.lower() for skill in self.__skills)
    
    def __find_skill(self, name: str) -> Optional[SkillBase]:
        """Find skill by name (private method)"""
        for skill in self.__skills:
            if skill.name.lower() == name.lower():
                return skill
        return None
    
    def list_skill_names(self) -> List[str]:
        """Return list of all skill names"""
        return [skill.name for skill in self.__skills]


# ============================================================================
# USER INTERFACE - Clean Console Interaction
# ============================================================================


class SkillForgeUI:
    """
    User interface handler for console interaction.
    Demonstrates: Separation of concerns, Input validation
    """
    
    def __init__(self):
        self.manager = SkillForgeManager()
    
    def display_menu(self) -> None:
        """Display main menu"""
        print("\n" + "="*70)
        print("⚡ SKILLFORGE - Personal Skill Tracker")
        print("="*70)
        print("1. Add Technical Skill")
        print("2. Add Soft Skill")
        print("3. Update Skill Progress")
        print("4. Log Practice Hours")
        print("5. Log Soft Skill Application")
        print("6. View All Skills")
        print("7. View Statistics")
        print("8. Save & Exit")
        print("="*70)
    
    def get_choice(self) -> str:
        """Get user menu choice"""
        return input("Enter your choice (1-8): ").strip()
    
    def add_technical_skill_flow(self) -> None:
        """Flow for adding technical skill"""
        try:
            print("\n--- Add Technical Skill ---")
            name = input("Skill name: ").strip()
            if not name:
                raise ValueError("Skill name cannot be empty")
            
            category = input("Category (e.g., Programming, DevOps, Data Science): ").strip()
            if not category:
                raise ValueError("Category cannot be empty")
            
            difficulty = int(input("Difficulty level (1-10): ").strip())
            
            self.manager.add_technical_skill(name, category, difficulty)
        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
    
    def add_soft_skill_flow(self) -> None:
        """Flow for adding soft skill"""
        try:
            print("\n--- Add Soft Skill ---")
            name = input("Skill name: ").strip()
            if not name:
                raise ValueError("Skill name cannot be empty")
            
            category = input("Category (e.g., Communication, Leadership, Teamwork): ").strip()
            if not category:
                raise ValueError("Category cannot be empty")
            
            applications = int(input("Initial real-world applications (default 0): ").strip() or "0")
            
            self.manager.add_soft_skill(name, category, applications)
        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
    
    def update_progress_flow(self) -> None:
        """Flow for updating skill progress"""
        try:
            skills = self.manager.list_skill_names()
            if not skills:
                print("\n✗ No skills available. Add some first!")
                return
            
            print("\n--- Update Skill Progress ---")
            print("Available skills:", ", ".join(skills))
            name = input("Skill name: ").strip()
            progress = float(input("Progress percentage (0-100): ").strip())
            
            self.manager.update_skill_progress(name, progress)
        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
    
    def log_hours_flow(self) -> None:
        """Flow for logging practice hours"""
        try:
            skills = self.manager.list_skill_names()
            if not skills:
                print("\n✗ No skills available. Add some first!")
                return
            
            print("\n--- Log Practice Hours ---")
            print("Available skills:", ", ".join(skills))
            name = input("Skill name: ").strip()
            hours = float(input("Hours practiced: ").strip())
            
            self.manager.log_practice_hours(name, hours)
        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
    
    def log_application_flow(self) -> None:
        """Flow for logging soft skill application"""
        try:
            skills = self.manager.list_skill_names()
            if not skills:
                print("\n✗ No skills available. Add some first!")
                return
            
            print("\n--- Log Soft Skill Application ---")
            print("Available skills:", ", ".join(skills))
            name = input("Soft skill name: ").strip()
            
            self.manager.add_soft_skill_application(name)
        except (ValueError, TypeError) as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
    
    def run(self) -> None:
        """Main application loop"""
        print("\n🚀 Welcome to SkillForge!")
        print("Track, measure, and master your skills with precision.\n")
        
        while True:
            try:
                self.display_menu()
                choice = self.get_choice()
                
                if choice == '1':
                    self.add_technical_skill_flow()
                elif choice == '2':
                    self.add_soft_skill_flow()
                elif choice == '3':
                    self.update_progress_flow()
                elif choice == '4':
                    self.log_hours_flow()
                elif choice == '5':
                    self.log_application_flow()
                elif choice == '6':
                    self.manager.display_all_skills()
                elif choice == '7':
                    self.manager.get_statistics()
                elif choice == '8':
                    self.manager.save_skills()
                    print("\n👋 Thank you for using SkillForge! Keep growing!")
                    break
                else:
                    print("\n✗ Invalid choice. Please select 1-8.")
            
            except KeyboardInterrupt:
                print("\n\n⚠ Interrupted! Saving your progress...")
                self.manager.save_skills()
                print("👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n✗ Unexpected error: {e}")



# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    app = SkillForgeUI()
    app.run()

