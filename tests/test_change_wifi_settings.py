from .conftest import GoProCameraTest
from goprocam import GoProCamera
import pytest


class ChangeWifiSettings(GoProCameraTest):
    def test_change_wifi_settings(self):
        with self.monkeypatch.context() as m:

            # this function calls exit() which means we need to be tricky.
            class SuccessException(Exception):
                pass

            def verify_cmd(self, text):
                assert text == 'wireless/ap/ssid?ssid=ssid&pw=password'
                raise SuccessException()

            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            with pytest.raises(SuccessException):
                self.goprocam.changeWiFiSettings('ssid', 'password')
