from .conftest import GoProCameraTest
from goprocam import GoProCamera
import json


class DownloadMultiShotTest(GoProCameraTest):
    def test_download_multi_shot_empty(self):
        with self.monkeypatch.context() as m:
            def downloadmedia_verify(self, folder, f):
                # even with an empty device it tries to download one file
                assert folder == ''
                assert f == '0.JPG'

            m.setattr(GoProCamera.GoPro, 'downloadMedia', downloadmedia_verify)
            m.setattr(GoProCamera.GoPro, 'listMedia', lambda s: '{"media":[]}')
            self.goprocam.downloadMultiShot()

    def test_download_multi_shot(self):
        with self.monkeypatch.context() as m:
            def downloadmedia_verify(self, folder, f):
                assert folder == ''
                assert f in ['0.JPG', '1.JPG', '2.JPG']

            m.setattr(GoProCamera.GoPro, 'downloadMedia', downloadmedia_verify)
            m.setattr(GoProCamera.GoPro, 'listMedia', lambda s: json.dumps(
                {
                    "media": [
                        {
                            'd': '',
                            'fs': [
                                {
                                    'n': '',
                                    'b': 0,
                                    'l': 2,
                                },
                                {
                                    'n': 'file2',
                                    'b': 1,
                                    'l': 7
                                }
                            ]
                        },
                        {
                            'd': 'f2',
                            'fs': [
                                {
                                    'n': '',
                                    'b': 0,
                                    'l': 2,
                                }
                            ]
                        }
                    ]
                }
            ))
            self.goprocam.downloadMultiShot()

    def test_download_multi_shot_path_empty(self):
        with self.monkeypatch.context() as m:
            def downloadmedia_verify(self, folder, f):
                assert folder == ''
                assert f == '0.JPG'

            m.setattr(GoProCamera.GoPro, 'downloadMedia', downloadmedia_verify)
            m.setattr(GoProCamera.GoPro, 'listMedia', lambda s: '{"media":[]}')
            # this basically does the same as the 'empty' test
            self.goprocam.downloadMultiShot(path='/')

    def test_download_multi_shot_path(self):
        with self.monkeypatch.context() as m:
            def downloadmedia_verify(self, folder, f):
                assert folder == ''
                assert f in ['0.JPG', '1.JPG', '2.JPG']

            m.setattr(GoProCamera.GoPro, 'downloadMedia', downloadmedia_verify)
            m.setattr(GoProCamera.GoPro, 'listMedia', lambda s: json.dumps(
                {
                    "media": [
                        {
                            'd': '',
                            'fs': [
                                {
                                    'n': '',
                                    'b': 0,
                                    'l': 2,
                                },
                                {
                                    'n': 'file2',
                                    'b': 1,
                                    'l': 7
                                }
                            ],
                        },
                        {
                            'd': 'folder2',
                            'fs': []
                        }
                    ]
                }
            ))
            self.goprocam.downloadMultiShot(path='/')
