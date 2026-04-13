import os
import sys
from pathlib import Path

# Ensure Django project root is importable in Vercel runtime
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game_platform.settings")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
