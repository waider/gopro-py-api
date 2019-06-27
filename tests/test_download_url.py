from .conftest import GoProCameraTestNoHttp
from goprocam import GoProCamera
import os


class DownloadUrlTest(GoProCameraTestNoHttp):
    def test_download_url_short_read(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda f: 'f')
            self.goprocam.download_url('http://10.5.5.9/shorty', 'X.mp4')
            assert os.stat('X.mp4').st_size >= 100
