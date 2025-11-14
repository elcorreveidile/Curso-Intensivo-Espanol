#!/usr/bin/env python3
"""
Script de Migración a MongoDB
Curso Intensivo de Español - Nivel 3 CLM

Este script:
1. Crea usuarios iniciales para los 11 estudiantes
2. Genera contraseñas temporales
3. Inicializa documentos de progreso
4. Opcionalmente migra registros de asistencia desde localStorage
"""

import os
import json
from datetime import datetime
from pymongo import MongoClient
import bcrypt
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', 'curso_intensivo_espanol')

# Lista completa de estudiantes
STUDENTS = {
    'EST-001': {
        'name': 'BENNASRI, MAMMER PAOLO',
        'email': 'bennasri@correo.ugr.es'
    },
    'EST-002': {
        'name': 'COCKRELL, JAMES RYDER',
        'email': 'cockrell@correo.ugr.es'
    },
    'EST-003': {
        'name': 'LU, JIAQI',
        'email': 'lu@correo.ugr.es'
    },
    'EST-004': {
        'name': 'MOLLAH, ALLAN SHUMON',
        'email': 'mollah@correo.ugr.es'
    },
    'EST-005': {
        'name': 'TJAHAJA, DYLANN',
        'email': 'tjahaja@correo.ugr.es'
    },
    'EST-006': {
        'name': 'WALKER, KAMRYN',
        'email': 'walker@correo.ugr.es'
    },
    'EST-007': {
        'name': 'WANG, XINYI',
        'email': 'wang@correo.ugr.es'
    },
    'EST-008': {
        'name': 'WILLIAMS, DIOR',
        'email': 'williams@correo.ugr.es'
    },
    'EST-009': {
        'name': 'XU, JIAHUI',
        'email': 'xu@correo.ugr.es'
    },
    'EST-010': {
        'name': 'ZHANG, ANJIE',
        'email': 'zhang.a@correo.ugr.es'
    },
    'EST-011': {
        'name': 'ZHANG, JING',
        'email': 'zhang.j@correo.ugr.es'
    }
}


def connect_to_mongodb():
    """Conectar a MongoDB"""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]

        # Test connection
        client.admin.command('ping')
        print(f"✅ Conectado a MongoDB: {DB_NAME}")

        return db
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")
        exit(1)


def create_users(db):
    """Crear usuarios iniciales con contraseñas temporales"""
    print("\n📝 Creando usuarios...")

    users_collection = db['users']
    progress_collection = db['progress']

    created_count = 0
    credentials = []

    for student_id, info in STUDENTS.items():
        try:
            # Verificar si ya existe
            if users_collection.find_one({'studentId': student_id}):
                print(f"   ⚠️  Usuario {student_id} ya existe, saltando...")
                continue

            # Generar contraseña temporal: últimos 3 dígitos del ID
            temp_password = student_id[-3:]  # "001", "002", etc.

            # Hashear contraseña
            password_hash = bcrypt.hashpw(temp_password.encode('utf-8'), bcrypt.gensalt())

            # Crear documento de usuario
            user_doc = {
                'studentId': student_id,
                'name': info['name'],
                'email': info['email'],
                'passwordHash': password_hash,
                'createdAt': datetime.utcnow(),
                'courseLevel': 'A1.2-A2.1',
                'active': True
            }

            # Insertar usuario
            result = users_collection.insert_one(user_doc)

            # Crear documento de progreso inicial
            progress_doc = {
                'userId': result.inserted_id,
                'studentId': student_id,
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

            print(f"   ✅ Usuario creado: {student_id} - {info['name']}")

            # Guardar credenciales para mostrar al final
            credentials.append({
                'studentId': student_id,
                'name': info['name'],
                'email': info['email'],
                'password': temp_password
            })

            created_count += 1

        except Exception as e:
            print(f"   ❌ Error creando usuario {student_id}: {e}")

    print(f"\n✅ {created_count} usuarios creados")

    return credentials


def migrate_attendance_from_json(db, json_file_path):
    """Migrar registros de asistencia desde archivo JSON exportado de localStorage"""
    if not os.path.exists(json_file_path):
        print(f"\n⚠️  Archivo {json_file_path} no encontrado. Saltando migración de asistencia.")
        return 0

    print(f"\n📥 Migrando asistencia desde {json_file_path}...")

    attendance_collection = db['attendance']
    progress_collection = db['progress']

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            records = json.load(f)

        migrated_count = 0

        for record in records:
            try:
                # Verificar si ya existe
                existing = attendance_collection.find_one({
                    'sessionId': record.get('sessionId'),
                    'studentId': record.get('studentId')
                })

                if existing:
                    continue

                # Crear documento de asistencia
                attendance_doc = {
                    'sessionId': record.get('sessionId', f"MIGRATED-{datetime.utcnow().timestamp()}"),
                    'studentId': record.get('studentId'),
                    'studentName': record.get('studentName'),
                    'timestamp': datetime.fromisoformat(record.get('timestamp', datetime.utcnow().isoformat()).replace('Z', '+00:00')),
                    'registeredAt': datetime.fromisoformat(record.get('registeredAt', record.get('timestamp', datetime.utcnow().isoformat())).replace('Z', '+00:00')),
                    'course': record.get('course', 'Curso Intensivo de Español - Nivel 3 CLM'),
                    'ipAddress': record.get('ip', record.get('ipAddress', 'unknown'))
                }

                # Insertar en MongoDB
                attendance_collection.insert_one(attendance_doc)

                # Actualizar progreso del estudiante
                progress_collection.update_one(
                    {'studentId': record.get('studentId')},
                    {
                        '$inc': {'attendance.attendedClasses': 1},
                        '$addToSet': {'attendance.dates': attendance_doc['timestamp'].isoformat()}
                    }
                )

                migrated_count += 1

            except Exception as e:
                print(f"   ❌ Error migrando registro: {e}")

        # Recalcular tasas de asistencia
        for student_id in STUDENTS.keys():
            progress = progress_collection.find_one({'studentId': student_id})
            if progress:
                total = progress['attendance']['totalClasses']
                attended = progress['attendance']['attendedClasses']
                rate = round((attended / total) * 100, 1) if total > 0 else 0

                progress_collection.update_one(
                    {'studentId': student_id},
                    {'$set': {'attendance.attendanceRate': rate}}
                )

        print(f"✅ {migrated_count} registros de asistencia migrados")
        return migrated_count

    except Exception as e:
        print(f"❌ Error migrando asistencia: {e}")
        return 0


def create_indexes(db):
    """Crear índices para optimizar consultas"""
    print("\n🔍 Creando índices...")

    try:
        # Índices de usuarios
        db['users'].create_index('studentId', unique=True)
        db['users'].create_index('email', unique=True)

        # Índices de asistencia
        db['attendance'].create_index([('sessionId', 1), ('studentId', 1)])
        db['attendance'].create_index('timestamp')

        # Índices de sesiones
        db['sessions'].create_index('sessionId', unique=True)
        db['sessions'].create_index('expiresAt', expireAfterSeconds=0)  # TTL index

        # Índices de progreso
        db['progress'].create_index('studentId')

        print("✅ Índices creados")

    except Exception as e:
        print(f"⚠️  Error creando índices: {e}")


def generate_admin_password_hash():
    """Generar hash para contraseña de administrador"""
    print("\n🔐 Generando hash para contraseña de administrador...")

    admin_password = input("Ingresa la contraseña de administrador (default: ugr2024): ").strip()

    if not admin_password:
        admin_password = "ugr2024"

    password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())

    print(f"\n📋 Agrega esto a tu archivo .env:")
    print(f"ADMIN_PASSWORD_HASH={password_hash.decode('utf-8')}")
    print(f"\nContraseña: {admin_password}")


def print_credentials(credentials):
    """Imprimir credenciales de usuarios creados"""
    if not credentials:
        return

    print("\n" + "="*70)
    print("📋 CREDENCIALES DE ACCESO - GUARDAR EN LUGAR SEGURO")
    print("="*70)
    print(f"{'ID':<10} {'Nombre':<30} {'Password':<10}")
    print("-"*70)

    for cred in credentials:
        print(f"{cred['studentId']:<10} {cred['name']:<30} {cred['password']:<10}")

    print("="*70)
    print("\n⚠️  IMPORTANTE:")
    print("   - Estas son contraseñas TEMPORALES")
    print("   - Los estudiantes deben cambiarlas en su primer login")
    print("   - Guarda estas credenciales en un lugar seguro")
    print("="*70 + "\n")


def main():
    """Función principal de migración"""
    print("\n" + "="*70)
    print("🚀 MIGRACIÓN A MONGODB - Curso Intensivo de Español")
    print("="*70 + "\n")

    # Conectar a MongoDB
    db = connect_to_mongodb()

    # Opciones
    print("\n¿Qué deseas hacer?")
    print("1. Crear usuarios iniciales (11 estudiantes)")
    print("2. Migrar asistencia desde archivo JSON")
    print("3. Crear índices")
    print("4. Generar hash de contraseña de administrador")
    print("5. Hacer todo lo anterior")

    choice = input("\nSelecciona una opción (1-5): ").strip()

    if choice == '1' or choice == '5':
        credentials = create_users(db)
        print_credentials(credentials)

    if choice == '2' or choice == '5':
        json_file = input("\nRuta al archivo JSON de asistencia (Enter para saltar): ").strip()
        if json_file:
            migrate_attendance_from_json(db, json_file)

    if choice == '3' or choice == '5':
        create_indexes(db)

    if choice == '4' or choice == '5':
        generate_admin_password_hash()

    print("\n" + "="*70)
    print("✅ MIGRACIÓN COMPLETADA")
    print("="*70)
    print("\nPróximos pasos:")
    print("1. Copia .env.example a .env y configura tus variables")
    print("2. Inicia el backend: python backend_mongodb.py")
    print("3. Prueba los endpoints con curl o Postman")
    print("4. Actualiza el frontend para usar la nueva API")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
