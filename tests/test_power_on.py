from .conftest import GoProCameraTest, GoProCameraAuthTest
from goprocam import GoProCamera
import pytest


class PowerOnTest(GoProCameraTest):
    def test_power_on(self):
        self.goprocam.power_on(self.goprocam._mac_address)

    @pytest.mark.xfail(reason='broken default', strict=True)
    def test_power_on_mac_none(self):
        self.goprocam.power_on(None)

    def test_power_on_short_mac(self):
        self.goprocam.power_on(self.goprocam._mac_address.replace(':', ''))


class PowerOnAuthTest(GoProCameraAuthTest):
    def test_power_on_auth(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, param, value):
                assert param == 'PW'
                assert value == '01'
            m.setattr(GoProCamera.GoPro, 'sendBacpac', verify_cmd)
            self.goprocam.power_on_auth()
