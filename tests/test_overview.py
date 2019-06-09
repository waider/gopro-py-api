from .conftest import GoProCameraTest, GoProCameraAuthTest,\
    GoProCameraUnknownTest, verify_uncalled
from goprocam import GoProCamera


class OverviewUnknownTest(GoProCameraUnknownTest):
    def test_overview(self):
        with self.monkeypatch.context() as m:
            m.setattr('builtins.print', verify_uncalled)
            self.goprocam.overview()


class OverviewTest(GoProCameraTest):
    def test_overview(self):
        # need to hook print() for this
        def mock_print(*args, **kwargs):
            for arg in args:
                assert arg in [
                    'camera overview',
                    'current mode: parsed',
                    'current submode: parsed',
                    'current video resolution: parsed',
                    'current video framerate: parsed',
                    'pictures taken: status',
                    'videos taken: ', 'status',  # tsk
                    'videos left: parsed',
                    'pictures left: status',
                    'battery left: parsed',
                    'space left in sd card: parsed',
                    'camera SSID: status',
                    'Is Recording: parsed',
                    'Clients connected: status',
                    'camera model: info',
                    'firmware version: info',
                    'serial number: info',
                    ]
        with self.monkeypatch.context() as m:
            m.setattr('builtins.print', mock_print)
            m.setattr(GoProCamera.GoPro, 'parse_value',
                      lambda s, p, v: 'parsed')
            m.setattr(GoProCamera.GoPro, 'getStatus',
                      lambda s, p, v: 'status')
            m.setattr(GoProCamera.GoPro, 'infoCamera',
                      lambda s, p: 'info')
            self.goprocam.overview()


class OverviewAuthTest(GoProCameraAuthTest):
    def test_overview(self):
        def mock_print(*args, **kwargs):
            for arg in args:
                assert arg in [
                    'camera overview',
                    'current mode: parsed',
                    'current video resolution: parsed',
                    'current photo resolution: parsed',
                    'current timelapse interval: parsed',
                    'current video Fov: parsed',
                    'status lights: parsed',
                    'recording: parsed',
                    ]
        with self.monkeypatch.context() as m:
            m.setattr('builtins.print', mock_print)
            m.setattr(GoProCamera.GoPro, 'parse_value',
                      lambda s, p, v: 'parsed')
            m.setattr(GoProCamera.GoPro, 'getStatus',
                      lambda s, p: 'status')
            self.goprocam.overview()
