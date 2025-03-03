from database import conectar_db, guardar_conversacion
from nlp_model import analizar_texto
import whisper

# Inicializar la base de datos
conectar_db()

# Cargar modelo de Whisper
modelo_whisper = whisper.load_model("small")

# 📌 Transcribir y procesar conversación
def procesar_audio(audio_path):
    print("🎙 Transcribiendo audio...")
    result = modelo_whisper.transcribe(audio_path)
    texto = result["text"]
    
    if texto:
        print(f"📝 Transcripción: {texto}")
        guardar_conversacion(texto)  # Guardar en base de datos
        analizar_texto(texto)  # Análisis NLP
    
# 📌 Simulación (prueba con un audio grabado)
procesar_audio("audio/audio.wav")
