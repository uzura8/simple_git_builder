import os
from app.common.file import get_file_time
from app.common.site.util import static_dir_path


def url_static(under_static_path):
    uri_path = static_dir_path(under_static_path)
    os_path = os.path.join('app', uri_path.lstrip('/'))
    asset_hash = get_file_time(os_path)
    return '{}?{}'.format(uri_path, asset_hash)
