import logging
import os
from datetime import datetime

# Configure logging
CHATS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'chats')
LOG_FILE = os.path.join(CHATS_DIR, 'requests.log')

# Check if log file exists and is not empty
if os.path.exists(LOG_FILE):
    if os.path.getsize(LOG_FILE) > 0:
        # Rotate log file if it exists and has content
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archived_log = os.path.join(CHATS_DIR, f'requests_{timestamp}.log')
        os.rename(LOG_FILE, archived_log)

# Ensure directory exists
os.makedirs(CHATS_DIR, exist_ok=True)

# Configure fresh logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Write initial header if file is new/empty
        if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
            logging.info("===== NEW LOG SESSION STARTED =====")
            logging.info("Timestamp - User - Path - Method - IP Address")

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = (
            f"User: {user} - "
            f"Path: {request.path} - "
            f"Method: {request.method} - "
            f"IP: {request.META.get('REMOTE_ADDR')}"
        )
        logging.info(log_message)
        
        response = self.get_response(request)
        return response