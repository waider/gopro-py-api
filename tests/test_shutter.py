from .conftest import GoProCameraTest, GoProCameraAuthTest
from goprocam import constants, GoProCamera


class ShutterTest(GoProCameraTest):
    def test_shutter_gpcontrol(self):
        # doesn't return anything, so we need to hack it
        with self.monkeypatch.context() as m:
            def verify_cmd(self, text):
                assert text == 'shutter?p={}'.format(constants.start)
            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.shutter(constants.start)


class ShutterAuthTest(GoProCameraAuthTest):
    def test_shutter_auth(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, param, value):
                assert param == 'SH'
                assert value == '01'
            m.setattr(GoProCamera.GoPro, 'sendBacpac', verify_cmd)
            self.goprocam.shutter(constants.start)

    def test_shutter_auth_longer_cmd(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, param, value):
                assert param == 'SH'
                assert value == 'FF'
            m.setattr(GoProCamera.GoPro, 'sendBacpac', verify_cmd)
            self.goprocam.shutter('FF')
