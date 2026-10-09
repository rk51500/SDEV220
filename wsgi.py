"""
WSGI config for student_registration_project.
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_registration_project.settings")

application = get_wsgi_application()
