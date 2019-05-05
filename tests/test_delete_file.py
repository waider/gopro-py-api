from .conftest import GoProCameraTest, GoProCameraAuthTest
from goprocam import GoProCamera


class DeleteFileTest(GoProCameraTest):
    def test_delete_file(self):
        with self.monkeypatch.context() as m:

            def verify_cmd(self, text):
                assert text == 'storage/delete?p=folder/file'
            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.deleteFile('folder', 'file')

    def test_delete_file_url(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getInfoFromURL',
                      lambda self, url: ('folder', 'file'))

            def verify_cmd(self, text):
                assert text == 'storage/delete?p=folder/file'
            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.deleteFile('http://' + self.goprocam.ip_addr,
                                     'dummy')


class DeleteFileAuthTest(GoProCameraAuthTest):
    def test_delete_file(self):
        with self.monkeypatch.context() as m:

            def verify_cmd(self, param, value):
                assert param == 'DF'
                assert value == '/folder/file'
            m.setattr(GoProCamera.GoPro, 'sendCamera', verify_cmd)
            self.goprocam.deleteFile('folder', 'file')
