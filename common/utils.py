import pydash
import socket
from django.apps import apps
from django.conf import settings
from urllib.parse import urljoin


class Utils:
    @staticmethod
    def url(path):
        return urljoin(settings.APP_URL, path)

    @staticmethod
    def static_url(path):
        if apps.is_installed('django.contrib.staticfiles'):
            from django.contrib.staticfiles.storage import staticfiles_storage

            query = pydash.substr_right(path, '?') if '?' in path else ''
            path = pydash.substr_left(path, '?')
            url = staticfiles_storage.url(path)

            if len(query.strip()) > 0:
                url += '?' + query

            if url.startswith('/'):
                return Utils.url(url)

            return url
        else:
            return urljoin(Utils.url(settings.STATIC_URL), path)

    @staticmethod
    def media_url(path=''):
        path = path.replace(settings.MEDIA_ROOT, '')
        if path.startswith('/'):
            path = pydash.replace_start(path, '/', '')
        return urljoin(Utils.url(settings.MEDIA_URL), path)

    @staticmethod
    def check_host_port_availability(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        try:
            s.connect((ip, int(port)))
            s.shutdown(socket.SHUT_RDWR)
            return False
        except:
            return True
        finally:
            s.close()


class Str:
    @staticmethod
    def contains(text, subs, strict=False):
        text = str(text)

        if not strict:
            text = text.lower()

        for sub in subs:
            sub = str(sub)

            if not strict:
                sub = sub.lower()

            if sub in text:
                return True
        return False


class ServiceProvider:
    def __init__(self):
        self.__services = {}
        self.__instances = {}

    def register(self, name, service_class):
        self.__services[name] = service_class

    def instance(self, name, obj):
        self.__instances[name] = obj

    def make(self, name, *args, **kwargs):
        if name in self.__instances:
            return self.__instances[name]

        return self.create(name, args, kwargs)

    def create(self, name, *args, **kwargs):
        if name not in self.__services:
            raise Exception("No service registered with the name '%s'." % name)

        return self.__services[name](*args, **kwargs)


service_provider = ServiceProvider()
