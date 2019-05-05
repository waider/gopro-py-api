from .conftest import GoProCameraTest
from goprocam import GoProCamera


class ModeTest(GoProCameraTest):
    def test_mode_gpcontrol_mode_only(self):
        with self.monkeypatch.context() as m:

            def verify_cmd(self, text):
                assert text == 'sub_mode?mode=foo&sub_mode=0'

            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.mode('foo')

    def test_mode_gpcontrol_mode_and_submode(self):
        with self.monkeypatch.context() as m:

            def verify_cmd(self, text):
                assert text == 'sub_mode?mode=foo&sub_mode=bar'

            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.mode('foo', 'bar')

    def test_mode_auth(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'whichCam', lambda self: 'auth')

            def verify_cmd(self, param, value):
                assert param == 'CM'
                assert value == '01'
            m.setattr(GoProCamera.GoPro, 'sendBacpac', verify_cmd)
            self.goprocam.mode('1')

    def test_mode_auth_longer_cmd(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'whichCam', lambda self: 'auth')

            def verify_cmd(self, param, value):
                assert param == 'CM'
                assert value == 'FF'
            m.setattr(GoProCamera.GoPro, 'sendBacpac', verify_cmd)
            self.goprocam.mode('FF')
