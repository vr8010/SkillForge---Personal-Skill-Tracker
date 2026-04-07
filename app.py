"""
SkillForge Web API - Flask Backend
Provides REST API endpoints for the web frontend
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from skillforge import SkillForgeManager, TechnicalSkill, SoftSkill, MasteryAlgorithm
from database_sqlite import Database
import os

app = Flask(__name__, static_folder='static', static_url_path='')

# Configure CORS for production
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],  # Update with your Vercel domain in production
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize database and manager
db = Database()
manager = SkillForgeManager('skillforge_data.json')

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get all skills"""
    try:
        # Try database first, fallback to JSON
        if db.is_connected():
            db_skills = db.get_all_skills()
            skills_data = []
            
            for skill_dict in db_skills:
                # Calculate mastery score
                if skill_dict['skill_type'] == 'technical':
                    mastery = MasteryAlgorithm.difficulty_adjusted(
                        skill_dict['progress'],
                        skill_dict['practice_hours'],
                        skill_dict.get('difficulty_level', 5)
                    )
                else:
                    mastery = MasteryAlgorithm.application_focused(
                        skill_dict['progress'],
                        skill_dict['practice_hours'],
                        skill_dict.get('real_world_applications', 0)
                    )
                
                skill_dict['mastery_score'] = mastery
                skill_dict['mastery_level'] = MasteryAlgorithm.get_mastery_level(mastery)
                skill_dict['skill_type'] = 'Technical Skill' if skill_dict['skill_type'] == 'technical' else 'Soft Skill'
                
                # Convert datetime to string
                if 'created_at' in skill_dict:
                    skill_dict['created_at'] = skill_dict['created_at'].strftime("%Y-%m-%d %H:%M:%S")
                if 'last_updated' in skill_dict:
                    skill_dict['last_updated'] = skill_dict['last_updated'].strftime("%Y-%m-%d %H:%M:%S")
                
                skills_data.append(skill_dict)
        else:
            # Fallback to JSON file
            skills_data = []
            for skill in manager._SkillForgeManager__skills:
                skill_dict = skill.to_dict()
                skill_dict['mastery_score'] = skill.calculate_mastery_score()
                skill_dict['mastery_level'] = MasteryAlgorithm.get_mastery_level(
                    skill_dict['mastery_score']
                )
                skill_dict['mastery_breakdown'] = skill.get_mastery_breakdown()
                skills_data.append(skill_dict)
        
        # Sort by mastery score
        skills_data.sort(key=lambda x: x['mastery_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'skills': skills_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/skills', methods=['POST'])
def add_skill():
    """Add a new skill"""
    try:
        data = request.json
        skill_type = data.get('skill_type')
        name = data.get('name')
        category = data.get('category')
        
        skill_data = {
            'name': name,
            'category': category,
            'skill_type': skill_type,
            'progress': 0,
            'practice_hours': 0
        }
        
        if skill_type == 'technical':
            difficulty = int(data.get('difficulty', 5))
            skill_data['difficulty_level'] = difficulty
            skill_data['real_world_applications'] = None
            
            # Add to database if connected
            if db.is_connected():
                db.add_skill(skill_data)
            else:
                manager.add_technical_skill(name, category, difficulty)
                manager.save_skills()
        elif skill_type == 'soft':
            applications = int(data.get('applications', 0))
            skill_data['real_world_applications'] = applications
            skill_data['difficulty_level'] = None
            
            # Add to database if connected
            if db.is_connected():
                db.add_skill(skill_data)
            else:
                manager.add_soft_skill(name, category, applications)
                manager.save_skills()
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid skill type'
            }), 400
        
        return jsonify({
            'success': True,
            'message': f'Skill "{name}" added successfully'
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/skills/<skill_name>/progress', methods=['PUT'])
def update_progress(skill_name):
    """Update skill progress"""
    try:
        data = request.json
        progress = float(data.get('progress'))
        
        # Update in database if connected
        if db.is_connected():
            success = db.update_skill_progress(skill_name, progress)
            if not success:
                return jsonify({
                    'success': False,
                    'error': f'Skill "{skill_name}" not found'
                }), 404
        else:
            manager.update_skill_progress(skill_name, progress)
            manager.save_skills()
        
        return jsonify({
            'success': True,
            'message': f'Progress updated for "{skill_name}"'
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/skills/<skill_name>/hours', methods=['PUT'])
def log_hours(skill_name):
    """Log practice hours"""
    try:
        data = request.json
        hours = float(data.get('hours'))
        
        # Update in database if connected
        if db.is_connected():
            success = db.log_practice_hours(skill_name, hours)
            if not success:
                return jsonify({
                    'success': False,
                    'error': f'Skill "{skill_name}" not found'
                }), 404
        else:
            manager.log_practice_hours(skill_name, hours)
            manager.save_skills()
        
        return jsonify({
            'success': True,
            'message': f'Logged {hours} hours for "{skill_name}"'
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/skills/<skill_name>/application', methods=['POST'])
def add_application(skill_name):
    """Add real-world application for soft skill"""
    try:
        # Update in database if connected
        if db.is_connected():
            success = db.add_application(skill_name)
            if not success:
                return jsonify({
                    'success': False,
                    'error': f'Soft skill "{skill_name}" not found'
                }), 404
        else:
            manager.add_soft_skill_application(skill_name)
            manager.save_skills()
        
        return jsonify({
            'success': True,
            'message': f'Application logged for "{skill_name}"'
        })
    except (ValueError, TypeError) as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/skills/<skill_name>/history', methods=['GET'])
def get_history(skill_name):
    """Get skill history"""
    try:
        # Get from database if connected
        if db.is_connected():
            history = db.get_skill_history(skill_name)
        else:
            skill = manager._SkillForgeManager__find_skill(skill_name)
            if not skill:
                return jsonify({
                    'success': False,
                    'error': f'Skill "{skill_name}" not found'
                }), 404
            history = skill.history
        
        return jsonify({
            'success': True,
            'history': history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get overall statistics"""
    try:
        # Get from database if connected
        if db.is_connected():
            db_skills = db.get_all_skills()
            
            if not db_skills:
                return jsonify({
                    'success': True,
                    'statistics': {
                        'total_skills': 0,
                        'technical_skills': 0,
                        'soft_skills': 0,
                        'average_mastery': 0,
                        'total_hours': 0
                    }
                })
            
            total_skills = len(db_skills)
            tech_skills = sum(1 for s in db_skills if s['skill_type'] == 'technical')
            soft_skills = sum(1 for s in db_skills if s['skill_type'] == 'soft')
            
            # Calculate average mastery
            total_mastery = 0
            for skill in db_skills:
                if skill['skill_type'] == 'technical':
                    mastery = MasteryAlgorithm.difficulty_adjusted(
                        skill['progress'],
                        skill['practice_hours'],
                        skill.get('difficulty_level', 5)
                    )
                else:
                    mastery = MasteryAlgorithm.application_focused(
                        skill['progress'],
                        skill['practice_hours'],
                        skill.get('real_world_applications', 0)
                    )
                total_mastery += mastery
            
            avg_mastery = total_mastery / total_skills
            total_hours = sum(s['practice_hours'] for s in db_skills)
        else:
            # Fallback to JSON file
            skills = manager._SkillForgeManager__skills
            
            if not skills:
                return jsonify({
                    'success': True,
                    'statistics': {
                        'total_skills': 0,
                        'technical_skills': 0,
                        'soft_skills': 0,
                        'average_mastery': 0,
                        'total_hours': 0
                    }
                })
            
            total_skills = len(skills)
            tech_skills = sum(1 for s in skills if isinstance(s, TechnicalSkill))
            soft_skills = sum(1 for s in skills if isinstance(s, SoftSkill))
            avg_mastery = sum(s.calculate_mastery_score() for s in skills) / total_skills
            total_hours = sum(s.practice_hours for s in skills)
        
        return jsonify({
            'success': True,
            'statistics': {
                'total_skills': total_skills,
                'technical_skills': tech_skills,
                'soft_skills': soft_skills,
                'average_mastery': round(avg_mastery, 2),
                'total_hours': round(total_hours, 1)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    # Get port from environment variable (for deployment platforms)
    port = int(os.environ.get('PORT', 5000))
    
    print("🚀 SkillForge Web Server Starting...")
    print(f"📱 Open http://localhost:{port} in your browser")
    print("⚡ Press Ctrl+C to stop the server")
    
    # Use 0.0.0.0 to allow external connections
    app.run(debug=False, host='0.0.0.0', port=port)
