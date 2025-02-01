import requests

from config import MODEL
from utils.llm import call_llm

AVAIALBLE_TOOLS_FORMAT = [
    {
        "type": "function",
        "function": {
            "name": "get_coin_price",
            "description": "Retrieves the price of a specified cryptocurrency from the CoinCap API",
            "parameters": {
                "type": "object",
                "properties": {
                    "coin_name": {
                        "type": "string",
                        "description": "The name of the cryptocurrency to retrieve the price for"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "translate_to_english",
            "description": "Use the tool when non-english user query is used, helps in converting the input text to English.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to be translated to English"
                    }
                }
            }
        }
    }
]

def get_coin_price(coin_name: str) -> str:
    """
    Retrieves the price of a specified cryptocurrency from the CoinCap API.

    Args:
        coin_name (str): The name of the cryptocurrency to retrieve the price for.

    Returns:
        str: The price of the specified cryptocurrency in USD if found, 
             otherwise a message indicating that the coin data was not available.
    """
    url = "https://api.coincap.io/v2/assets"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        for coin in data:
            if any([coin['name'].lower() == coin_name.lower(), coin['symbol'].lower() == coin_name.lower()]):
                return f"Current price of {coin_name} is {coin['priceUsd']} USD."
        return "Coin data not available"
    else:
        return "Failed to retrieve data"
    

def translate_to_english(text: str) -> str:
    """
    Detect the language of the input text and translate it to English.
    """
    try:
        # Use Together AI to detect and translate
        prompt = f"""Translate the following user_input to English. If the input is already in English, return the same text.
        Your task is only to translate the text to English, not come up with translation with other languages.
        
        user_input : `{text}`"""
        messages = [{
            "role": "assistant",
            "content": prompt
        }]
        translated_text = call_llm(MODEL, messages)
        return translated_text.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Error translating text: {e}")