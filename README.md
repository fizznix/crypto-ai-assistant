# crypto-ai-assistant

## About the App
This app is designed to create a simple tool-calling agent from scratch. It leverages AI capabilities to interact with various tools and APIs, providing a seamless user experience. The app makes use of tool calling to get the crypto prices from [CoinCap API](https://api.coincap.io/v2/assets).

## Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create the `.env` file:**
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Update the `.env` file with your configuration.

## Running the App

### Command Line Interface (CLI)
You can run the app via the CLI using `main.py`:
```bash
python main.py
```

### Streamlit Interface
You can run the app using Streamlit with `chat_interface.py`:
```bash
streamlit run chat_interface.py
```

## Together AI API Key
To use the Together AI API, you need to obtain an API key. You can get the API key from the [Together AI website](https://api.together.ai/). Sign-up/sign-in and generate the api key.
