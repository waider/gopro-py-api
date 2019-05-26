from .conftest import GoProCameraTest, GoProCameraAuthTest
from goprocam import GoProCamera


class ChangeWifiSettingsTest(GoProCameraTest):
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


class ChangeWifiSettingsAuthTest(GoProCameraAuthTest):
    def test_change_wifi_settings(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, text):
                assert False

            def mock_builtin(*args, **kwargs):
                assert False

            # this is a no-op for 'auth' cameras
            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            m.setattr('builtins.print', mock_builtin)
            m.setattr('builtins.exit', mock_builtin)

            self.goprocam.changeWiFiSettings('ssid', 'password')
