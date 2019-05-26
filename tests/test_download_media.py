from .conftest import GoProCameraTest
from goprocam import GoProCamera
import urllib


class DownloadMediaTest(GoProCameraTest):
    def test_download_media_busy(self):
        with self.monkeypatch.context() as m:
            def print_verify(arg):
                assert arg ==\
                    'Not supported while recording or processing media.'
            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 1)
            m.setattr('builtins.print', print_verify)
            self.goprocam.downloadMedia(folder='folder', file='file')

    def test_download_media(self):
        with self.monkeypatch.context() as m:
            def mock_urlretrieve(url, path, reporthook=None):
                assert url == 'http://10.5.5.9:8080/videos/DCIM/folder/file'
                assert path == 'file'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr(urllib.request, 'urlretrieve', mock_urlretrieve)
            self.goprocam.downloadMedia(folder='folder', file='file')

    def test_download_media_custom_filename(self):
        with self.monkeypatch.context() as m:
            def mock_urlretrieve(url, path, reporthook=None):
                assert url == 'http://10.5.5.9:8080/videos/DCIM/folder/file'
                assert path == 'custom'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr(urllib.request, 'urlretrieve', mock_urlretrieve)
            self.goprocam.downloadMedia(folder='folder', file='file',
                                        custom_filename='custom')

    # I think this is buggy?... tries to download twice
    def test_download_media_fs_front(self):
        with self.monkeypatch.context() as m:
            def mock_urlretrieve(url, path, reporthook=None):
                assert url in ['http://10.5.5.9:8080/videos2/DCIM/GFRNT/file',
                               'http://10.5.5.9:8080/videos/DCIM/GFRNT/file']
                assert path == 'file'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            m.setattr(urllib.request, 'urlretrieve', mock_urlretrieve)
            self.goprocam.downloadMedia(folder='GFRNT', file='file')

    def test_download_media_fs_back(self):
        with self.monkeypatch.context() as m:
            def mock_urlretrieve(url, path, reporthook=None):
                assert url == 'http://10.5.5.9:8080/videos/DCIM/GBACK/file'
                assert path == 'file'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            m.setattr(urllib.request, 'urlretrieve', mock_urlretrieve)
            self.goprocam.downloadMedia(folder='GBACK', file='file')

    def test_download_media_error(self):
        with self.monkeypatch.context() as m:
            # A bit clunky
            def print_verify(arg):
                assert arg in [
                    'filename: file',
                    'ERROR: HTTP Error 404: Not Found (http://10.5.5.9:8080/' +
                    'videos/DCIM/folder/file)']
            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            self.goprocam.downloadMedia(folder='folder', file='file')
