from .conftest import GoProCameraTest
from goprocam import GoProCamera


class ChangeWifiSettings(GoProCameraTest):
    def test_change_wifi_settings(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, text):
                assert text == 'wireless/ap/ssid?ssid=ssid&pw=password'

            # need to trap print() and exit()
            def mock_builtin(*args, **kwargs):
                pass

            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            m.setattr('builtins.print', mock_builtin)
            m.setattr('builtins.exit', mock_builtin)
            self.goprocam.changeWiFiSettings('ssid', 'password')
