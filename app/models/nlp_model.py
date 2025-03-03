import spacy

# Cargar modelo en español
nlp = spacy.load("es_core_news_sm")

# 📌 Analizar texto con NLP
def analizar_texto(texto):
    doc = nlp(texto)
    
    entidades = [(ent.text, ent.label_) for ent in doc.ents]  # Extrae entidades nombradas
    palabras_clave = [token.lemma_ for token in doc if not token.is_stop]  # Extrae palabras clave
    
    print("🔍 Análisis NLP:")
    print("📌 Entidades:", entidades)
    print("📌 Palabras clave:", palabras_clave)
    
    return {
        "entidades": entidades,
        "palabras_clave": palabras_clave
    }
