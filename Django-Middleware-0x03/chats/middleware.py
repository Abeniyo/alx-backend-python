import logging
import os
from datetime import datetime

CHATS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'chats')
LOG_FILE = os.path.join(CHATS_DIR, 'requests.log')

os.makedirs(CHATS_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

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
