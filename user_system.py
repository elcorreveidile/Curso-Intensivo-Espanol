#!/usr/bin/env python3
"""
Sistema de gestión de usuarios y base de datos para seguimiento del progreso
"""

import json
import os
from datetime import datetime, date
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import hashlib
import secrets

# Datos de usuarios (en producción usaríamos una base de datos real)
USERS_DB_FILE = 'users_database.json'
PROGRESS_DB_FILE = 'progress_database.json'

class UserSystem:
    def __init__(self):
        self.load_databases()

    def load_databases(self):
        """Cargar bases de datos desde archivos JSON"""
        if os.path.exists(USERS_DB_FILE):
            with open(USERS_DB_FILE, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        else:
            self.users = {}

        if os.path.exists(PROGRESS_DB_FILE):
            with open(PROGRESS_DB_FILE, 'r', encoding='utf-8') as f:
                self.progress = json.load(f)
        else:
            self.progress = {}

    def save_databases(self):
        """Guardar bases de datos a archivos JSON"""
        with open(USERS_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)

        with open(PROGRESS_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, ensure_ascii=False, indent=2)

    def create_user(self, name, email, student_id=None):
        """Crear nuevo usuario"""
        user_id = secrets.token_hex(8)
        password = secrets.token_hex(4)

        user_data = {
            'id': user_id,
            'name': name,
            'email': email,
            'student_id': student_id,
            'password': password,
            'created_at': datetime.now().isoformat(),
            'course_level': 'A1.2-A2.1',
            'active': True
        }

        self.users[user_id] = user_data
        self.initialize_progress(user_id)
        self.save_databases()

        return user_data

    def initialize_progress(self, user_id):
        """Inicializar progreso del usuario"""
        self.progress[user_id] = {
            'user_id': user_id,
            'attendance': {
                'total_classes': 16,  # Lunes-Jueves x 4 semanas
                'attended_classes': 0,
                'attendance_dates': [],
                'attendance_rate': 0
            },
            'materials': {
                'vocabulary_completed': 0,
                'total_vocabulary': 50,
                'exercises_completed': 0,
                'total_exercises': 20,
                'materials_viewed': [],
                'completion_rate': 0
            },
            'projects': {
                'photo_project': {'status': 'pending', 'completed_at': None},
                'cooking_workshop': {'status': 'pending', 'completed_at': None},
                'role_playing': {'status': 'pending', 'completed_at': None},
                'final_project': {'status': 'pending', 'completed_at': None},
                'completion_rate': 0
            },
            'quiz_scores': {
                'total_quizzes': 0,
                'correct_answers': 0,
                'accuracy_rate': 0,
                'quiz_history': []
            },
            'weekly_goals': {
                'week_1': {'goals': [], 'completed': 0, 'total': 0},
                'week_2': {'goals': [], 'completed': 0, 'total': 0},
                'week_3': {'goals': [], 'completed': 0, 'total': 0},
                'week_4': {'goals': [], 'completed': 0, 'total': 0}
            },
            'last_updated': datetime.now().isoformat()
        }

    def get_user_progress(self, user_id):
        """Obtener progreso completo del usuario"""
        if user_id not in self.progress:
            return None

        # Calcular tasas de completado
        progress_data = self.progress[user_id]

        # Asistencia
        attendance = progress_data['attendance']
        attendance['attendance_rate'] = round((attendance['attended_classes'] / attendance['total_classes']) * 100, 1) if attendance['total_classes'] > 0 else 0

        # Materiales
        materials = progress_data['materials']
        total_materials = materials['total_vocabulary'] + materials['total_exercises']
        completed_materials = materials['vocabulary_completed'] + materials['exercises_completed']
        materials['completion_rate'] = round((completed_materials / total_materials) * 100, 1) if total_materials > 0 else 0

        # Proyectos
        projects = progress_data['projects']
        completed_projects = sum(1 for project in projects.values() if project['status'] == 'completed')
        total_projects = len([p for p in projects.values() if p['status'] != 'final_project']) + 1
        projects['completion_rate'] = round((completed_projects / total_projects) * 100, 1) if total_projects > 0 else 0

        # Quiz scores
        quiz_scores = progress_data['quiz_scores']
        if quiz_scores['total_quizzes'] > 0:
            quiz_scores['accuracy_rate'] = round((quiz_scores['correct_answers'] / (quiz_scores['total_quizzes'] * 5)) * 100, 1)  # Asumiendo 5 preguntas por quiz

        progress_data['last_updated'] = datetime.now().isoformat()
        self.save_databases()

        return progress_data

    def record_attendance(self, user_id, class_date=None):
        """Registrar asistencia de un usuario"""
        if user_id not in self.progress:
            return False

        if class_date is None:
            class_date = date.today().isoformat()

        progress = self.progress[user_id]
        if class_date not in progress['attendance']['attendance_dates']:
            progress['attendance']['attendance_dates'].append(class_date)
            progress['attendance']['attended_classes'] += 1
            progress['last_updated'] = datetime.now().isoformat()
            self.save_databases()
            return True

        return False

    def update_material_progress(self, user_id, material_type, item_id):
        """Actualizar progreso de materiales"""
        if user_id not in self.progress:
            return False

        progress = self.progress[user_id]
        material_key = f"{material_type}_completed"

        if material_key in progress['materials']:
            if item_id not in progress['materials'].get('materials_viewed', []):
                progress['materials']['materials_viewed'].append(item_id)
                progress['materials'][material_key] += 1
                progress['last_updated'] = datetime.now().isoformat()
                self.save_databases()
                return True

        return False

    def record_quiz_score(self, user_id, correct_answers, total_questions, quiz_id=None):
        """Registrar resultado de quiz"""
        if user_id not in self.progress:
            return False

        progress = self.progress[user_id]
        quiz_record = {
            'quiz_id': quiz_id or f"quiz_{len(progress['quiz_scores']['quiz_history']) + 1}",
            'correct_answers': correct_answers,
            'total_questions': total_questions,
            'accuracy': round((correct_answers / total_questions) * 100, 1) if total_questions > 0 else 0,
            'date': datetime.now().isoformat()
        }

        progress['quiz_scores']['quiz_history'].append(quiz_record)
        progress['quiz_scores']['total_quizzes'] += 1
        progress['quiz_scores']['correct_answers'] += correct_answers
        progress['last_updated'] = datetime.now().isoformat()
        self.save_databases()

        return True

    def complete_project(self, user_id, project_id):
        """Marcar proyecto como completado"""
        if user_id not in self.progress or project_id not in self.progress[user_id]['projects']:
            return False

        progress = self.progress[user_id]
        if progress['projects'][project_id]['status'] != 'completed':
            progress['projects'][project_id]['status'] = 'completed'
            progress['projects'][project_id]['completed_at'] = datetime.now().isoformat()
            progress['last_updated'] = datetime.now().isoformat()
            self.save_databases()
            return True

        return False

    def get_user_by_id(self, user_id):
        """Obtener datos de usuario por ID"""
        return self.users.get(user_id)

    def authenticate_user(self, user_id, password):
        """Autenticar usuario"""
        user = self.users.get(user_id)
        if user and user.get('password') == password:
            return user
        return None

    def get_all_users_summary(self):
        """Obtener resumen de todos los usuarios"""
        summary = []
        for user_id, user in self.users.items():
            if user.get('active', True):
                progress = self.get_user_progress(user_id)
                if progress:
                    summary.append({
                        'user_id': user_id,
                        'name': user['name'],
                        'email': user['email'],
                        'attendance_rate': progress['attendance']['attendance_rate'],
                        'materials_completion': progress['materials']['completion_rate'],
                        'projects_completion': progress['projects']['completion_rate'],
                        'quiz_accuracy': progress['quiz_scores']['accuracy_rate'],
                        'last_active': progress['last_updated']
                    })
        return summary

# Crear aplicación Flask para el API
app = Flask(__name__)
CORS(app)
user_system = UserSystem()

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    student_id = data.get('student_id')

    if not name or not email:
        return jsonify({'error': 'Nombre y email son requeridos'}), 400

    user = user_system.create_user(name, email, student_id)
    return jsonify({
        'success': True,
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'password': user['password']
        }
    })

@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.json
    user_id = data.get('user_id')
    password = data.get('password')

    if not user_id or not password:
        return jsonify({'error': 'ID de usuario y contraseña son requeridos'}), 400

    user = user_system.authenticate_user(user_id, password)
    if user:
        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email']
            }
        })
    else:
        return jsonify({'error': 'Credenciales inválidas'}), 401

@app.route('/api/progress/<user_id>', methods=['GET'])
def get_progress(user_id):
    progress = user_system.get_user_progress(user_id)
    if progress:
        return jsonify({'success': True, 'progress': progress})
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

@app.route('/api/attendance', methods=['POST'])
def record_attendance():
    data = request.json
    user_id = data.get('user_id')
    class_date = data.get('class_date')

    if not user_id:
        return jsonify({'error': 'ID de usuario requerido'}), 400

    success = user_system.record_attendance(user_id, class_date)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'No se pudo registrar la asistencia'}), 400

@app.route('/api/materials', methods=['POST'])
def update_materials():
    data = request.json
    user_id = data.get('user_id')
    material_type = data.get('material_type')
    item_id = data.get('item_id')

    if not all([user_id, material_type, item_id]):
        return jsonify({'error': 'Todos los campos son requeridos'}), 400

    success = user_system.update_material_progress(user_id, material_type, item_id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'No se pudo actualizar el progreso'}), 400

@app.route('/api/quiz', methods=['POST'])
def record_quiz():
    data = request.json
    user_id = data.get('user_id')
    correct_answers = data.get('correct_answers')
    total_questions = data.get('total_questions')
    quiz_id = data.get('quiz_id')

    if not all([user_id, correct_answers is not None, total_questions]):
        return jsonify({'error': 'Todos los campos son requeridos'}), 400

    success = user_system.record_quiz_score(user_id, correct_answers, total_questions, quiz_id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'No se pudo registrar el quiz'}), 400

@app.route('/api/projects', methods=['POST'])
def complete_project():
    data = request.json
    user_id = data.get('user_id')
    project_id = data.get('project_id')

    if not user_id or not project_id:
        return jsonify({'error': 'ID de usuario y proyecto son requeridos'}), 400

    success = user_system.complete_project(user_id, project_id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'No se pudo completar el proyecto'}), 400

# Crear archivos de bases de datos si no existen
if __name__ == "__main__":
    # Inicializar bases de datos si no existen
    if not os.path.exists(USERS_DB_FILE):
        # Crear un usuario de ejemplo para pruebas
        example_user = user_system.create_user(
            name="Estudiante Ejemplo",
            email="estudiante@ejemplo.com",
            student_id="2025001"
        )
        print(f"✅ Usuario de ejemplo creado:")
        print(f"   ID: {example_user['id']}")
        print(f"   Contraseña: {example_user['password']}")
        print(f"   Guarda estos datos para probar el sistema")

    print("\n🚀 Sistema de usuarios iniciado en http://localhost:5000")
    print("📊 API endpoints disponibles:")
    print("   POST /api/register - Registrar nuevo usuario")
    print("   POST /api/login - Iniciar sesión")
    print("   GET  /api/progress/<user_id> - Obtener progreso")
    print("   POST /api/attendance - Registrar asistencia")
    print("   POST /api/materials - Actualizar materiales")
    print("   POST /api/quiz - Registrar quiz")
    print("   POST /api/projects - Completar proyecto")

    # Iniciar servidor (solo para desarrollo)
    # app.run(debug=True, port=5000)