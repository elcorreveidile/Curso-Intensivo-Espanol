#!/usr/bin/env python3
"""
Script para iniciar el servidor de gestión de usuarios
"""

import subprocess
import sys
import os
import webbrowser
import time
from threading import Thread

def check_requirements():
    """Verificar que los requisitos están instalados"""
    try:
        import flask
        import flask_cors
        print("✅ Requisitos encontrados")
        return True
    except ImportError as e:
        print(f"❌ Falta el requisito: {e}")
        print("📦 Instalando requisitos...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-cors"])
        return True

def start_server():
    """Iniciar el servidor Flask"""
    print("🚀 Iniciando servidor de gestión de usuarios...")
    print("📍 URL: http://localhost:5000")
    print("📚 API endpoints:")
    print("   POST /api/register - Registrar nuevo usuario")
    print("   POST /api/login - Iniciar sesión")
    print("   GET  /api/progress/<user_id> - Obtener progreso")
    print("   POST /api/attendance - Registrar asistencia")
    print("   POST /api/materials - Actualizar materiales")
    print("   POST /api/quiz - Registrar quiz")
    print("   POST /api/projects - Completar proyecto")
    print("\n🔄 Servidor iniciado. Presiona Ctrl+C para detener.")
    print("💡 Puedes mantener esta ventana abierta mientras usas la web.")

    # Importar y ejecutar el servidor
    from user_system import app

    try:
        app.run(debug=True, port=5000, threaded=True)
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")

def show_usage_instructions():
    """Mostrar instrucciones de uso"""
    print("\n" + "="*60)
    print("📖 INSTRUCCIONES DE USO")
    print("="*60)
    print("1️⃣ Este script inicia el servidor de gestión de usuarios")
    print("2️⃣ Abre 'index.html' en tu navegador para ver la web")
    print("3️⃣ Los estudiantes pueden:")
    print("   • Registrarse con nombre y email")
    print("   • Iniciar sesión con su ID y contraseña")
    print("   • Ver su progreso personal")
    print("   • Guardar actividades realizadas")
    print("4️⃣ Los datos se guardan en archivos JSON:")
    print("   • users_database.json - Usuarios registrados")
    print("   • progress_database.json - Progreso individual")
    print("5️⃣ Mantén este servidor corriendo mientras usas la web")
    print("="*60)

if __name__ == "__main__":
    print("🎯 Sistema de Gestión de Usuarios - Curso Intensivo de Español")
    print("="*60)

    # Verificar requisitos
    if not check_requirements():
        print("❌ No se pudieron instalar los requisitos")
        sys.exit(1)

    # Mostrar instrucciones
    show_usage_instructions()

    # Esperar un momento para que el usuario lea
    try:
        input("\n⏱️ Presiona Enter para iniciar el servidor...")
    except KeyboardInterrupt:
        print("\n👋 Operación cancelada")
        sys.exit(0)

    # Iniciar el servidor
    start_server()