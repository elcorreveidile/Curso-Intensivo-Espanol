#!/usr/bin/env python3
"""
Backend MongoDB para Sistema de Gestión de Estudiantes
Curso Intensivo de Español - Nivel 3 CLM
Universidad de Granada - Centro de Lenguas Modernas

API Endpoints:
    - POST /api/auth/register - Registrar nuevo estudiante
    - POST /api/auth/login - Login de estudiante
    - POST /api/auth/admin-login - Login de administrador
    - POST /api/attendance/session - Crear sesión QR (admin)
    - GET  /api/attendance/session/<id> - Validar sesión QR
    - POST /api/attendance/register - Registrar asistencia
    - GET  /api/attendance/records - Obtener todos los registros (admin)
    - GET  /api/attendance/student/<id> - Asistencia de un estudiante
    - GET  /api/progress/<userId> - Progreso de estudiante
    - POST /api/progress/material - Actualizar progreso de material
    - POST /api/progress/quiz - Registrar resultado de quiz
    - GET  /api/students - Obtener lista de estudiantes (admin)
"""

import os
import secrets
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import bcrypt
import jwt
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', 'curso_intensivo_espanol')
JWT_SECRET = os.getenv('JWT_SECRET', 'change-this-secret-key')
JWT_EXPIRATION = int(os.getenv('JWT_EXPIRATION', 86400))  # 24 horas
QR_SESSION_DURATION = int(os.getenv('QR_SESSION_DURATION', 300))  # 5 minutos
ADMIN_PASSWORD_HASH = os.getenv('ADMIN_PASSWORD_HASH')

# Crear aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'flask-secret-key')

# Configurar CORS
allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, resources={
    r"/api/*": {
        "origins": allowed_origins,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Conectar a MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    # Colecciones
    users_collection = db['users']
    attendance_collection = db['attendance']
    sessions_collection = db['sessions']
    progress_collection = db['progress']

    # Crear índices
    users_collection.create_index('studentId', unique=True)
    users_collection.create_index('email', unique=True)
    attendance_collection.create_index([('sessionId', 1), ('studentId', 1)])
    sessions_collection.create_index('sessionId', unique=True)
    sessions_collection.create_index('expiresAt', expireAfterSeconds=0)  # TTL index

    print("✅ Conectado a MongoDB exitosamente")

except Exception as e:
    print(f"❌ Error conectando a MongoDB: {e}")
    exit(1)


# ========================================
# DECORADORES DE AUTENTICACIÓN
# ========================================

def token_required(f):
    """Decorator para verificar JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Obtener token del header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'success': False, 'error': 'Token mal formado'}), 401

        if not token:
            return jsonify({'success': False, 'error': 'Token no proporcionado'}), 401

        try:
            # Verificar token
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            current_user = users_collection.find_one({'studentId': data['studentId']})

            if not current_user:
                return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'error': 'Token inválido'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def admin_required(f):
    """Decorator para verificar que el usuario es administrador"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'success': False, 'error': 'Token mal formado'}), 401

        if not token:
            return jsonify({'success': False, 'error': 'Token no proporcionado'}), 401

        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

            # Verificar que sea admin
            if not data.get('isAdmin', False):
                return jsonify({'success': False, 'error': 'Acceso denegado - Se requiere rol de administrador'}), 403

        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'error': 'Token inválido'}), 401

        return f(*args, **kwargs)

    return decorated


# ========================================
# ENDPOINTS DE AUTENTICACIÓN
# ========================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Registrar nuevo estudiante"""
    try:
        data = request.get_json()

        # Validar datos requeridos
        required_fields = ['studentId', 'name', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Campo requerido: {field}'}), 400

        # Verificar si el estudiante ya existe
        if users_collection.find_one({'studentId': data['studentId']}):
            return jsonify({'success': False, 'error': 'ID de estudiante ya registrado'}), 400

        if users_collection.find_one({'email': data['email']}):
            return jsonify({'success': False, 'error': 'Email ya registrado'}), 400

        # Hashear contraseña
        password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        # Crear documento de usuario
        user_doc = {
            'studentId': data['studentId'],
            'name': data['name'],
            'email': data['email'],
            'passwordHash': password_hash,
            'createdAt': datetime.utcnow(),
            'courseLevel': data.get('courseLevel', 'A1.2-A2.1'),
            'active': True
        }

        # Insertar en MongoDB
        result = users_collection.insert_one(user_doc)

        # Crear documento de progreso inicial
        progress_doc = {
            'userId': result.inserted_id,
            'studentId': data['studentId'],
            'attendance': {
                'totalClasses': 16,
                'attendedClasses': 0,
                'attendanceRate': 0,
                'dates': []
            },
            'materials': {
                'vocabularyCompleted': 0,
                'totalVocabulary': 50,
                'exercisesCompleted': 0,
                'totalExercises': 20,
                'materialsViewed': [],
                'completionRate': 0
            },
            'projects': {
                'photo_project': {'status': 'pending', 'completedAt': None},
                'cooking_workshop': {'status': 'pending', 'completedAt': None},
                'role_playing': {'status': 'pending', 'completedAt': None},
                'final_project': {'status': 'pending', 'completedAt': None},
                'completionRate': 0
            },
            'quizScores': {
                'totalQuizzes': 0,
                'correctAnswers': 0,
                'accuracyRate': 0,
                'quizHistory': []
            },
            'lastUpdated': datetime.utcnow()
        }

        progress_collection.insert_one(progress_doc)

        # Generar JWT token
        token = jwt.encode({
            'studentId': data['studentId'],
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION)
        }, JWT_SECRET, algorithm='HS256')

        return jsonify({
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'token': token,
            'user': {
                'studentId': data['studentId'],
                'name': data['name'],
                'email': data['email']
            }
        }), 201

    except DuplicateKeyError:
        return jsonify({'success': False, 'error': 'Usuario ya existe'}), 400
    except Exception as e:
        print(f"Error en register: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login de estudiante"""
    try:
        data = request.get_json()

        # Validar datos requeridos
        if not data.get('studentId') or not data.get('password'):
            return jsonify({'success': False, 'error': 'ID de estudiante y contraseña requeridos'}), 400

        # Buscar usuario
        user = users_collection.find_one({'studentId': data['studentId']})

        if not user:
            return jsonify({'success': False, 'error': 'Credenciales inválidas'}), 401

        # Verificar contraseña
        if not bcrypt.checkpw(data['password'].encode('utf-8'), user['passwordHash']):
            return jsonify({'success': False, 'error': 'Credenciales inválidas'}), 401

        # Verificar que el usuario esté activo
        if not user.get('active', True):
            return jsonify({'success': False, 'error': 'Usuario desactivado'}), 401

        # Generar JWT token
        token = jwt.encode({
            'studentId': user['studentId'],
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION)
        }, JWT_SECRET, algorithm='HS256')

        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'studentId': user['studentId'],
                'name': user['name'],
                'email': user['email'],
                'courseLevel': user.get('courseLevel', 'A1.2-A2.1')
            }
        }), 200

    except Exception as e:
        print(f"Error en login: {e}")
        return jsonify({'success': False, 'error': 'Error en el servidor'}), 500


@app.route('/api/auth/admin-login', methods=['POST'])
def admin_login():
    """Login de administrador/profesor"""
    try:
        data = request.get_json()

        if not data.get('password'):
            return jsonify({'success': False, 'error': 'Contraseña requerida'}), 400

        # Verificar contraseña de admin
        if ADMIN_PASSWORD_HASH:
            if not bcrypt.checkpw(data['password'].encode('utf-8'), ADMIN_PASSWORD_HASH.encode('utf-8')):
                return jsonify({'success': False, 'error': 'Credenciales inválidas'}), 401
        else:
            # Fallback para desarrollo (sin hash configurado)
            if data['password'] != 'ugr2024':
                return jsonify({'success': False, 'error': 'Credenciales inválidas'}), 401

        # Generar JWT token con flag de admin
        token = jwt.encode({
            'isAdmin': True,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION)
        }, JWT_SECRET, algorithm='HS256')

        return jsonify({
            'success': True,
            'token': token,
            'admin': True
        }), 200

    except Exception as e:
        print(f"Error en admin_login: {e}")
        return jsonify({'success': False, 'error': 'Error en el servidor'}), 500


# ========================================
# ENDPOINTS DE ASISTENCIA
# ========================================

@app.route('/api/attendance/session', methods=['POST'])
@admin_required
def create_attendance_session():
    """Crear nueva sesión de QR (solo admin)"""
    try:
        data = request.get_json()

        # Generar ID único de sesión
        session_id = f"{datetime.utcnow().strftime('%Y-%m-%d')}-Session-{secrets.token_hex(4)}"

        # Crear documento de sesión
        session_doc = {
            'sessionId': session_id,
            'course': data.get('course', 'Curso Intensivo de Español - Nivel 3 CLM'),
            'createdAt': datetime.utcnow(),
            'expiresAt': datetime.utcnow() + timedelta(seconds=QR_SESSION_DURATION),
            'isActive': True,
            'qrData': {
                'sessionId': session_id,
                'timestamp': datetime.utcnow().isoformat(),
                'type': 'attendance'
            }
        }

        # Insertar en MongoDB
        sessions_collection.insert_one(session_doc)

        return jsonify({
            'success': True,
            'sessionId': session_id,
            'qrData': session_doc['qrData'],
            'expiresIn': QR_SESSION_DURATION
        }), 201

    except Exception as e:
        print(f"Error en create_attendance_session: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/attendance/session/<session_id>', methods=['GET'])
def validate_session(session_id):
    """Validar si una sesión QR es válida"""
    try:
        # Buscar sesión
        session = sessions_collection.find_one({'sessionId': session_id})

        if not session:
            return jsonify({'success': False, 'error': 'Sesión no encontrada'}), 404

        # Verificar si ha expirado
        if datetime.utcnow() > session['expiresAt']:
            return jsonify({'success': False, 'error': 'Sesión expirada'}), 410

        # Verificar si está activa
        if not session.get('isActive', False):
            return jsonify({'success': False, 'error': 'Sesión desactivada'}), 403

        return jsonify({
            'success': True,
            'session': {
                'sessionId': session['sessionId'],
                'course': session.get('course'),
                'createdAt': session['createdAt'].isoformat(),
                'expiresAt': session['expiresAt'].isoformat()
            }
        }), 200

    except Exception as e:
        print(f"Error en validate_session: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/attendance/register', methods=['POST'])
@token_required
def register_attendance(current_user):
    """Registrar asistencia de un estudiante"""
    try:
        data = request.get_json()

        # Validar sessionId
        if not data.get('sessionId'):
            return jsonify({'success': False, 'error': 'sessionId requerido'}), 400

        # Verificar que la sesión existe y es válida
        session = sessions_collection.find_one({'sessionId': data['sessionId']})

        if not session:
            return jsonify({'success': False, 'error': 'Sesión no encontrada'}), 404

        if datetime.utcnow() > session['expiresAt']:
            return jsonify({'success': False, 'error': 'Sesión expirada'}), 410

        # Verificar si ya registró asistencia para esta sesión
        existing = attendance_collection.find_one({
            'sessionId': data['sessionId'],
            'studentId': current_user['studentId']
        })

        if existing:
            return jsonify({'success': False, 'error': 'Ya has registrado tu asistencia para esta sesión'}), 400

        # Crear registro de asistencia
        attendance_doc = {
            'sessionId': data['sessionId'],
            'studentId': current_user['studentId'],
            'studentName': current_user['name'],
            'timestamp': datetime.utcnow(),
            'registeredAt': datetime.utcnow(),
            'course': session.get('course', 'Curso Intensivo de Español - Nivel 3 CLM'),
            'ipAddress': request.remote_addr
        }

        # Insertar en MongoDB
        attendance_collection.insert_one(attendance_doc)

        # Actualizar progreso del estudiante
        progress_collection.update_one(
            {'studentId': current_user['studentId']},
            {
                '$inc': {'attendance.attendedClasses': 1},
                '$push': {'attendance.dates': datetime.utcnow().isoformat()},
                '$set': {'lastUpdated': datetime.utcnow()}
            }
        )

        # Recalcular tasa de asistencia
        progress = progress_collection.find_one({'studentId': current_user['studentId']})
        if progress:
            total = progress['attendance']['totalClasses']
            attended = progress['attendance']['attendedClasses']
            rate = round((attended / total) * 100, 1) if total > 0 else 0

            progress_collection.update_one(
                {'studentId': current_user['studentId']},
                {'$set': {'attendance.attendanceRate': rate}}
            )

        return jsonify({
            'success': True,
            'message': 'Asistencia registrada correctamente',
            'attendance': {
                'sessionId': data['sessionId'],
                'timestamp': attendance_doc['timestamp'].isoformat()
            }
        }), 201

    except Exception as e:
        print(f"Error en register_attendance: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/attendance/records', methods=['GET'])
@admin_required
def get_attendance_records():
    """Obtener todos los registros de asistencia (solo admin)"""
    try:
        # Obtener parámetros de query
        session_id = request.args.get('sessionId')
        student_id = request.args.get('studentId')

        # Construir filtro
        query = {}
        if session_id:
            query['sessionId'] = session_id
        if student_id:
            query['studentId'] = student_id

        # Obtener registros
        records = list(attendance_collection.find(query).sort('timestamp', -1))

        # Convertir ObjectId a string y datetime a ISO
        for record in records:
            record['_id'] = str(record['_id'])
            record['timestamp'] = record['timestamp'].isoformat()
            record['registeredAt'] = record['registeredAt'].isoformat()

        return jsonify({
            'success': True,
            'records': records,
            'count': len(records)
        }), 200

    except Exception as e:
        print(f"Error en get_attendance_records: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/attendance/student/<student_id>', methods=['GET'])
@token_required
def get_student_attendance(current_user, student_id):
    """Obtener asistencia de un estudiante específico"""
    try:
        # Verificar que el usuario solo puede ver su propia asistencia
        if current_user['studentId'] != student_id:
            return jsonify({'success': False, 'error': 'No autorizado'}), 403

        # Obtener registros
        records = list(attendance_collection.find({'studentId': student_id}).sort('timestamp', -1))

        # Convertir ObjectId y datetime
        for record in records:
            record['_id'] = str(record['_id'])
            record['timestamp'] = record['timestamp'].isoformat()
            record['registeredAt'] = record['registeredAt'].isoformat()

        return jsonify({
            'success': True,
            'records': records,
            'count': len(records)
        }), 200

    except Exception as e:
        print(f"Error en get_student_attendance: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ========================================
# ENDPOINTS DE PROGRESO
# ========================================

@app.route('/api/progress/<student_id>', methods=['GET'])
@token_required
def get_student_progress(current_user, student_id):
    """Obtener progreso completo de un estudiante"""
    try:
        # Verificar autorización
        if current_user['studentId'] != student_id:
            return jsonify({'success': False, 'error': 'No autorizado'}), 403

        # Obtener progreso
        progress = progress_collection.find_one({'studentId': student_id})

        if not progress:
            return jsonify({'success': False, 'error': 'Progreso no encontrado'}), 404

        # Convertir ObjectId y datetime
        progress['_id'] = str(progress['_id'])
        progress['userId'] = str(progress['userId'])
        progress['lastUpdated'] = progress['lastUpdated'].isoformat()

        return jsonify({
            'success': True,
            'progress': progress
        }), 200

    except Exception as e:
        print(f"Error en get_student_progress: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/progress/material', methods=['POST'])
@token_required
def update_material_progress(current_user):
    """Actualizar progreso de materiales"""
    try:
        data = request.get_json()

        material_type = data.get('materialType')  # 'vocabulary' or 'exercises'
        item_id = data.get('itemId')

        if not material_type or not item_id:
            return jsonify({'success': False, 'error': 'materialType e itemId requeridos'}), 400

        # Actualizar progreso
        field_key = f'materials.{material_type}Completed'

        progress_collection.update_one(
            {'studentId': current_user['studentId']},
            {
                '$inc': {field_key: 1},
                '$addToSet': {'materials.materialsViewed': item_id},
                '$set': {'lastUpdated': datetime.utcnow()}
            }
        )

        # Recalcular completion rate
        progress = progress_collection.find_one({'studentId': current_user['studentId']})
        if progress:
            materials = progress['materials']
            total = materials['totalVocabulary'] + materials['totalExercises']
            completed = materials['vocabularyCompleted'] + materials['exercisesCompleted']
            rate = round((completed / total) * 100, 1) if total > 0 else 0

            progress_collection.update_one(
                {'studentId': current_user['studentId']},
                {'$set': {'materials.completionRate': rate}}
            )

        return jsonify({
            'success': True,
            'message': 'Progreso actualizado'
        }), 200

    except Exception as e:
        print(f"Error en update_material_progress: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/progress/quiz', methods=['POST'])
@token_required
def record_quiz_result(current_user):
    """Registrar resultado de quiz"""
    try:
        data = request.get_json()

        correct_answers = data.get('correctAnswers')
        total_questions = data.get('totalQuestions')
        quiz_id = data.get('quizId')

        if correct_answers is None or not total_questions:
            return jsonify({'success': False, 'error': 'correctAnswers y totalQuestions requeridos'}), 400

        # Crear registro de quiz
        quiz_record = {
            'quizId': quiz_id or f"quiz_{datetime.utcnow().timestamp()}",
            'correctAnswers': correct_answers,
            'totalQuestions': total_questions,
            'accuracy': round((correct_answers / total_questions) * 100, 1),
            'date': datetime.utcnow().isoformat()
        }

        # Actualizar progreso
        progress_collection.update_one(
            {'studentId': current_user['studentId']},
            {
                '$inc': {
                    'quizScores.totalQuizzes': 1,
                    'quizScores.correctAnswers': correct_answers
                },
                '$push': {'quizScores.quizHistory': quiz_record},
                '$set': {'lastUpdated': datetime.utcnow()}
            }
        )

        # Recalcular accuracy rate
        progress = progress_collection.find_one({'studentId': current_user['studentId']})
        if progress:
            quiz_scores = progress['quizScores']
            total_possible = quiz_scores['totalQuizzes'] * 5  # Asumiendo 5 preguntas por quiz
            rate = round((quiz_scores['correctAnswers'] / total_possible) * 100, 1) if total_possible > 0 else 0

            progress_collection.update_one(
                {'studentId': current_user['studentId']},
                {'$set': {'quizScores.accuracyRate': rate}}
            )

        return jsonify({
            'success': True,
            'message': 'Quiz registrado',
            'result': quiz_record
        }), 200

    except Exception as e:
        print(f"Error en record_quiz_result: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ========================================
# ENDPOINTS ADMINISTRATIVOS
# ========================================

@app.route('/api/students', methods=['GET'])
@admin_required
def get_all_students():
    """Obtener lista de todos los estudiantes (solo admin)"""
    try:
        # Obtener todos los usuarios
        users = list(users_collection.find({'active': True}))

        students = []
        for user in users:
            # Obtener progreso del estudiante
            progress = progress_collection.find_one({'studentId': user['studentId']})

            student_data = {
                'studentId': user['studentId'],
                'name': user['name'],
                'email': user['email'],
                'courseLevel': user.get('courseLevel'),
                'createdAt': user['createdAt'].isoformat(),
                'attendance': progress['attendance'] if progress else None,
                'materialsCompletion': progress['materials']['completionRate'] if progress else 0,
                'quizAccuracy': progress['quizScores']['accuracyRate'] if progress else 0
            }

            students.append(student_data)

        return jsonify({
            'success': True,
            'students': students,
            'count': len(students)
        }), 200

    except Exception as e:
        print(f"Error en get_all_students: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ========================================
# ENDPOINTS DE SALUD Y ESTADO
# ========================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Verificar conexión a MongoDB
        client.admin.command('ping')

        return jsonify({
            'success': True,
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'API Backend - Curso Intensivo de Español',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth/*',
            'attendance': '/api/attendance/*',
            'progress': '/api/progress/*',
            'admin': '/api/students',
            'health': '/api/health'
        }
    }), 200


# ========================================
# ERROR HANDLERS
# ========================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': 'Endpoint no encontrado'}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500


# ========================================
# MAIN
# ========================================

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    print("\n" + "="*60)
    print("🚀 Backend API - Curso Intensivo de Español")
    print("="*60)
    print(f"📡 Server: http://{host}:{port}")
    print(f"🗄️  Database: {DB_NAME}")
    print(f"🔐 JWT Expiration: {JWT_EXPIRATION}s ({JWT_EXPIRATION/3600}h)")
    print(f"⏱️  QR Session Duration: {QR_SESSION_DURATION}s ({QR_SESSION_DURATION/60}min)")
    print("="*60)
    print("\n📋 API Endpoints:")
    print("   POST   /api/auth/register")
    print("   POST   /api/auth/login")
    print("   POST   /api/auth/admin-login")
    print("   POST   /api/attendance/session")
    print("   GET    /api/attendance/session/<id>")
    print("   POST   /api/attendance/register")
    print("   GET    /api/attendance/records")
    print("   GET    /api/attendance/student/<id>")
    print("   GET    /api/progress/<student_id>")
    print("   POST   /api/progress/material")
    print("   POST   /api/progress/quiz")
    print("   GET    /api/students")
    print("   GET    /api/health")
    print("="*60 + "\n")

    app.run(host=host, port=port, debug=debug)
