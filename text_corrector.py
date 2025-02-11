import requests
import json
import sys
import argparse

# Sprachspezifische Prompts
PROMPTS = {
    'de': """
    Bitte korrigiere den folgenden deutschen Text bezüglich Rechtschreibung, 
    Grammatik, Zeichensetzung und Groß-/Kleinschreibung. Der Text stammt aus einer Transkription. 
    Es ist möglich, dass du einzelne Worte noch aus dem Kontext des Satzes korrigieren musst.
    Gib nur den korrigierten Text zurück, keine Erklärungen:
    """,
    
    'en': """
    Please correct the following English text for spelling, 
    grammar, punctuation, and capitalization. The text is from a transcription.
    You may need to correct individual words based on the context of the sentence.
    Return only the corrected text, no explanations:
    """
}

# Standard-Modelle für verschiedene Sprachen
DEFAULT_MODELS = {
    'de': 'mistral',
    'en': 'llama2:13b'
}

def correct_text(text: str, language: str = 'de', model: str = None, 
                temperature: float = 0.7, top_p: float = 0.9, top_k: int = 40) -> str:
    """
    Sendet Text an lokales Ollama Modell zur Korrektur.
    
    Args:
        text (str): Zu korrigierender Text
        language (str): Sprache des Textes ('de' oder 'en')
        model (str): Zu verwendendes Modell (Optional)
        temperature (float): Kreativität/Zufälligkeit (0.0 bis 1.0)
        top_p (float): Nucleus Sampling Parameter (0.0 bis 1.0)
        top_k (int): Anzahl der Token-Kandidaten (1 bis 100)
    """
    url = "http://localhost:11434/api/generate"
    
    # Wähle das passende Modell
    selected_model = model if model else DEFAULT_MODELS[language]
    
    # Wähle den passenden Prompt
    prompt = f"{PROMPTS[language]}\n\n{text}"
    
    data = {
        "model": selected_model,
        "prompt": prompt,
        "stream": False,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Prüfe auf HTTP-Fehler
        result = response.json()
        return result['response']
    except requests.exceptions.RequestException as e:
        return f"Fehler bei der Verbindung zu Ollama: {str(e)}"
    except (KeyError, json.JSONDecodeError) as e:
        return f"Fehler bei der Verarbeitung der Antwort: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description='Textkorrektur mit Ollama')
    parser.add_argument('file', help='Pfad zur Textdatei')
    parser.add_argument('--language', '-l', choices=['de', 'en'], default='de',
                      help='Sprache des Textes (de/en, Standard: de)')
    parser.add_argument('--model', '-m', help='Ollama Modell (Standard: abhängig von Sprache)')
    parser.add_argument('--temperature', '-t', type=float, default=0.7,
                      help='Kreativität/Zufälligkeit (0.0 bis 1.0, Standard: 0.7)')
    parser.add_argument('--top-p', '-p', type=float, default=0.9,
                      help='Nucleus Sampling Parameter (0.0 bis 1.0, Standard: 0.9)')
    parser.add_argument('--top-k', '-k', type=int, default=40,
                      help='Anzahl der Token-Kandidaten (1 bis 100, Standard: 40)')
    
    args = parser.parse_args()
    
    # Validiere Parameter
    if not 0.0 <= args.temperature <= 1.0:
        print("Fehler: Temperature muss zwischen 0.0 und 1.0 liegen")
        sys.exit(1)
    if not 0.0 <= args.top_p <= 1.0:
        print("Fehler: Top-P muss zwischen 0.0 und 1.0 liegen")
        sys.exit(1)
    if not 1 <= args.top_k <= 100:
        print("Fehler: Top-K muss zwischen 1 und 100 liegen")
        sys.exit(1)
    
    try:
        print(f"Versuche Datei zu öffnen: {args.file}")
        with open(args.file, 'r', encoding='utf-8') as file:
            text = file.read().strip()
            print(f"Dateigröße: {len(text)} Zeichen")

        if not text:
            print("Fehler: Die Eingabedatei ist leer!")
            sys.exit(1)
        
        # Zeige verwendetes Modell
        model = args.model if args.model else DEFAULT_MODELS[args.language]
        print(f"\nVerwendetes Modell: {model}")
        print(f"Sprache: {args.language}")
        
        print("\nOriginal Text:")
        print("-" * 40)
        print(text)
        print("-" * 40)
        
        print("\nKorrigierter Text (Parameter: temp={:.1f}, top_p={:.1f}, top_k={:d}):".format(
            args.temperature, args.top_p, args.top_k))
        print("-" * 40)
        print(correct_text(text, args.language, args.model, 
                         args.temperature, args.top_p, args.top_k))
        print("-" * 40)
    except FileNotFoundError:
        print(f"Fehler: Datei '{args.file}' wurde nicht gefunden.")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Fehler: Die Datei konnte nicht als UTF-8 gelesen werden.")
        sys.exit(1)
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
