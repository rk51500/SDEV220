"""
ASGI config for student_registration_project.
"""

import os

from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_registration_project.settings")

application = get_asgi_application()
