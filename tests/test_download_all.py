from .conftest import GoProCameraTest
from goprocam import GoProCamera
from socket import timeout


class DownloadAllTest(GoProCameraTest):
    # noting here: if it calls wakeup and a URLError (timeout) occurs,
    # it tries to print error.code which URLError does not possess.
    def test_download_all_empty(self):
        assert self.goprocam.downloadAll() == []

    def test_download_all_error(self):
        with self.monkeypatch.context() as m:
            def print_verify(arg):
                assert arg == 'Error code:404\n' +\
                    'Make sure the connection to the WiFi camera ' +\
                    'is still active.'
            del(self.responses[':8080/gp/gpMediaList'])
            m.setattr('builtins.print', print_verify)
            assert self.goprocam.downloadAll() is None

    def test_download_all_timeout(self):
        with self.monkeypatch.context() as m:
            def print_verify(arg):
                assert arg == 'HTTP Timeout\n' +\
                    'Make sure the connection to the WiFi camera ' +\
                    'is still active.'
            self.responses[':8080/gp/gpMediaList'] = timeout()
            m.setattr('builtins.print', print_verify)
            assert self.goprocam.downloadAll() is None

    def test_download_all_videos_empty(self):
        assert self.goprocam.downloadAll(option='videos') == []

    def test_download_all_videos_error(self):
        with self.monkeypatch.context() as m:
            def print_verify(arg):
                assert arg == 'Error code:404\n' +\
                    'Make sure the connection to the WiFi camera ' +\
                    'is still active.'
            del(self.responses[':8080/gp/gpMediaList'])
            m.setattr('builtins.print', print_verify)
            assert self.goprocam.downloadAll(option='videos') is None

    def test_download_all_videos_timeout(self):
        with self.monkeypatch.context() as m:
            def print_verify(arg):
                assert arg == 'HTTP Timeout\n' +\
                    'Make sure the connection to the WiFi camera ' +\
                    'is still active.'
            self.responses[':8080/gp/gpMediaList'] = timeout()
            m.setattr('builtins.print', print_verify)
            assert self.goprocam.downloadAll(option='videos') is None

    def test_download_all_photos_empty(self):
        assert self.goprocam.downloadAll(option='photos') == []

    def test_download_all_photos_error(self):
        with self.monkeypatch.context() as m:
            def print_verify(arg):
                assert arg == 'Error code:404\n' +\
                    'Make sure the connection to the WiFi camera ' +\
                    'is still active.'
            del(self.responses[':8080/gp/gpMediaList'])
            m.setattr('builtins.print', print_verify)
            assert self.goprocam.downloadAll(option='photos') is None

    def test_download_all_photos_timeout(self):
        with self.monkeypatch.context() as m:
            def print_verify(arg):
                assert arg == 'HTTP Timeout\n' +\
                    'Make sure the connection to the WiFi camera ' +\
                    'is still active.'
            self.responses[':8080/gp/gpMediaList'] = timeout()
            m.setattr('builtins.print', print_verify)
            assert self.goprocam.downloadAll(option='photos') is None

    def test_download_all_has_file(self):
        with self.monkeypatch.context() as m:
            def verify_download(self, folder, file, custom_filename=""):
                assert folder == 'folder'
                assert file == 'file'

            self.responses[':8080/gp/gpMediaList'] = {
                'media': [{
                    'd': 'folder',
                    'fs': [{'n': 'file'}]
                }]}
            m.setattr(GoProCamera.GoPro, 'downloadMedia', verify_download)
            assert self.goprocam.downloadAll() == ['file']

    def test_download_all_videos_has_file(self):
        with self.monkeypatch.context() as m:
            def verify_download(self, folder, file, custom_filename=""):
                assert folder == 'folder'
                assert file == 'file'

            self.responses[':8080/gp/gpMediaList'] = {
                'media': [{
                    'd': 'folder',
                    'fs': [{'n': 'file'}]
                }]}
            m.setattr(GoProCamera.GoPro, 'downloadMedia', verify_download)
            # will return empty because no videos (*.MP4)
            assert self.goprocam.downloadAll(option="videos") == []

    def test_download_all_photos_has_file(self):
        with self.monkeypatch.context() as m:
            def verify_download(self, folder, file, custom_filename=""):
                assert folder == 'folder'
                assert file == 'file'

            self.responses[':8080/gp/gpMediaList'] = {
                'media': [{
                    'd': 'folder',
                    'fs': [{'n': 'file'}]
                }]}
            m.setattr(GoProCamera.GoPro, 'downloadMedia', verify_download)
            # will return empty because no photos (*.JPG)
            assert self.goprocam.downloadAll(option="photos") == []

    def test_download_all_videos_has_mp4_file(self):
        with self.monkeypatch.context() as m:
            def verify_download(self, folder, file, custom_filename=""):
                assert folder == 'folder'
                assert file == 'file.MP4'

            self.responses[':8080/gp/gpMediaList'] = {
                'media': [{
                    'd': 'folder',
                    'fs': [{'n': 'file.MP4'}]
                }]}
            m.setattr(GoProCamera.GoPro, 'downloadMedia', verify_download)
            assert self.goprocam.downloadAll(option="videos") == ['file.MP4']

    def test_download_all_photos_has_jpg_file(self):
        with self.monkeypatch.context() as m:
            def verify_download(self, folder, file, custom_filename=""):
                assert folder == 'folder'
                assert file == 'file.JPG'

            self.responses[':8080/gp/gpMediaList'] = {
                'media': [{
                    'd': 'folder',
                    'fs': [{'n': 'file.JPG'}]
                }]}
            m.setattr(GoProCamera.GoPro, 'downloadMedia', verify_download)
            assert self.goprocam.downloadAll(option="photos") == ['file.JPG']
