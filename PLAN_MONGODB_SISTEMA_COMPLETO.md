# Plan Completo: Sistema de Login y Asistencia con MongoDB

## 📊 Análisis del Sistema Actual

### Estado Actual

#### 1. **Sistema de Login de Estudiantes**
- ✅ Backend existe en `user_system.py` (Flask + API REST)
- ❌ Usa archivos JSON en lugar de MongoDB
- ❌ No está conectado al frontend
- ❌ Contraseñas en texto plano (inseguro)
- ❌ No hay interfaz de login en `index.html`

#### 2. **Sistema de QR para Asistencia**
- ✅ Genera QR correctamente en `index.html`
- ✅ Formulario de registro en `attendance-register.html`
- ✅ Panel admin en `attendance-admin.html`
- ❌ **Solo guarda en localStorage** (se pierde al borrar navegador)
- ❌ **NO hay persistencia en base de datos**
- ❌ **NO se conecta con el backend**

### Archivos Clave Identificados

```
user_system.py              → Backend Flask (usa JSON, no MongoDB)
index.html                  → Genera QR (líneas 1358-1386)
attendance-register.html    → Registro de asistencia (guarda en localStorage)
attendance-admin.html       → Panel admin (lee de localStorage)
```

---

## 🎯 Plan de Implementación Completo

### FASE 1: Configuración de MongoDB y Backend

#### 1.1. Crear Backend con MongoDB Atlas o Local

**Opción A: MongoDB Atlas (Recomendado - Gratis y en la nube)**
```bash
# 1. Crear cuenta en MongoDB Atlas (https://www.mongodb.com/cloud/atlas)
# 2. Crear cluster gratuito
# 3. Obtener connection string
```

**Opción B: MongoDB Local**
```bash
# Instalar MongoDB localmente
sudo apt-get install mongodb  # Linux
brew install mongodb-community  # macOS
```

#### 1.2. Instalar Dependencias Python

```bash
pip install pymongo flask flask-cors bcrypt pyjwt python-dotenv
```

#### 1.3. Crear Estructura de Base de Datos MongoDB

**Colecciones necesarias:**

```javascript
// 1. users - Información de estudiantes
{
  _id: ObjectId,
  studentId: "EST-001",
  name: "BENNASRI, MAMMER PAOLO",
  email: "student@example.com",
  passwordHash: "bcrypt_hash",
  createdAt: ISODate,
  courseLevel: "A1.2-A2.1",
  active: true
}

// 2. attendance - Registros de asistencia
{
  _id: ObjectId,
  sessionId: "2025-11-13-Session-1",
  studentId: "EST-001",
  studentName: "BENNASRI, MAMMER PAOLO",
  timestamp: ISODate,
  registeredAt: ISODate,
  ipAddress: "192.168.1.1",
  course: "Curso Intensivo de Español - Nivel 3 CLM"
}

// 3. sessions - Sesiones de clase con QR
{
  _id: ObjectId,
  sessionId: "2025-11-13-Session-1",
  qrData: {...},
  createdAt: ISODate,
  expiresAt: ISODate,  // 5 minutos después
  isActive: true
}

// 4. progress - Progreso de estudiantes
{
  _id: ObjectId,
  userId: ObjectId,
  attendance: {
    totalClasses: 16,
    attendedClasses: 12,
    attendanceRate: 75,
    dates: [...]
  },
  materials: {...},
  projects: {...},
  quizScores: {...}
}
```

---

### FASE 2: Reescribir Backend con MongoDB

#### 2.1. Crear `backend_mongodb.py`

**Estructura del archivo:**

```python
# backend_mongodb.py
import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
import jwt
from dotenv import load_dotenv

# Configuración
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-this')

# Conexión MongoDB
client = MongoClient(MONGO_URI)
db = client['curso_intensivo_espanol']

# Colecciones
users_collection = db['users']
attendance_collection = db['attendance']
sessions_collection = db['sessions']
progress_collection = db['progress']

app = Flask(__name__)
CORS(app)

# Endpoints:
# POST /api/auth/register - Registrar nuevo estudiante
# POST /api/auth/login - Login de estudiante
# POST /api/attendance/session - Crear nueva sesión QR
# GET  /api/attendance/session/:id - Validar sesión QR
# POST /api/attendance/register - Registrar asistencia
# GET  /api/attendance/records - Obtener todos los registros
# GET  /api/attendance/student/:id - Asistencia de un estudiante
# GET  /api/progress/:userId - Progreso de estudiante
```

#### 2.2. Endpoints Principales

**Login y Autenticación:**
```python
@app.route('/api/auth/register', methods=['POST'])
def register():
    # Crear usuario con bcrypt hash
    # Retornar JWT token
    pass

@app.route('/api/auth/login', methods=['POST'])
def login():
    # Validar credenciales
    # Retornar JWT token
    pass
```

**Gestión de Sesiones QR:**
```python
@app.route('/api/attendance/session', methods=['POST'])
def create_qr_session():
    # Crear sesión QR válida por 5 minutos
    # Guardar en sessions_collection
    # Retornar sessionId y datos del QR
    pass

@app.route('/api/attendance/session/<session_id>', methods=['GET'])
def validate_session(session_id):
    # Validar que la sesión existe y no ha expirado
    pass
```

**Registro de Asistencia:**
```python
@app.route('/api/attendance/register', methods=['POST'])
def register_attendance():
    # Validar JWT token del estudiante
    # Validar sessionId
    # Guardar en attendance_collection
    # Actualizar progress_collection
    pass

@app.route('/api/attendance/records', methods=['GET'])
def get_all_attendance():
    # Retornar todos los registros (para admin)
    # Requiere autenticación de profesor
    pass
```

---

### FASE 3: Actualizar Frontend

#### 3.1. Crear Interfaz de Login

**Agregar a `index.html`:**

```html
<!-- Modal de Login -->
<div id="loginModal" class="modal" style="display: none;">
  <div class="modal-content">
    <h2>🔐 Login de Estudiante</h2>
    <form id="loginForm">
      <div class="form-group">
        <label>ID de Estudiante:</label>
        <input type="text" id="studentId" placeholder="EST-001" required>
      </div>
      <div class="form-group">
        <label>Contraseña:</label>
        <input type="password" id="password" required>
      </div>
      <button type="submit">Iniciar Sesión</button>
    </form>
    <div id="loginError" style="display: none; color: red;"></div>
  </div>
</div>

<script>
// JavaScript para manejar login
async function handleLogin(e) {
  e.preventDefault();
  const studentId = document.getElementById('studentId').value;
  const password = document.getElementById('password').value;

  try {
    const response = await fetch('http://localhost:5000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ studentId, password })
    });

    const data = await response.json();

    if (data.success) {
      // Guardar token
      localStorage.setItem('authToken', data.token);
      localStorage.setItem('currentUser', JSON.stringify(data.user));

      // Cerrar modal y mostrar bienvenida
      closeLoginModal();
      showWelcomeMessage(data.user.name);
    } else {
      showLoginError(data.error);
    }
  } catch (error) {
    showLoginError('Error de conexión con el servidor');
  }
}
</script>
```

#### 3.2. Conectar Generación de QR con Backend

**Actualizar función en `index.html` (aprox. línea 1358):**

```javascript
async function generateQRCode() {
  try {
    // Llamar al backend para crear sesión
    const response = await fetch('http://localhost:5000/api/attendance/session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('authToken')}`
      },
      body: JSON.stringify({
        course: 'Curso Intensivo de Español - Nivel 3 CLM',
        date: new Date().toISOString()
      })
    });

    const data = await response.json();

    if (data.success) {
      const sessionId = data.sessionId;
      const qrData = data.qrData;

      // Generar QR con URL que incluye sessionId
      const attendanceUrl = `${baseUrl}/Curso-Intensivo-Espanol/attendance-register.html?sessionId=${sessionId}`;

      document.getElementById('qr-code').innerHTML = '';
      new QRCode(document.getElementById('qr-code'), {
        text: attendanceUrl,
        width: 200,
        height: 200,
        colorDark: '#059669',
        colorLight: '#ffffff',
        correctLevel: QRCode.CorrectLevel.H
      });

      // Iniciar temporizador
      startQRTimer(300); // 5 minutos
    }
  } catch (error) {
    console.error('Error generando QR:', error);
    alert('Error al generar código QR. Intenta de nuevo.');
  }
}
```

#### 3.3. Actualizar `attendance-register.html`

**Modificar el submit del formulario:**

```javascript
async function handleAttendanceSubmit(e) {
  e.preventDefault();

  const studentId = studentSelect.value;
  const sessionId = getSessionIdFromURL();  // Extraer de URL
  const authToken = localStorage.getItem('authToken');

  if (!authToken) {
    showError('Debes iniciar sesión primero');
    return;
  }

  try {
    const response = await fetch('http://localhost:5000/api/attendance/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
      },
      body: JSON.stringify({
        sessionId: sessionId,
        studentId: studentId,
        timestamp: new Date().toISOString()
      })
    });

    const data = await response.json();

    if (data.success) {
      showSuccess('¡Asistencia registrada correctamente!');

      // Redirigir después de 2 segundos
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 2000);
    } else {
      showError(data.error || 'Error al registrar asistencia');
    }
  } catch (error) {
    console.error('Error:', error);
    showError('Error de conexión. Por favor, intenta de nuevo.');
  }
}
```

#### 3.4. Actualizar `attendance-admin.html`

**Cargar datos desde MongoDB:**

```javascript
async function loadAttendanceData() {
  const authToken = localStorage.getItem('authToken');

  try {
    const response = await fetch('http://localhost:5000/api/attendance/records', {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });

    const data = await response.json();

    if (data.success) {
      attendanceRecords = data.records;
      updateStatistics();
      displayRecords();
    } else {
      console.error('Error cargando datos:', data.error);
    }
  } catch (error) {
    console.error('Error de conexión:', error);
    // Fallback a localStorage si el backend no está disponible
    loadFromLocalStorage();
  }
}
```

---

### FASE 4: Seguridad y Configuración

#### 4.1. Variables de Entorno

**Crear archivo `.env`:**

```env
# MongoDB
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/curso_intensivo
DB_NAME=curso_intensivo_espanol

# JWT
JWT_SECRET=tu-secreto-super-seguro-cambiar-esto-12345
JWT_EXPIRATION=86400  # 24 horas en segundos

# Flask
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=otra-clave-secreta-cambiar

# CORS
ALLOWED_ORIGINS=https://elcorreveidile.github.io,http://localhost:3000

# Admin
ADMIN_PASSWORD_HASH=$2b$12$hash_del_password_admin
```

#### 4.2. Seguridad de Contraseñas

**Hashear contraseñas existentes:**

```python
import bcrypt

# Generar hashes para los estudiantes
def create_initial_passwords():
    students = [
        "EST-001", "EST-002", "EST-003", # ... todos
    ]

    for student_id in students:
        # Generar contraseña temporal: primeras 4 letras del ID
        temp_password = student_id[-3:]  # "001", "002", etc.

        # Hashear
        password_hash = bcrypt.hashpw(
            temp_password.encode('utf-8'),
            bcrypt.gensalt()
        )

        # Guardar en MongoDB
        users_collection.update_one(
            {'studentId': student_id},
            {'$set': {'passwordHash': password_hash}},
            upsert=True
        )
```

---

### FASE 5: Migración de Datos

#### 5.1. Script de Migración

**Crear `migrate_to_mongodb.py`:**

```python
#!/usr/bin/env python3
"""
Script para migrar datos de localStorage a MongoDB
"""

import json
from pymongo import MongoClient
from datetime import datetime

# Conectar a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['curso_intensivo_espanol']

# Lista de estudiantes
STUDENTS = {
    'EST-001': {'name': 'BENNASRI, MAMMER PAOLO', 'email': 'bennasri@example.com'},
    'EST-002': {'name': 'COCKRELL, JAMES RYDER', 'email': 'cockrell@example.com'},
    'EST-003': {'name': 'LU, JIAQI', 'email': 'lu@example.com'},
    'EST-004': {'name': 'MOLLAH, ALLAN SHUMON', 'email': 'mollah@example.com'},
    'EST-005': {'name': 'TJAHAJA, DYLANN', 'email': 'tjahaja@example.com'},
    'EST-006': {'name': 'WALKER, KAMRYN', 'email': 'walker@example.com'},
    'EST-007': {'name': 'WANG, XINYI', 'email': 'wang@example.com'},
    'EST-008': {'name': 'WILLIAMS, DIOR', 'email': 'williams@example.com'},
    'EST-009': {'name': 'XU, JIAHUI', 'email': 'xu@example.com'},
    'EST-010': {'name': 'ZHANG, ANJIE', 'email': 'zhang.a@example.com'},
    'EST-011': {'name': 'ZHANG, JING', 'email': 'zhang.j@example.com'},
}

def migrate_users():
    """Crear usuarios iniciales"""
    import bcrypt

    for student_id, info in STUDENTS.items():
        # Password temporal: últimos 3 dígitos del ID
        temp_password = student_id[-3:]
        password_hash = bcrypt.hashpw(temp_password.encode('utf-8'), bcrypt.gensalt())

        user_doc = {
            'studentId': student_id,
            'name': info['name'],
            'email': info['email'],
            'passwordHash': password_hash,
            'createdAt': datetime.now(),
            'courseLevel': 'A1.2-A2.1',
            'active': True
        }

        db.users.update_one(
            {'studentId': student_id},
            {'$set': user_doc},
            upsert=True
        )

        print(f"✅ Usuario creado: {student_id} - Password: {temp_password}")

def migrate_attendance_from_localstorage(json_file):
    """Migrar registros de asistencia desde archivo JSON exportado de localStorage"""
    with open(json_file, 'r') as f:
        records = json.load(f)

    for record in records:
        attendance_doc = {
            'sessionId': record.get('sessionId'),
            'studentId': record.get('studentId'),
            'studentName': record.get('studentName'),
            'timestamp': datetime.fromisoformat(record.get('timestamp').replace('Z', '+00:00')),
            'registeredAt': datetime.fromisoformat(record.get('registeredAt', record.get('timestamp')).replace('Z', '+00:00')),
            'course': record.get('course', 'Curso Intensivo de Español - Nivel 3 CLM'),
            'ipAddress': record.get('ip', 'unknown')
        }

        db.attendance.insert_one(attendance_doc)

    print(f"✅ {len(records)} registros de asistencia migrados")

if __name__ == '__main__':
    print("🚀 Iniciando migración a MongoDB...")

    # 1. Crear usuarios
    print("\n📝 Creando usuarios...")
    migrate_users()

    # 2. Migrar asistencia (si existe archivo)
    # migrate_attendance_from_localstorage('attendance_export.json')

    print("\n✅ ¡Migración completada!")
    print("\n📋 Credenciales de acceso:")
    print("   EST-001 → Password: 001")
    print("   EST-002 → Password: 002")
    print("   ... etc")
```

---

### FASE 6: Deployment y Producción

#### 6.1. Configurar GitHub Pages + Backend

**Opción 1: Backend en Render/Railway/Heroku**
```bash
# 1. Crear cuenta en Render.com (gratis)
# 2. Conectar repositorio
# 3. Configurar variables de entorno
# 4. Deploy automático
```

**Opción 2: Backend en Vercel (Serverless)**
```bash
# Crear api/ folder con endpoints como funciones serverless
vercel deploy
```

#### 6.2. Actualizar URLs en Frontend

```javascript
// config.js
const API_BASE_URL = window.location.hostname === 'localhost'
  ? 'http://localhost:5000'
  : 'https://tu-backend.onrender.com';

// Usar en todas las llamadas fetch
fetch(`${API_BASE_URL}/api/attendance/register`, {
  // ...
});
```

#### 6.3. CORS en Producción

```python
# backend_mongodb.py
from flask_cors import CORS

ALLOWED_ORIGINS = [
    'https://elcorreveidile.github.io',
    'http://localhost:3000'
]

CORS(app, resources={
    r"/api/*": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

---

## 📋 Resumen de Pasos de Implementación

### Para hacer el sistema 100% funcional:

1. **Configurar MongoDB Atlas** (15 min)
   - Crear cuenta gratis
   - Crear cluster
   - Obtener connection string

2. **Instalar dependencias** (5 min)
   ```bash
   pip install pymongo flask flask-cors bcrypt pyjwt python-dotenv
   ```

3. **Crear `backend_mongodb.py`** (2 horas)
   - Endpoints de autenticación
   - Endpoints de asistencia
   - Endpoints de progreso

4. **Crear script de migración** (30 min)
   - Migrar usuarios existentes
   - Crear contraseñas iniciales

5. **Actualizar `index.html`** (1 hora)
   - Agregar modal de login
   - Conectar generación QR con backend

6. **Actualizar `attendance-register.html`** (30 min)
   - Conectar con backend API
   - Validar JWT tokens

7. **Actualizar `attendance-admin.html`** (30 min)
   - Cargar datos desde MongoDB
   - Mantener fallback a localStorage

8. **Testing completo** (1 hora)
   - Probar login
   - Probar generación QR
   - Probar registro de asistencia
   - Verificar datos en MongoDB

9. **Deploy a producción** (1 hora)
   - Backend en Render/Railway
   - Actualizar URLs en frontend
   - Configurar CORS

---

## 🔧 Comandos Útiles

```bash
# Iniciar MongoDB local
mongod --dbpath /data/db

# Iniciar backend
python backend_mongodb.py

# Ver logs de MongoDB
tail -f /var/log/mongodb/mongod.log

# Backup de MongoDB
mongodump --uri="mongodb://localhost:27017/curso_intensivo_espanol" --out=backup/

# Restore de MongoDB
mongorestore --uri="mongodb://localhost:27017/" backup/
```

---

## 📊 Estructura Final de Archivos

```
Curso-Intensivo-Espanol/
├── backend_mongodb.py          ← Nuevo: Backend con MongoDB
├── migrate_to_mongodb.py       ← Nuevo: Script de migración
├── requirements.txt            ← Nuevo: Dependencias Python
├── .env                        ← Nuevo: Variables de entorno
├── .env.example                ← Nuevo: Ejemplo de variables
├── index.html                  ← Modificado: Agregar login
├── attendance-register.html    ← Modificado: Conectar con API
├── attendance-admin.html       ← Modificado: Cargar desde MongoDB
├── config.js                   ← Nuevo: Configuración del frontend
└── user_system.py             ← Deprecado: Ya no se usa
```

---

## ⚠️ Consideraciones de Seguridad

1. **Nunca commitear `.env`** al repositorio
2. **Usar HTTPS** en producción
3. **Rotar JWT secrets** periódicamente
4. **Implementar rate limiting** en endpoints
5. **Validar todos los inputs** en backend
6. **Usar prepared statements** con MongoDB
7. **Implementar logs de auditoría**

---

## 🎯 Próximos Pasos Sugeridos

1. **Fase 1**: Configurar MongoDB y migrar usuarios
2. **Fase 2**: Implementar backend básico con login
3. **Fase 3**: Conectar frontend de login
4. **Fase 4**: Implementar sistema de QR con backend
5. **Fase 5**: Testing y correcciones
6. **Fase 6**: Deploy a producción

---

## 📞 Soporte

Si necesitas ayuda en cualquier paso:
1. Revisa los logs del backend
2. Usa `debugCompleteSystem()` en la consola del navegador
3. Verifica la conexión a MongoDB con MongoDB Compass
4. Revisa los headers de las peticiones en Network tab

¿Quieres que empiece a implementar alguna fase específica?
