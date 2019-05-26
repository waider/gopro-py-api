from .conftest import GoProCameraTest
from goprocam import GoProCamera
import urllib


class DownloadLowResTest(GoProCameraTest):
    def test_download_low_res_busy(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args == 'Not supported while recording ' +\
                    'or processing media.'
            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 1)
            m.setattr('builtins.print', print_verify)
            self.goprocam.downloadLowRes()

    def test_download_low_res_empty(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args in [
                    'not supported',
                    'filename: ',  # definitely buggy
                    '',
                    'ERROR: HTTP Error 404: Not Found ()'
                ]
            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(GoProCamera.GoPro, 'getMedia', lambda s: '')
            self.goprocam.downloadLowRes()

    def test_download_low_res_mp4(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args in [
                    'filename: LOWRESfolder-file.MP4',
                    'http://10.5.5.9/folder/file.LRV'
                ]

            def urlretrieve_verify(url, path):
                assert url == 'http://10.5.5.9/folder/file.LRV'
                assert path == 'LOWRESfolder-file.MP4'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(GoProCamera.GoPro, 'getMedia',
                      lambda s: 'http://10.5.5.9/folder/file.MP4')
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, o: o + '.MP4' if o == 'file' else o)
            m.setattr(urllib.request, 'urlretrieve', urlretrieve_verify)
            self.goprocam.downloadLowRes()

    def test_download_low_res_mp4_error(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args in [
                    'filename: LOWRESfolder-file.MP4',
                    'http://10.5.5.9/folder/file.LRV',
                    'ERROR: HTTP Error 404: Not Found'
                ]

            def urlretrieve_verify(url, path):
                raise urllib.error.HTTPError(url, 404, 'Not Found', None, None)

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(GoProCamera.GoPro, 'getMedia',
                      lambda s: 'http://10.5.5.9/folder/file.MP4')
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, o: o + '.MP4' if o == 'file' else o)
            m.setattr(urllib.request, 'urlretrieve', urlretrieve_verify)
            self.goprocam.downloadLowRes()

    def test_download_low_res_mp4_gh(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args in [
                    'filename: LOWRESfolder-file.MP4',
                    'http://10.5.5.9/folder/file-GL.LRV'
                ]

            def urlretrieve_verify(url, path):
                assert url == 'http://10.5.5.9/folder/file-GL.LRV'
                assert path == 'LOWRESfolder-file.MP4'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(GoProCamera.GoPro, 'getMedia',
                      lambda s: 'http://10.5.5.9/folder/file-GH.MP4')
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, o: o + '.MP4' if o == 'file' else o)
            m.setattr(urllib.request, 'urlretrieve', urlretrieve_verify)
            self.goprocam.downloadLowRes()

    def test_download_low_res_mp4_custom_filename(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args in [
                    'filename: LOWRESfolder-file.MP4',
                    'http://10.5.5.9/folder/file.LRV'
                ]

            def urlretrieve_verify(url, path):
                assert url == 'http://10.5.5.9/folder/file.LRV'
                assert path == 'lowres.mp4'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(GoProCamera.GoPro, 'getMedia',
                      lambda s: 'http://10.5.5.9/folder/file.MP4')
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, o: o + '.MP4' if o == 'file' else o)
            m.setattr(urllib.request, 'urlretrieve', urlretrieve_verify)
            self.goprocam.downloadLowRes(custom_filename="lowres.mp4")

    def test_download_low_res_mp4_custom_filename_error(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args in [
                    'filename: LOWRESfolder-file.MP4',
                    'http://10.5.5.9/folder/file.LRV',
                    'ERROR: HTTP Error 404: Not Found'
                ]

            def urlretrieve_verify(url, path):
                raise urllib.error.HTTPError(url, 404, 'Not Found', None, None)

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(GoProCamera.GoPro, 'getMedia',
                      lambda s: 'http://10.5.5.9/folder/file.MP4')
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, o: o + '.MP4' if o == 'file' else o)
            m.setattr(urllib.request, 'urlretrieve', urlretrieve_verify)
            self.goprocam.downloadLowRes(custom_filename="lowres.mp4")

    def test_download_low_res_mp4_fs(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args in [
                    'filename: LOWRESfolder-file.MP4',
                    'http://10.5.5.9/folder/file.LRV'
                ]

            def urlretrieve_verify(url, path):
                assert url == 'http://10.5.5.9/folder/file.LRV'
                assert path == 'LOWRESfolder-file.MP4'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(GoProCamera.GoPro, 'getMedia',
                      lambda s: ['http://10.5.5.9/folder/file.MP4'])
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, o: [o + '.MP4' if o == 'file' else o])
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            m.setattr(urllib.request, 'urlretrieve', urlretrieve_verify)
            self.goprocam.downloadLowRes()

    def test_download_low_res_non_mp4_path(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args in [
                    'not supported',
                    # broken...
                    'filename: ',
                    '',
                    'ERROR: HTTP Error 404: Not Found ()',
                ]

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            # Behaves poorly if this is a full URL
            self.goprocam.downloadLowRes(path='/folder/file.JPG')

    def test_download_low_res_mp4_path(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args in [
                    'filename: LOWRES-folder-file.LRV',
                    '/folder/file.LRV'
                ]

            def urlretrieve_verify(url, path):
                assert url == '/folder/file.LRV'
                assert path == 'LOWRES-folder-file.LRV'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(urllib.request, 'urlretrieve', urlretrieve_verify)
            self.goprocam.downloadLowRes(path='/folder/file.MP4')

    def test_download_low_res_mp4_path_gh(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args in [
                    'filename: LOWRES-folder-file-GH.LRV',
                    '/folder/file-GL.LRV'
                ]

            def urlretrieve_verify(url, path):
                # broken also
                assert url == '/folder/file-GL.LRV'
                assert path == 'LOWRES-folder-file-GH.LRV'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(urllib.request, 'urlretrieve', urlretrieve_verify)
            self.goprocam.downloadLowRes(path='/folder/file-GH.MP4')

    def test_download_low_res_mp4_path_custom_filename(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args in [
                    'filename: LOWRES-folder-file.LRV',
                    '/folder/file.LRV'
                ]

            def urlretrieve_verify(url, path):
                assert url == '/folder/file.LRV'
                assert path == 'foo.mp4'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(urllib.request, 'urlretrieve', urlretrieve_verify)
            self.goprocam.downloadLowRes(path='/folder/file.MP4',
                                         custom_filename='foo.mp4')

    def test_download_low_res_mp4_path_error(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args in [
                    'filename: LOWRES-folder-file.LRV',
                    '/folder/file.LRV',
                    'ERROR: HTTP Error 404: Not Found'
                ]

            def urlretrieve_verify(url, path):
                raise urllib.error.HTTPError(url, 404, 'Not Found', None, None)

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(urllib.request, 'urlretrieve', urlretrieve_verify)
            self.goprocam.downloadLowRes(path='/folder/file.MP4')

    def test_download_low_res_mp4_path_custom_filename_error(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args in [
                    'filename: LOWRES-folder-file.LRV',
                    '/folder/file.LRV',
                    'ERROR: HTTP Error 404: Not Found'
                ]

            def urlretrieve_verify(url, path):
                raise urllib.error.HTTPError(url, 404, 'Not Found', None, None)

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr('builtins.print', print_verify)
            m.setattr(urllib.request, 'urlretrieve', urlretrieve_verify)
            self.goprocam.downloadLowRes(path='/folder/file.MP4',
                                         custom_filename='foo.mp4')
