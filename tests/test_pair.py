from .conftest import GoProCameraTest
from goprocam import GoProCamera
import socket


class PairTest(GoProCameraTest):
    def test_pair(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, cmd):
                # this picks up the value from input, below
                assert cmd == 'wireless/ap/ssid?ssid=pair&pw=pair'

            m.setattr('builtins.input', lambda x: 'pair')

            self.responses['https://10.5.5.9/gpPair' +
                           '?c=start&pin=pair&mode=0'] = '[start pairing]'
            self.responses['https://10.5.5.9/gpPair' +
                           '?c=finish&pin=pair&mode=0'] = '[end pairing]'
            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.pair()

    def test_pair_nopin(self):
        # Danger: loops infinitely and tightly until '{}' shows up
        self.responses['/gp/gpControl/command/wireless/pair/complete?' +
                       'success=1&' +
                       'deviceName=' + socket.gethostname()] = {}
        self.goprocam.pair(usepin=False)
