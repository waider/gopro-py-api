from .conftest import GoProCameraTest
from goprocam import constants, GoProCamera

class ShutterTest(GoProCameraTest):
    def test_shutter_gpcontrol(self):
        # doesn't return anything, so we need to hack it
        with self.monkeypatch.context() as m:
        
            def verify_cmd(self, text):
                assert text == 'shutter?p={}'.format(constants.start)
            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.shutter(constants.start)

    def test_shutter_auth(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'whichCam', lambda self: 'auth')

            def verify_cmd(self, param, value):
                assert param == 'SH'
                assert value == '01'
            m.setattr(GoProCamera.GoPro, 'sendBacpac', verify_cmd)
            self.goprocam.shutter(constants.start)
