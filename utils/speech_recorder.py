import whisper
import sounddevice as sd
import numpy as np
import wave
import time
import queue

# Configuración
samplerate = 44100  # Frecuencia de muestreo
silence_threshold = 100  # Nivel de silencio (ajustable)
silence_duration = 5  # Segundos de silencio antes de detener grabación
auto_mode = True  # Modo automático activado por defecto
audio_queue = queue.Queue()

# 📌 Función para detectar sonido y grabar automáticamente
def grabar_audio():
    global auto_mode
    print("🎙 Modo Automático Activo: Esperando sonido...")
    
    while True:
        recording = []
        silence_counter = 0
        start_time = time.time()
        
        while True:
            audio = sd.rec(int(samplerate * 0.5), samplerate=samplerate, channels=1, dtype=np.int16)
            sd.wait()
            volume = np.abs(audio).mean()
            
            if volume > silence_threshold:
                recording.append(audio)
                silence_counter = 0  # Reiniciar contador de silencio
            else:
                silence_counter += 0.5  # Sumar tiempo de silencio
            
            # ⏹ Detener grabación tras X segundos de silencio
            if silence_counter >= silence_duration:
                break

        # Guardar audio solo si se grabó algo
        if recording:
            audio_data = np.concatenate(recording, axis=0)
            wavefile = wave.open("audio/audio.wav", "wb")
            wavefile.setnchannels(1)
            wavefile.setsampwidth(2)
            wavefile.setframerate(samplerate)
            wavefile.writeframes(audio_data.tobytes())
            wavefile.close()
            print("✅ Audio grabado y guardado como 'audio.wav'")
            
            # Añadir a la cola para procesamiento
            audio_queue.put("audio/audio.wav")

# 📝 Transcribir audio con Whisper
def transcribir_audio():
    model = whisper.load_model("small")
    
    while True:
        if not audio_queue.empty():
            audio_file = audio_queue.get()
            result = model.transcribe(audio_file)
            print("📝 Transcripción:", result["text"])
            
            # 🔄 Activar comandos de voz
            procesar_comando(result["text"])

# 🎤 Procesar comandos de voz
def procesar_comando(texto):
    global auto_mode
    texto = texto.lower()
    
    if "activar modo automático" in texto:
        auto_mode = True
        print("🔊 Modo automático activado.")
    elif "desactivar modo automático" in texto:
        auto_mode = False
        print("🔇 Modo automático desactivado.")
