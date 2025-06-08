import logging
import os
from datetime import datetime, timedelta
from collections import defaultdict
from django.http import HttpResponseForbidden
from django.utils.timezone import now

# Setup log file path
CHATS_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(CHATS_DIR, 'requests.log')

# Rotate old log if it exists and is not empty
#if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
#    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#    os.rename(LOG_FILE, os.path.join(CHATS_DIR, f'requests_{timestamp}.log'))
if os.path.exists(LOG_FILE):
    if os.path.getsize(LOG_FILE) > 0:  # Rotate non-empty logs
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        os.rename(LOG_FILE, os.path.join(CHATS_DIR, f'requests_{timestamp}.log'))
    else:  # Delete empty logs
        os.remove(LOG_FILE)



# Ensure directory exists
os.makedirs(CHATS_DIR, exist_ok=True)

# Logging config
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 1. Logging User Requests
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
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
        return self.get_response(request)

# 2. Restrict Chat Access by time
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if request.path.startswith('/chat') and not (18 <= current_hour < 21):
            return HttpResponseForbidden("Access to chat is restricted at this time.")
        return self.get_response(request)

# 3. Detect and Block Offensive Language (Rate Limiting)
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_counts = defaultdict(list)

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/chat'):
            ip = request.META.get('REMOTE_ADDR')
            current_time = now()
            # Clean up messages older than 1 minute
            self.message_counts[ip] = [
                t for t in self.message_counts[ip]
                if current_time - t < timedelta(minutes=1)
            ]
            if len(self.message_counts[ip]) >= 5:
                return HttpResponseForbidden("Too many messages sent. Please wait.")
            self.message_counts[ip].append(current_time)

        return self.get_response(request)

# 4. Enforce Chat User Role Permissions
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/chat'):
            user = request.user
            if not user.is_authenticated or getattr(user, 'role', '') not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to access this chat.")
        return self.get_response(request)
