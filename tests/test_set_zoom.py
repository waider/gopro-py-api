from .conftest import GoProCameraTest
from goprocam import GoProCamera


class SetZoomTest(GoProCameraTest):
    def test_set_zoom_min(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, cmd):
                assert cmd == 'digital_zoom?range_pcnt=0'

            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.setZoom(zoomLevel=0)

    def test_set_zoom_max(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, cmd):
                assert cmd == 'digital_zoom?range_pcnt=100'

            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.setZoom(zoomLevel=100)

    def test_set_zoom_over_max(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, cmd):
                raise ValueError("shouldn't get here")

            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.setZoom(zoomLevel=101)
