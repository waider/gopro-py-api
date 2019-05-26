from .conftest import GoProCameraTest, mock_mediainfo_jpg, mock_mediainfo_txt,\
    mock_mediainfo_jpg_fs, mock_mediainfo_txt_fs, verify_uncalled
from goprocam import GoProCamera
import urllib


class DownloadLastRawPhotoTest(GoProCameraTest):
    def test_download_last_raw_photo_recording(self):
        with self.monkeypatch.context() as m:
            def print_verify(arg):
                assert arg ==\
                    'Not supported while recording or processing media.'
            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 1)
            m.setattr('builtins.print', print_verify)
            self.goprocam.downloadLastRawPhoto()

    def test_download_last_raw_photo(self):
        with self.monkeypatch.context() as m:
            def mock_urlretrieve(url, path):
                assert url == 'folder/file.GPR'
                assert path == 'folder-file.GPR'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr(GoProCamera.GoPro, 'getMediaInfo', mock_mediainfo_jpg)
            m.setattr(GoProCamera.GoPro, 'getMedia',
                      lambda s: 'folder/file.JPG')
            m.setattr(urllib.request, 'urlretrieve', mock_urlretrieve)
            self.goprocam.downloadLastRawPhoto()

    def test_download_last_raw_photo_not_jpg(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr(GoProCamera.GoPro, 'getMediaInfo', mock_mediainfo_txt)
            m.setattr(GoProCamera.GoPro, 'getMedia',
                      lambda s: 'folder/file.TXT')
            m.setattr(urllib.request, 'urlretrieve', verify_uncalled)
            self.goprocam.downloadLastRawPhoto()

    def test_download_last_raw_photo_custom_filename(self):
        with self.monkeypatch.context() as m:
            def mock_urlretrieve(url, path):
                assert url == 'folder/file.GPR'
                assert path == 'path'

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr(GoProCamera.GoPro, 'getMediaInfo', mock_mediainfo_jpg)
            m.setattr(GoProCamera.GoPro, 'getMedia',
                      lambda s: 'folder/file.JPG')
            m.setattr(urllib.request, 'urlretrieve', mock_urlretrieve)
            self.goprocam.downloadLastRawPhoto(custom_filename='path')

    def test_download_last_raw_photo_fs(self):
        with self.monkeypatch.context() as m:
            def mock_urlretrieve(url, path):
                assert url in ['GFRNT/front.JPG',
                               'GBACK/back.JPG']  # XXX bug
                assert path in ['GBACKfront.JPG', 'GBACKback.JPG']  # also

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            m.setattr(GoProCamera.GoPro, 'getMediaInfo', mock_mediainfo_jpg_fs)
            m.setattr(GoProCamera.GoPro, 'getMedia',
                      lambda s: ['GFRNT/front.JPG', 'GBACK/back.JPG'])
            m.setattr(urllib.request, 'urlretrieve', mock_urlretrieve)
            self.goprocam.downloadLastRawPhoto()

    def test_download_last_raw_photo_fs_not_jpg(self):
        with self.monkeypatch.context() as m:
            def mock_urlretrieve(url, path):
                assert url in ['GFRNT/front.JPG',
                               'GBACK/back.JPG']  # XXX bug
                assert path in ['GBACKfront.JPG', 'GBACKback.JPG']  # also

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            m.setattr(GoProCamera.GoPro, 'getMediaInfo', mock_mediainfo_txt_fs)
            m.setattr(GoProCamera.GoPro, 'getMedia',
                      lambda s: ['GFRNT/front.TXT', 'GBACK/back.TXT'])
            m.setattr(urllib.request, 'urlretrieve', verify_uncalled)
            self.goprocam.downloadLastRawPhoto()

    def test_download_last_raw_photo_fs_custom_filename(self):
        with self.monkeypatch.context() as m:
            def mock_urlretrieve(url, path):
                assert url in ['GFRNT/front.JPG',
                               'GBACK/back.JPG']  # XXX bug
                assert path in ['GBACKfront.JPG', 'GBACKback.JPG']  # also

            m.setattr(GoProCamera.GoPro, 'IsRecording', lambda s: 0)
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            m.setattr(GoProCamera.GoPro, 'getMediaInfo', mock_mediainfo_jpg_fs)
            m.setattr(GoProCamera.GoPro, 'getMedia',
                      lambda s: ['GFRNT/front.JPG', 'GBACK/back.JPG'])
            m.setattr(urllib.request, 'urlretrieve', mock_urlretrieve)
            self.goprocam.downloadLastRawPhoto(custom_filename='path')
