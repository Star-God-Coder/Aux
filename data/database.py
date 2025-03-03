import sqlite3
from datetime import datetime

# 📌 Conectar con la base de datos
def conectar_db():
    conn = sqlite3.connect("data/asistente.db")
    cursor = conn.cursor()
    
    # Crear tabla si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texto TEXT NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

# 📌 Guardar transcripción en la base de datos
def guardar_conversacion(texto):
    conn = sqlite3.connect("data/asistente.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO conversaciones (texto, fecha) VALUES (?, ?)", (texto, datetime.now()))
    
    conn.commit()
    conn.close()
    print("✅ Conversación guardada en la base de datos")

# 📌 Mostrar todas las conversaciones guardadas
def obtener_conversaciones():
    conn = sqlite3.connect("data/asistente.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM conversaciones ORDER BY fecha DESC")
    conversaciones = cursor.fetchall()
    
    conn.close()
    return conversaciones
