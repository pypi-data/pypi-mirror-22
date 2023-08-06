import pip
import semver
import pkg_resources
from urllib.parse import urlparse

from pipper import downloader


def parse_url(wheel_url: str) -> dict:
    """ """

    url_data = urlparse(wheel_url)
    path_parts = url_data.path.strip('/').split('/')

    return dict(
        url=wheel_url,
        wheel_filename=path_parts[-1],
        version=path_parts[-2].replace('-', '.'),
        package_name=path_parts[-3]
    )


def update_required(wheel_url: str) -> bool:
    """ """

    data = parse_url(wheel_url)
    existing = status(data['package_name'])

    if not existing:
        return True

    result = semver.compare(data['version'], existing.version)
    return result != 0


def status(package_name: str):
    """ """

    try:
        return pkg_resources.get_distribution(package_name)
    except pkg_resources.DistributionNotFound:
        return None
    except Exception:
        raise


def install(package_name: str):
    """ """

    pip.main(['install', package_name])


def install_wheel(wheel_url: str):
    """ """

    wheel_path = downloader.to_temp_file(wheel_url)
    install(wheel_path)
