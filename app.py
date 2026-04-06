"""
SkillForge Web API - Flask Backend
Provides REST API endpoints for the web frontend
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from skillforge import SkillForgeManager, TechnicalSkill, SoftSkill, MasteryAlgorithm
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

# Initialize manager
manager = SkillForgeManager('skillforge_data.json')

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get all skills"""
    try:
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
        
        if skill_type == 'technical':
            difficulty = int(data.get('difficulty', 5))
            manager.add_technical_skill(name, category, difficulty)
        elif skill_type == 'soft':
            applications = int(data.get('applications', 0))
            manager.add_soft_skill(name, category, applications)
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid skill type'
            }), 400
        
        manager.save_skills()
        
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
        skill = manager._SkillForgeManager__find_skill(skill_name)
        if not skill:
            return jsonify({
                'success': False,
                'error': f'Skill "{skill_name}" not found'
            }), 404
        
        return jsonify({
            'success': True,
            'history': skill.history
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
