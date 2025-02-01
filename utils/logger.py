import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logger
logger = logging.getLogger('crypto_ai_assistant')
logger.setLevel(logging.DEBUG)

# Create a file handler that logs debug and higher level messages
handler = TimedRotatingFileHandler('logs/log.log', when='midnight', interval=1)
handler.suffix = "%Y-%m-%d"
handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the file handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(handler)