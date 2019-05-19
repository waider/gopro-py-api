from .conftest import GoProCameraTest, GoProCameraAuthTest
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
        self.goprocam.power_on(self.goprocam._mac_address)
