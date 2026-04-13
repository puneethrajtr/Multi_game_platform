import os
DJANGO_SETTINGS_MODULE = game_platform.settings and app = get_wsgi_application()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_platform.settings')

app = get_wsgi_application()
