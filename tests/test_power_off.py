from .conftest import GoProCameraTest, GoProCameraAuthTest
from goprocam import GoProCamera


class PowerOffTest(GoProCameraTest):
    def test_power_off(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, text):
                assert text == 'system/sleep'
            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.power_off()


class PowerOffAuthTest(GoProCameraAuthTest):
    def test_power_off(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, cmd, param):
                assert cmd == 'PW'
                assert param == '00'
            m.setattr(GoProCamera.GoPro, 'sendBacpac', verify_cmd)
            self.goprocam.power_off()
