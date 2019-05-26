from .conftest import GoProCameraTest
from goprocam import GoProCamera


class StreamSettingsTest(GoProCameraTest):
    def test_stream_settings(self):
        with self.monkeypatch.context() as m:
            def verify_gp_control_set(self, param, value):
                assert param in ['62', '64']
                assert value in ['1', '2']
            m.setattr(GoProCamera.GoPro, 'gpControlSet',
                      verify_gp_control_set)
            self.goprocam.streamSettings(bitrate='1', resolution='2')
