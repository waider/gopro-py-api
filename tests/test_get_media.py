from .conftest import GoProCameraTest
from goprocam import GoProCamera
from socket import timeout


class GetMediaTest(GoProCameraTest):
    def test_get_media_FS(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            m.setattr(GoProCamera.GoPro, 'getMediaFusion', lambda s: 'MF')
            assert self.goprocam.getMedia() == 'MF'

    def test_get_media_empty(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'HD')
            # tut tut. this should raise an exception or return None
            assert self.goprocam.getMedia() ==\
                'http://10.5.5.9:8080/videos/DCIM//'

    def test_get_media_empty_folder(self):
        with self.monkeypatch.context() as m:
            self.responses[':8080/gp/gpMediaList'] = {
                'media': [
                    {
                        'd': 'folder',
                        'fs': [
                        ]
                    }
                ]
            }
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'HD')
            assert self.goprocam.getMedia() ==\
                'http://10.5.5.9:8080/videos/DCIM/folder/'

    def test_get_media(self):
        with self.monkeypatch.context() as m:
            self.responses[':8080/gp/gpMediaList'] = {
                'media': [
                    {
                        'd': 'folder',
                        'fs': [
                            {'n': 'file'}
                        ]
                    }
                ]
            }
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'HD')
            assert self.goprocam.getMedia() ==\
                'http://10.5.5.9:8080/videos/DCIM/folder/file'

    def test_get_media_timeout(self):
        with self.monkeypatch.context() as m:
            self.responses[':8080/gp/gpMediaList'] = timeout()
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'HD')
            assert self.goprocam.getMedia() == ''

    def test_get_media_httperror(self):
        with self.monkeypatch.context() as m:
            del(self.responses[':8080/gp/gpMediaList'])
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'HD')
            assert self.goprocam.getMedia() == ''
