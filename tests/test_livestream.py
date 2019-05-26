from .conftest import GoProCameraTest, GoProCameraAuthTest
from goprocam import GoProCamera


class LivestreamTest(GoProCameraTest):
    def test_livestream_start(self):
        with self.monkeypatch.context() as m:
            def verify_exe(self, cmd):
                assert cmd == 'p1=gpStream&a1=proto_v2&c1=restart'
            m.setattr(GoProCamera.GoPro, 'gpControlExecute', verify_exe)
            self.goprocam.livestream(option='start')

    def test_livestream_stop(self):
        with self.monkeypatch.context() as m:
            def verify_exe(self, cmd):
                assert cmd == 'p1=gpStream&a1=proto_v2&c1=stop'
            m.setattr(GoProCamera.GoPro, 'gpControlExecute', verify_exe)
            self.goprocam.livestream(option='stop')


class LivestreamAuthTest(GoProCameraAuthTest):
    def test_livestream_start(self):
        with self.monkeypatch.context() as m:
            def verify_exe(self, cmd, param):
                assert cmd == 'PV'
                assert param == '02'
            m.setattr(GoProCamera.GoPro, 'sendCamera', verify_exe)
            self.goprocam.livestream(option='start')

    def test_livestream_stop(self):
        with self.monkeypatch.context() as m:
            def verify_exe(self, cmd, param):
                assert cmd == 'PV'
                assert param == '00'
            m.setattr(GoProCamera.GoPro, 'sendCamera', verify_exe)
            self.goprocam.livestream(option='stop')
