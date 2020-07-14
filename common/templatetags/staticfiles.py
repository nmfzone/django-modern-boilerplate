import json
import os
import pydash
import logging
from common.utils import Utils
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()
logger = logging.getLogger('django')


@register.simple_tag
def mix(path, manifest_directory=''):
    manifests = {}

    if not path.startswith('/'):
        path = '/%s' % path

    if manifest_directory and not manifest_directory.startswith('/'):
        manifest_directory = '/%s' % manifest_directory

    hot_file = os.path.join(settings.BASE_DIR, 'public/static', manifest_directory, 'hot')

    if os.path.exists(hot_file):
        with open(hot_file, 'r') as file:
            data = file.read()

            url = data.rstrip()

            if url.startswith('http://') or url.startswith('https://'):
                return mark_safe(pydash.substr_right(url, ':') + path)

        return mark_safe('//localhost:8080%s' % path)

    manifest_path = os.path.join(settings.BASE_DIR, 'public/static', manifest_directory, 'mix-manifest.json')

    if manifest_path not in manifests:
        if not os.path.exists(manifest_path):
            raise Exception('The Mix manifest does not exist.')

        with open(manifest_path, 'r') as file:
            data = file.read()

            manifests[manifest_path] = json.loads(data)

    manifest = manifests[manifest_path]

    if path not in manifest:
        exception = Exception('Unable to locate Mix file: %s.' % path)

        if not settings.DEBUG:
            logger.error(str(exception))

            return path
        else:
            raise exception

    return mark_safe(Utils.static_url(manifest_directory + manifest[path]))
