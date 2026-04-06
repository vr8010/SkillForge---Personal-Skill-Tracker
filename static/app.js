// SkillForge Frontend JavaScript

const API_BASE_URL = 'http://localhost:5000/api';

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadStatistics();
    loadSkills();
    setupEventListeners();
});

// Setup Event Listeners
function setupEventListeners() {
    // Skill type change
    document.getElementById('skillType').addEventListener('change', (e) => {
        const type = e.target.value;
        const difficultyGroup = document.getElementById('difficultyGroup');
        const applicationsGroup = document.getElementById('applicationsGroup');
        
        if (type === 'technical') {
            difficultyGroup.style.display = 'block';
            applicationsGroup.style.display = 'none';
        } else if (type === 'soft') {
            difficultyGroup.style.display = 'none';
            applicationsGroup.style.display = 'block';
        } else {
            difficultyGroup.style.display = 'none';
            applicationsGroup.style.display = 'none';
        }
    });
    
    // Difficulty slider
    document.getElementById('difficulty').addEventListener('input', (e) => {
        document.getElementById('difficultyValue').textContent = e.target.value;
    });
    
    // Progress slider
    document.getElementById('progressValue').addEventListener('input', (e) => {
        document.getElementById('progressDisplay').textContent = e.target.value + '%';
    });
    
    // Add skill button
    document.getElementById('addSkillBtn').addEventListener('click', addSkill);
    
    // Update progress button
    document.getElementById('updateProgressBtn').addEventListener('click', updateProgress);
    
    // Log hours button
    document.getElementById('logHoursBtn').addEventListener('click', logHours);
    
    // Filter buttons
    document.querySelectorAll('[data-filter]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('[data-filter]').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            filterSkills(e.target.dataset.filter);
        });
    });
}

// Load Statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/statistics`);
        const data = await response.json();
        
        if (data.success) {
            displayStatistics(data.statistics);
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Display Statistics
function displayStatistics(stats) {
    const statsCards = document.getElementById('statsCards');
    
    statsCards.innerHTML = `
        <div class="col-md-3 col-sm-6">
            <div class="stat-card text-center">
                <div class="stat-icon text-primary">
                    <i class="bi bi-collection-fill"></i>
                </div>
                <div class="stat-value">${stats.total_skills}</div>
                <div class="stat-label">Total Skills</div>
            </div>
        </div>
        <div class="col-md-3 col-sm-6">
            <div class="stat-card text-center">
                <div class="stat-icon text-info">
                    <i class="bi bi-code-slash"></i>
                </div>
                <div class="stat-value">${stats.technical_skills}</div>
                <div class="stat-label">Technical Skills</div>
            </div>
        </div>
        <div class="col-md-3 col-sm-6">
            <div class="stat-card text-center">
                <div class="stat-icon text-success">
                    <i class="bi bi-people-fill"></i>
                </div>
                <div class="stat-value">${stats.soft_skills}</div>
                <div class="stat-label">Soft Skills</div>
            </div>
        </div>
        <div class="col-md-3 col-sm-6">
            <div class="stat-card text-center">
                <div class="stat-icon text-warning">
                    <i class="bi bi-trophy-fill"></i>
                </div>
                <div class="stat-value">${stats.average_mastery.toFixed(1)}</div>
                <div class="stat-label">Avg Mastery</div>
            </div>
        </div>
    `;
}

// Load Skills
async function loadSkills() {
    try {
        const response = await fetch(`${API_BASE_URL}/skills`);
        const data = await response.json();
        
        if (data.success) {
            displaySkills(data.skills);
        }
    } catch (error) {
        console.error('Error loading skills:', error);
        showNotification('Error loading skills', 'error');
    }
}

// Display Skills
function displaySkills(skills) {
    const container = document.getElementById('skillsContainer');
    const noSkills = document.getElementById('noSkills');
    
    if (skills.length === 0) {
        container.innerHTML = '';
        noSkills.style.display = 'block';
        return;
    }
    
    noSkills.style.display = 'none';
    
    container.innerHTML = skills.map(skill => createSkillCard(skill)).join('');
}

// Create Skill Card
function createSkillCard(skill) {
    const masteryClass = getMasteryClass(skill.mastery_score);
    const typeColor = skill.skill_type === 'Technical Skill' ? 'info' : 'success';
    const typeBadge = skill.skill_type === 'Technical Skill' ? 
        `<span class="badge bg-${typeColor} skill-type-badge">
            <i class="bi bi-code-slash"></i> Technical
        </span>` :
        `<span class="badge bg-${typeColor} skill-type-badge">
            <i class="bi bi-people"></i> Soft
        </span>`;
    
    const additionalInfo = skill.skill_type === 'Technical Skill' ?
        `<div class="metric-item">
            <i class="bi bi-speedometer2 metric-icon"></i>
            <span>Difficulty: <span class="metric-value">${skill.difficulty_level}/10</span></span>
        </div>` :
        `<div class="metric-item">
            <i class="bi bi-check-circle metric-icon"></i>
            <span>Applications: <span class="metric-value">${skill.real_world_applications || 0}</span></span>
        </div>`;
    
    return `
        <div class="col-lg-4 col-md-6 skill-item fade-in" data-skill-type="${skill.skill_type.toLowerCase().replace(' ', '-')}">
            <div class="skill-card">
                <div class="skill-header">
                    <div>
                        <div class="skill-title">${skill.name}</div>
                        <div class="skill-category">
                            <i class="bi bi-tag"></i> ${skill.category}
                        </div>
                    </div>
                    ${typeBadge}
                </div>
                
                <div class="mastery-section">
                    <div class="mastery-score ${masteryClass}">
                        ${skill.mastery_score.toFixed(1)}
                        <small class="text-muted">/100</small>
                    </div>
                    <div class="mastery-level">
                        ${skill.mastery_level}
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill" style="width: ${skill.mastery_score}%">
                            ${skill.mastery_score.toFixed(0)}%
                        </div>
                    </div>
                </div>
                
                <div class="skill-metrics">
                    <div class="metric-item">
                        <i class="bi bi-graph-up metric-icon"></i>
                        <span>Progress: <span class="metric-value">${skill.progress}%</span></span>
                    </div>
                    <div class="metric-item">
                        <i class="bi bi-clock metric-icon"></i>
                        <span>Hours: <span class="metric-value">${skill.practice_hours}h</span></span>
                    </div>
                    ${additionalInfo}
                    <div class="metric-item">
                        <i class="bi bi-calendar-event metric-icon"></i>
                        <span class="small text-muted">Updated: ${formatDate(skill.last_updated)}</span>
                    </div>
                </div>
                
                <div class="skill-actions">
                    <button class="btn btn-sm btn-outline-success" onclick="openUpdateProgress('${skill.name}', ${skill.progress})">
                        <i class="bi bi-arrow-up-circle"></i> Progress
                    </button>
                    <button class="btn btn-sm btn-outline-info" onclick="openLogHours('${skill.name}')">
                        <i class="bi bi-clock"></i> Hours
                    </button>
                    ${skill.skill_type === 'Soft Skill' ? 
                        `<button class="btn btn-sm btn-outline-primary" onclick="addApplication('${skill.name}')">
                            <i class="bi bi-plus-circle"></i> App
                        </button>` : ''}
                    <button class="btn btn-sm btn-outline-secondary" onclick="viewHistory('${skill.name}')">
                        <i class="bi bi-clock-history"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Get Mastery Class
function getMasteryClass(score) {
    if (score >= 90) return 'mastery-master';
    if (score >= 75) return 'mastery-expert';
    if (score >= 60) return 'mastery-advanced';
    if (score >= 40) return 'mastery-intermediate';
    if (score >= 20) return 'mastery-beginner';
    return 'mastery-novice';
}

// Format Date
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    
    return date.toLocaleDateString();
}

// Add Skill
async function addSkill() {
    const form = document.getElementById('addSkillForm');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const skillData = {
        skill_type: document.getElementById('skillType').value,
        name: document.getElementById('skillName').value,
        category: document.getElementById('skillCategory').value
    };
    
    if (skillData.skill_type === 'technical') {
        skillData.difficulty = document.getElementById('difficulty').value;
    } else if (skillData.skill_type === 'soft') {
        skillData.applications = document.getElementById('applications').value;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/skills`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(skillData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            bootstrap.Modal.getInstance(document.getElementById('addSkillModal')).hide();
            form.reset();
            loadSkills();
            loadStatistics();
        } else {
            showNotification(data.error, 'error');
        }
    } catch (error) {
        console.error('Error adding skill:', error);
        showNotification('Error adding skill', 'error');
    }
}

// Open Update Progress Modal
function openUpdateProgress(skillName, currentProgress) {
    document.getElementById('updateSkillName').value = skillName;
    document.getElementById('progressValue').value = currentProgress;
    document.getElementById('progressDisplay').textContent = currentProgress + '%';
    
    const modal = new bootstrap.Modal(document.getElementById('updateProgressModal'));
    modal.show();
}

// Update Progress
async function updateProgress() {
    const skillName = document.getElementById('updateSkillName').value;
    const progress = document.getElementById('progressValue').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/skills/${encodeURIComponent(skillName)}/progress`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ progress: parseFloat(progress) })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            bootstrap.Modal.getInstance(document.getElementById('updateProgressModal')).hide();
            loadSkills();
            loadStatistics();
        } else {
            showNotification(data.error, 'error');
        }
    } catch (error) {
        console.error('Error updating progress:', error);
        showNotification('Error updating progress', 'error');
    }
}

// Open Log Hours Modal
function openLogHours(skillName) {
    document.getElementById('logHoursSkillName').value = skillName;
    document.getElementById('hoursValue').value = '';
    
    const modal = new bootstrap.Modal(document.getElementById('logHoursModal'));
    modal.show();
}

// Log Hours
async function logHours() {
    const form = document.getElementById('logHoursForm');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const skillName = document.getElementById('logHoursSkillName').value;
    const hours = document.getElementById('hoursValue').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/skills/${encodeURIComponent(skillName)}/hours`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ hours: parseFloat(hours) })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            bootstrap.Modal.getInstance(document.getElementById('logHoursModal')).hide();
            loadSkills();
            loadStatistics();
        } else {
            showNotification(data.error, 'error');
        }
    } catch (error) {
        console.error('Error logging hours:', error);
        showNotification('Error logging hours', 'error');
    }
}

// Add Application
async function addApplication(skillName) {
    try {
        const response = await fetch(`${API_BASE_URL}/skills/${encodeURIComponent(skillName)}/application`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            loadSkills();
            loadStatistics();
        } else {
            showNotification(data.error, 'error');
        }
    } catch (error) {
        console.error('Error adding application:', error);
        showNotification('Error adding application', 'error');
    }
}

// View History
async function viewHistory(skillName) {
    try {
        const response = await fetch(`${API_BASE_URL}/skills/${encodeURIComponent(skillName)}/history`);
        const data = await response.json();
        
        if (data.success) {
            displayHistory(skillName, data.history);
        } else {
            showNotification(data.error, 'error');
        }
    } catch (error) {
        console.error('Error loading history:', error);
        showNotification('Error loading history', 'error');
    }
}

// Display History
function displayHistory(skillName, history) {
    const content = document.getElementById('historyContent');
    
    if (history.length === 0) {
        content.innerHTML = '<p class="text-muted text-center">No history available</p>';
    } else {
        content.innerHTML = `
            <h6 class="mb-3">${skillName}</h6>
            <div class="history-timeline">
                ${history.map(entry => `
                    <div class="history-item">
                        <div class="history-dot"></div>
                        <div class="history-timestamp">
                            <i class="bi bi-clock"></i> ${entry.timestamp}
                        </div>
                        <div class="history-action">
                            <i class="bi bi-arrow-right-circle"></i> ${entry.description}
                        </div>
                        ${entry.details ? `
                            <div class="history-details">
                                ${Object.entries(entry.details).map(([key, value]) => `
                                    <div class="history-detail-item">
                                        <span>${formatKey(key)}:</span>
                                        <strong>${formatValue(value)}</strong>
                                    </div>
                                `).join('')}
                            </div>
                        ` : ''}
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    const modal = new bootstrap.Modal(document.getElementById('historyModal'));
    modal.show();
}

// Format Key
function formatKey(key) {
    return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Format Value
function formatValue(value) {
    if (typeof value === 'number') {
        return value.toFixed(2);
    }
    return value;
}

// Filter Skills
function filterSkills(filter) {
    const skills = document.querySelectorAll('.skill-item');
    
    skills.forEach(skill => {
        if (filter === 'all') {
            skill.style.display = 'block';
        } else if (filter === 'technical') {
            skill.style.display = skill.dataset.skillType === 'technical-skill' ? 'block' : 'none';
        } else if (filter === 'soft') {
            skill.style.display = skill.dataset.skillType === 'soft-skill' ? 'block' : 'none';
        }
    });
}

// Show Notification
function showNotification(message, type = 'success') {
    const toast = document.getElementById('notificationToast');
    const toastMessage = document.getElementById('toastMessage');
    const toastHeader = toast.querySelector('.toast-header i');
    
    toastMessage.textContent = message;
    
    // Update icon based on type
    if (type === 'success') {
        toastHeader.className = 'bi bi-check-circle-fill text-success me-2';
    } else {
        toastHeader.className = 'bi bi-exclamation-circle-fill text-danger me-2';
    }
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}
