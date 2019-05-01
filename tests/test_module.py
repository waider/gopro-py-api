from .conftest import GoProCameraTest
from goprocam import GoProCamera
import time

class ModuleTest(GoProCameraTest):
    def test_init(self):
        assert self.goprocam, "got a self.goprocam object"
        assert self.goprocam.ip_addr == '10.5.5.9'
        assert self.goprocam._mac_address == 'DE:AD:BE:EF' # xxx
        assert self.goprocam._camera == 'gpcontrol'

    def test_init_auth(self):
        # this will invoke time.sleep and power_on_auth
        self.monkeypatch.setattr(time, 'sleep', lambda x: None)
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'power_on_auth', lambda self: None)
            self.goprocam = GoProCamera.GoPro(camera='auth')
        assert self.goprocam._camera == 'auth'

    def test_init_pair(self):
        def fakepair(self):
            self.paired = True
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'pair', fakepair)
            self.goprocam = GoProCamera.GoPro(camera='startpair')
        assert self.goprocam.paired
        
    def test_init_detect(self):
        self.monkeypatch.setattr(time, 'sleep', lambda x: None)
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'prepare_gpcontrol', lambda self: None)
            self.goprocam = GoProCamera.GoPro(camera='detect')
        assert self.goprocam._camera == 'gpcontrol'

    def test_str(self):
        # this is a little contrived but avoids testing infoCamera by side-effect
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda self: 'stringy')
            assert str(self.goprocam) == 'stringy'
