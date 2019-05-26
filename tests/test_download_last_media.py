from .conftest import GoProCameraTest
from goprocam import GoProCamera
import urllib


class DownloadLastMediaTest(GoProCameraTest):
    def test_download_last_media_recording(self):
        with self.monkeypatch.context() as m:
            def print_verify(arg):
                assert arg ==\
                    'Not supported while recording or processing media.'
            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 1)
            m.setattr('builtins.print', print_verify)
            self.goprocam.downloadLastMedia()

    def test_download_last_media(self):
        with self.monkeypatch.context() as m:
            def mock_media_info(self, option):
                if option == 'folder':
                    return 'folder'
                elif option == 'file':
                    return 'file'
                elif option == 'size':
                    return '1.0B'
                else:
                    raise ValueError(option)

            def mock_media(self):
                return 'http://10.5.5.9/foo/bar'

            def mock_urlretrieve(url, path):
                assert url == mock_media(None)
                assert path == 'folder-file'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr(GoProCamera.GoPro, 'getMediaInfo', mock_media_info)
            m.setattr(GoProCamera.GoPro, 'getMedia', mock_media)
            m.setattr(urllib.request, 'urlretrieve', mock_urlretrieve)

            self.responses['/foo/bar'] = 'data'

            self.goprocam.downloadLastMedia()

    def test_download_last_media_custom_filename(self):
        with self.monkeypatch.context() as m:
            def mock_media_info(self, option):
                if option == 'folder':
                    return 'folder'
                elif option == 'file':
                    return 'file'
                elif option == 'size':
                    return '1.0B'
                else:
                    raise ValueError(option)

            def mock_media(self):
                return 'http://10.5.5.9/foo/bar'

            def mock_urlretrieve(url, path):
                assert url == mock_media(None)
                assert path == '/foo/bar'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr(GoProCamera.GoPro, 'getMediaInfo', mock_media_info)
            m.setattr(GoProCamera.GoPro, 'getMedia', mock_media)
            m.setattr(urllib.request, 'urlretrieve', mock_urlretrieve)

            self.responses['/foo/bar'] = 'data'

            self.goprocam.downloadLastMedia(custom_filename='/foo/bar')

    def test_download_last_media_path(self):
        with self.monkeypatch.context() as m:
            def mock_media_info(self, option):
                if option == 'folder':
                    return 'folder'
                elif option == 'file':
                    return 'file'
                elif option == 'size':
                    return '1.0B'
                else:
                    raise ValueError(option)

            def mock_media(self):
                return '/other/path'

            def mock_urlretrieve(url, path):
                assert url == mock_media(None)
                assert path == '-other-path'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr(GoProCamera.GoPro, 'getMediaInfo', mock_media_info)
            m.setattr(GoProCamera.GoPro, 'getMedia', mock_media)
            m.setattr(urllib.request, 'urlretrieve', mock_urlretrieve)

            self.responses['/foo/bar'] = 'data'

            self.goprocam.downloadLastMedia(path='/other/path')

    def test_download_last_media_path_custom_filename(self):
        with self.monkeypatch.context() as m:
            def mock_media_info(self, option):
                if option == 'folder':
                    return 'folder'
                elif option == 'file':
                    return 'file'
                elif option == 'size':
                    return '1.0B'
                else:
                    raise ValueError(option)

            def mock_media(self):
                return '/other/path'

            def mock_urlretrieve(url, path):
                assert url == mock_media(None)
                assert path == '/foo/bar'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr(GoProCamera.GoPro, 'getMediaInfo', mock_media_info)
            m.setattr(GoProCamera.GoPro, 'getMedia', mock_media)
            m.setattr(urllib.request, 'urlretrieve', mock_urlretrieve)

            self.responses['/foo/bar'] = 'data'

            self.goprocam.downloadLastMedia(path='/other/path',
                                            custom_filename='/foo/bar')

    def test_download_last_media_fs(self):
        with self.monkeypatch.context() as m:
            def mock_media_info(self, option):
                if option == 'folder':
                    return ['folder1', 'folder2']
                elif option == 'file':
                    return ['file1', 'file2']
                elif option == 'size':
                    return ['1.0B', '2.0B']
                else:
                    raise ValueError(option)

            def mock_media(self):
                return ['/folder1/path', '/folder2/path']

            def mock_urlretrieve(url, path):
                assert url in mock_media(None)
                assert path in ['folder1file1', 'folder2file2']

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr(GoProCamera.GoPro, 'getMediaInfo', mock_media_info)
            m.setattr(GoProCamera.GoPro, 'getMedia', mock_media)
            m.setattr(urllib.request, 'urlretrieve', mock_urlretrieve)
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')

            self.responses['/foo/bar'] = 'data'

            self.goprocam.downloadLastMedia()
