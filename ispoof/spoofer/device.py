from pathlib import Path
from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.cli.mounter import MobileImageMounterService
from pymobiledevice3.cli.developer import DtSimulateLocation
from pymobiledevice3.services.diagnostics import DiagnosticsService
from pymobiledevice3.exceptions import PasscodeRequiredError
import logging
import requests
import tempfile
import zipfile
from tqdm import tqdm
from ispoof.utils import get_home_folder
from ispoof.spoofer.location import Location

DEVELOPER_DISK_IMAGE_URL = 'https://github.com/pdso/DeveloperDiskImage/raw/master/{ios_version}/{ios_version}.zip'

logger = logging.getLogger(__name__)


def download_developer_disk_image(ios_version: str, directory: Path):
    url = DEVELOPER_DISK_IMAGE_URL.format(ios_version=ios_version)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size_in_bytes = int(r.headers.get('content-length', 0))
        with tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, dynamic_ncols=True) as progress_bar:
            with tempfile.NamedTemporaryFile('wb+') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    progress_bar.update(len(chunk))
                    f.write(chunk)
                zip_file = zipfile.ZipFile(f)
                zip_file.extractall(directory)


class Device:
    def __init__(self):
        self.lockdown = LockdownClient()
        self.diagnostics = DiagnosticsService(self.lockdown)
        self.mounter = None
        self.location = None

    def mount_image(self):
        try:
            self.mounter = MobileImageMounterService(self.lockdown)
        except PasscodeRequiredError as e:
            logger.error(e)
        image_type = 'Developer'

        if not self.mounter.is_image_mounted(image_type):
            logger.debug("Image is not mounted yet")
            logger.debug('trying to figure out the best suited DeveloperDiskImage')
            version = self.lockdown.sanitized_ios_version
            image_dir = f'{get_home_folder()}/DevDiskImage/'
            image_path = f'{image_dir}/DeveloperDiskImage.dmg'
            signature = f'{image_path}.signature'
            developer_disk_image_dir = Path(image_path).parent

            if not developer_disk_image_dir.exists():
                try:
                    download_developer_disk_image(version, developer_disk_image_dir)
                except PermissionError:
                    logger.error(
                        f'DeveloperDiskImage could not be saved to path ({developer_disk_image_dir}). '
                        f'Please make sure your user has the necessary permissions')
                    return

            image_path = Path(image_path)
            signature = Path(signature)
            image_path = image_path.read_bytes()
            signature = signature.read_bytes()

            self.mounter.upload_image(image_type, image_path, signature)
            self.mounter.mount(image_type, signature)
            logger.info('DeveloperDiskImage mounted successfully')
        else:
            logger.debug("Image is mounted.")

    def spoof_gps(self, destination: Location):
        if self.location is None:
            self.location = DtSimulateLocation(self.lockdown)
        self.location.set(destination.latitude, destination.longitude)
        return True

    def stop_spoofing(self):
        self.location.clear()
        self.diagnostics.restart()

        

    

