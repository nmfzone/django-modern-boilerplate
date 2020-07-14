from urllib.parse import urlsplit
from common.utils import Utils


def common_context_processor(request):
    return {
        'current_uri_': request.get_raw_uri(),
        'current_url_': request.build_absolute_uri('?'),
        'current_url_full_path_': request.get_full_path(),
        'current_url_path_': urlsplit('//%s' % request.get_full_path()).path,
        'current_page_': int(request.GET.get('page', 1)),
        'STATIC_URL': Utils.static_url('/')
    }
