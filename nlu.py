import yaml
import re

# Kommentti: Tallennetaan keskustelun konteksti

dialog_context = {}

# Kommentti: Ladataan konfiguraatio YAML-tiedostosta
def load_config():
    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: config.yaml file not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error reading YAML file: {e}")
        return None

# Kommentti: Tekstin tulkintafunktio
def interpret(text):
    config = load_config()
    if not config:
        return None  # Kommentti: Turvallinen palautus, jos konfiguraatio puuttuu

    text = text.lower()
    intent_data = {}

    # Kommentti: Tarkistetaan, onko kysymys säästä
    if "weather" in text:
        city = None
        for word in text.split():
            if word in ["moscow", "paris", "london", "kyiv", "berlin"]:
                city = word
                break

        if not city and "last_city" in dialog_context:
            city = dialog_context["last_city"]

        if city:
            dialog_context["last_city"] = city
            return {"action": "get_weather", "city": city}
        else:
            return None

    # Kommentti: Yleinen logiikka config.yaml:n perusteella
    for intent, data in config.get("intents", {}).items():
        for keyword in data.get("keywords", []):
            pattern = r'\\b' + re.escape(keyword.lower()) + r'\\b'
            if re.search(pattern, text):
                return {"action": intent}

    # Kommentti: 🧠 Jos mitään ei löytynyt — lähetetään GPT:lle
    return {"action": "ask_anything"}