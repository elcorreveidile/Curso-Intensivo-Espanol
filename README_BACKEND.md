# Backend MongoDB - Curso Intensivo de Español

Sistema de gestión de estudiantes, asistencia y progreso académico con MongoDB.

## 🚀 Inicio Rápido

### 1. Requisitos Previos

- Python 3.8 o superior
- MongoDB (local o MongoDB Atlas)
- pip (gestor de paquetes de Python)

### 2. Instalación

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 3. Ejecutar migración inicial
python migrate_to_mongodb.py

# 4. Iniciar servidor
python backend_mongodb.py
```

El servidor estará disponible en: `http://localhost:5000`

---

## 📋 Configuración

### MongoDB Atlas (Recomendado - Gratis)

1. **Crear cuenta en MongoDB Atlas:**
   - Ir a https://www.mongodb.com/cloud/atlas
   - Crear cuenta gratuita
   - Crear nuevo cluster (tier gratuito)

2. **Obtener connection string:**
   - En Atlas, click en "Connect"
   - Seleccionar "Connect your application"
   - Copiar el connection string
   - Formato: `mongodb+srv://user:password@cluster.mongodb.net/`

3. **Configurar en .env:**
   ```env
   MONGO_URI=mongodb+srv://tu_usuario:tu_password@cluster.mongodb.net/curso_intensivo_espanol
   ```

### MongoDB Local

```bash
# Instalar MongoDB
# Ubuntu/Debian:
sudo apt-get install mongodb

# macOS:
brew install mongodb-community

# Iniciar servicio
sudo systemctl start mongodb  # Linux
brew services start mongodb-community  # macOS

# Usar en .env:
MONGO_URI=mongodb://localhost:27017/
```

---

## 🔐 Seguridad

### Generar Claves Secretas

```bash
# JWT Secret
python -c "import secrets; print(secrets.token_hex(32))"

# Admin Password Hash
python -c "import bcrypt; print(bcrypt.hashpw(b'ugr2024', bcrypt.gensalt()).decode())"
```

Agregar a `.env`:
```env
JWT_SECRET=tu_clave_secreta_generada
ADMIN_PASSWORD_HASH=$2b$12$hash_generado
```

---

## 📊 Estructura de la Base de Datos

### Colecciones

#### 1. `users` - Estudiantes
```javascript
{
  _id: ObjectId,
  studentId: "EST-001",
  name: "BENNASRI, MAMMER PAOLO",
  email: "student@ugr.es",
  passwordHash: "bcrypt_hash",
  createdAt: ISODate,
  courseLevel: "A1.2-A2.1",
  active: true
}
```

#### 2. `attendance` - Asistencia
```javascript
{
  _id: ObjectId,
  sessionId: "2025-11-13-Session-abc123",
  studentId: "EST-001",
  studentName: "BENNASRI, MAMMER PAOLO",
  timestamp: ISODate,
  registeredAt: ISODate,
  course: "Curso Intensivo de Español",
  ipAddress: "192.168.1.1"
}
```

#### 3. `sessions` - Sesiones QR
```javascript
{
  _id: ObjectId,
  sessionId: "2025-11-13-Session-abc123",
  course: "Curso Intensivo de Español",
  createdAt: ISODate,
  expiresAt: ISODate,  // +5 minutos
  isActive: true,
  qrData: {...}
}
```

#### 4. `progress` - Progreso Académico
```javascript
{
  _id: ObjectId,
  userId: ObjectId,
  studentId: "EST-001",
  attendance: {
    totalClasses: 16,
    attendedClasses: 8,
    attendanceRate: 50,
    dates: [...]
  },
  materials: {...},
  projects: {...},
  quizScores: {...},
  lastUpdated: ISODate
}
```

---

## 🔌 API Endpoints

### Base URL
```
http://localhost:5000/api
```

### Autenticación

#### Registrar Nuevo Estudiante
```http
POST /api/auth/register
Content-Type: application/json

{
  "studentId": "EST-001",
  "name": "BENNASRI, MAMMER PAOLO",
  "email": "student@ugr.es",
  "password": "password123",
  "courseLevel": "A1.2-A2.1"
}

Response:
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {...}
}
```

#### Login de Estudiante
```http
POST /api/auth/login
Content-Type: application/json

{
  "studentId": "EST-001",
  "password": "001"
}

Response:
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "studentId": "EST-001",
    "name": "BENNASRI, MAMMER PAOLO",
    "email": "student@ugr.es"
  }
}
```

#### Login de Administrador
```http
POST /api/auth/admin-login
Content-Type: application/json

{
  "password": "ugr2024"
}

Response:
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "admin": true
}
```

### Asistencia

#### Crear Sesión QR (Admin)
```http
POST /api/attendance/session
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "course": "Curso Intensivo de Español - Nivel 3 CLM"
}

Response:
{
  "success": true,
  "sessionId": "2025-11-13-Session-abc123",
  "qrData": {...},
  "expiresIn": 300
}
```

#### Validar Sesión QR
```http
GET /api/attendance/session/{sessionId}

Response:
{
  "success": true,
  "session": {
    "sessionId": "2025-11-13-Session-abc123",
    "course": "Curso Intensivo de Español",
    "createdAt": "2025-11-13T12:30:00Z",
    "expiresAt": "2025-11-13T12:35:00Z"
  }
}
```

#### Registrar Asistencia
```http
POST /api/attendance/register
Authorization: Bearer <student_token>
Content-Type: application/json

{
  "sessionId": "2025-11-13-Session-abc123"
}

Response:
{
  "success": true,
  "message": "Asistencia registrada correctamente",
  "attendance": {
    "sessionId": "2025-11-13-Session-abc123",
    "timestamp": "2025-11-13T12:31:00Z"
  }
}
```

#### Obtener Todos los Registros (Admin)
```http
GET /api/attendance/records?sessionId=xxx&studentId=EST-001
Authorization: Bearer <admin_token>

Response:
{
  "success": true,
  "records": [...],
  "count": 25
}
```

#### Obtener Asistencia de un Estudiante
```http
GET /api/attendance/student/{studentId}
Authorization: Bearer <student_token>

Response:
{
  "success": true,
  "records": [...],
  "count": 8
}
```

### Progreso

#### Obtener Progreso de Estudiante
```http
GET /api/progress/{studentId}
Authorization: Bearer <student_token>

Response:
{
  "success": true,
  "progress": {
    "studentId": "EST-001",
    "attendance": {...},
    "materials": {...},
    "projects": {...},
    "quizScores": {...}
  }
}
```

#### Actualizar Progreso de Material
```http
POST /api/progress/material
Authorization: Bearer <student_token>
Content-Type: application/json

{
  "materialType": "vocabulary",
  "itemId": "vocab-session-1-colors"
}

Response:
{
  "success": true,
  "message": "Progreso actualizado"
}
```

#### Registrar Resultado de Quiz
```http
POST /api/progress/quiz
Authorization: Bearer <student_token>
Content-Type: application/json

{
  "quizId": "quiz-session-1",
  "correctAnswers": 4,
  "totalQuestions": 5
}

Response:
{
  "success": true,
  "message": "Quiz registrado",
  "result": {
    "quizId": "quiz-session-1",
    "accuracy": 80,
    "date": "2025-11-13T12:45:00Z"
  }
}
```

### Administrativo

#### Obtener Lista de Estudiantes (Admin)
```http
GET /api/students
Authorization: Bearer <admin_token>

Response:
{
  "success": true,
  "students": [
    {
      "studentId": "EST-001",
      "name": "BENNASRI, MAMMER PAOLO",
      "email": "student@ugr.es",
      "attendance": {...},
      "materialsCompletion": 45.5,
      "quizAccuracy": 82.3
    },
    ...
  ],
  "count": 11
}
```

### Salud del Sistema

#### Health Check
```http
GET /api/health

Response:
{
  "success": true,
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-11-13T12:30:00Z"
}
```

---

## 🧪 Testing con curl

### Test Login
```bash
# Login de estudiante
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"studentId": "EST-001", "password": "001"}'

# Guardar token
export TOKEN="token_obtenido_del_login"
```

### Test Asistencia
```bash
# Login de admin
curl -X POST http://localhost:5000/api/auth/admin-login \
  -H "Content-Type: application/json" \
  -d '{"password": "ugr2024"}'

export ADMIN_TOKEN="token_admin"

# Crear sesión QR
curl -X POST http://localhost:5000/api/attendance/session \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"course": "Curso Intensivo de Español"}'

# Registrar asistencia
curl -X POST http://localhost:5000/api/attendance/register \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "session_id_obtenido"}'
```

### Test Progreso
```bash
# Obtener progreso
curl http://localhost:5000/api/progress/EST-001 \
  -H "Authorization: Bearer $TOKEN"

# Registrar material completado
curl -X POST http://localhost:5000/api/progress/material \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"materialType": "vocabulary", "itemId": "vocab-1"}'
```

---

## 🐛 Troubleshooting

### Error: "No module named 'pymongo'"
```bash
pip install -r requirements.txt
```

### Error: "Connection refused" al conectar a MongoDB
```bash
# Verificar que MongoDB está corriendo
sudo systemctl status mongodb  # Linux
brew services list  # macOS

# Iniciar MongoDB si está detenido
sudo systemctl start mongodb  # Linux
brew services start mongodb-community  # macOS
```

### Error: "Authentication failed" en MongoDB Atlas
- Verificar que el connection string es correcto
- Verificar usuario y contraseña
- Verificar que la IP está en la whitelist (0.0.0.0/0 para permitir todas)

### Error: "Token expired"
- El token JWT expira después de 24 horas (configurable)
- Hacer login nuevamente para obtener nuevo token

### Ver logs del backend
```bash
# El backend imprime logs en la consola
python backend_mongodb.py

# Para logs detallados, activar debug en .env:
FLASK_DEBUG=True
```

---

## 📦 Deployment

### Render.com (Recomendado - Gratis)

1. **Crear cuenta en Render:**
   - Ir a https://render.com
   - Conectar tu repositorio de GitHub

2. **Crear nuevo Web Service:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python backend_mongodb.py`

3. **Configurar Environment Variables:**
   - Agregar todas las variables de `.env`
   - Usar MongoDB Atlas para la base de datos

4. **Deploy:**
   - Render hace deploy automático al hacer push

### Railway.app (Alternativa)

Similar a Render, conectar repo y configurar variables de entorno.

### Vercel (Serverless)

Requiere restructurar como funciones serverless. No recomendado para este proyecto.

---

## 📚 Recursos Adicionales

- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PyMongo Tutorial](https://pymongo.readthedocs.io/)
- [JWT.io](https://jwt.io/) - Para decodificar tokens

---

## 🆘 Soporte

Si encuentras problemas:

1. Revisa los logs del backend
2. Verifica que MongoDB está corriendo
3. Verifica las variables de entorno en `.env`
4. Prueba los endpoints con curl primero
5. Revisa la consola del navegador para errores CORS

---

## 🔒 Seguridad en Producción

### Checklist de Seguridad:

- [ ] Cambiar JWT_SECRET a un valor seguro y aleatorio
- [ ] Cambiar ADMIN_PASSWORD_HASH
- [ ] Usar HTTPS en producción
- [ ] Configurar CORS solo para dominios permitidos
- [ ] Habilitar rate limiting
- [ ] Revisar logs regularmente
- [ ] Hacer backups de la base de datos
- [ ] No exponer .env al repositorio

---

## 📊 Mantenimiento

### Backup de MongoDB

```bash
# Backup completo
mongodump --uri="mongodb://localhost:27017/curso_intensivo_espanol" --out=backup/

# Restore
mongorestore --uri="mongodb://localhost:27017/" backup/
```

### Ver estadísticas

```javascript
// En MongoDB shell
use curso_intensivo_espanol

// Contar usuarios
db.users.count()

// Contar registros de asistencia
db.attendance.count()

// Estudiantes más activos
db.attendance.aggregate([
  { $group: { _id: "$studentId", count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 5 }
])
```

---

Creado para el Curso Intensivo de Español - Nivel 3 CLM
Universidad de Granada - Centro de Lenguas Modernas
© 2025
