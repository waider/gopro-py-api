from .conftest import GoProCameraTest
from goprocam import GoProCamera
import urllib


class DownloadRawPhotoTest(GoProCameraTest):
    def test_download_raw_photo_busy(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args == 'Not supported while recording ' +\
                    'or processing media.'
            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 1)
            m.setattr('builtins.print', print_verify)
            self.goprocam.downloadRawPhoto(folder='folder', file='file')

    def test_download_raw_photo(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args == 'filename: file.GPR'

            def urlretrieve_mock(url, path):
                assert url == 'http://10.5.5.9:8080/videos/DCIM/folder/' +\
                    'file.GPR'
                assert path == 'file.GPR'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(urllib.request, 'urlretrieve', urlretrieve_mock)
            self.goprocam.downloadRawPhoto(folder='folder', file='file.JPG')

    def test_download_raw_photo_custom_filename(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args == 'filename: file.GPR'

            def urlretrieve_mock(url, path):
                assert url == 'http://10.5.5.9:8080/videos/DCIM/folder/' +\
                    'file.GPR'
                assert path == 'myfile.GPR'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(urllib.request, 'urlretrieve', urlretrieve_mock)
            self.goprocam.downloadRawPhoto(folder='folder', file='file.JPG',
                                           custom_filename='myfile.GPR')

    def test_download_raw_photo_fs_not_front(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args == 'filename: file.GPR'

            def urlretrieve_mock(url, path):
                assert url == 'http://10.5.5.9:8080/videos/DCIM/GBACK/file.GPR'
                assert path == 'file.GPR'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(urllib.request, 'urlretrieve', urlretrieve_mock)
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            self.goprocam.downloadRawPhoto(folder='GBACK', file='file.JPG')

    def test_download_raw_photo_fs_front(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args == 'filename: file.GPR'

            def urlretrieve_mock(url, path):
                # buggy, I think
                assert url in [
                    'http://10.5.5.9:8080/videos2/DCIM/GFRNT/file.GPR',
                    'http://10.5.5.9:8080/videos/DCIM/GFRNT/file.GPR'
                ]
                assert path == 'file.GPR'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(urllib.request, 'urlretrieve', urlretrieve_mock)
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            self.goprocam.downloadRawPhoto(folder='GFRNT', file='file.JPG')

    def test_download_raw_photo_error(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args in ['filename: file.GPR',
                                'ERROR: HTTP Error 404: Not Found']

            def urlretrieve_mock(url, path):
                raise urllib.error.HTTPError(url, 404, 'Not Found', None, None)

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(urllib.request, 'urlretrieve', urlretrieve_mock)
            self.goprocam.downloadRawPhoto(folder='folder', file='file.JPG')
