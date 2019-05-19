from .conftest import GoProCameraTest, GoProCameraAuthTest
from goprocam import GoProCamera


class LocateTest(GoProCameraTest):
    def test_locate(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, text):
                assert text == 'system/locate?p=foo'
            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.locate('foo')


class LocateAuthTest(GoProCameraAuthTest):
    def test_locate(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, cmd, param):
                assert cmd == 'LL'
                assert param == '0foo'
            m.setattr(GoProCamera.GoPro, 'sendCamera', verify_cmd)
            self.goprocam.locate('foo')
