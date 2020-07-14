import os
import inspect
import dotenv

from django.core.wsgi import get_wsgi_application

# Load settings from possible .env file
try:
    inspect_file = inspect.getfile(inspect.currentframe())
    env_path = os.path.dirname(os.path.abspath(inspect_file))
    env_file = "%s/../.env" % (env_path,)

    if os.path.exists(env_file):
        dotenv.load_dotenv(env_file)
except Exception as e:
    pass

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_wsgi_application()
