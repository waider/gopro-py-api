from .conftest import GoProCameraTest, GoProCameraAuthTest,\
    GoProCameraUnknownTest, verify_uncalled
from goprocam import GoProCamera
from goprocam.constants import Video, Hero3Commands


class VideoSettingsUnknownCamTest(GoProCameraUnknownTest):
    def setUp(self):
        super().setUp()

    def test_video_settings(self):
        with self.monkeypatch.context() as m:
            m.setattr('builtins.print', verify_uncalled)
            self.goprocam.video_settings(None)


class VideoSettingsTest(GoProCameraTest):
    def test_video_settings_resolution(self):
        with self.monkeypatch.context() as m:
            def control_verify(self, param, value):
                assert param == Video.RESOLUTION

            m.setattr(GoProCamera.GoPro, 'gpControlSet', control_verify)
            for res in [c.replace('R', '') for c in Video.Resolution.__dict__
                        if type(c) == str and c[0] >= 'A' and c[0] <= 'Z']:
                self.goprocam.video_settings(res)

    def test_video_settings_resolution_and_fps(self):
        with self.monkeypatch.context() as m:
            def control_verify(self, param, value):
                assert param in [Video.RESOLUTION, Video.FRAME_RATE]

            m.setattr(GoProCamera.GoPro, 'gpControlSet', control_verify)
            for res in [c.replace('R', '') for c in Video.Resolution.__dict__
                        if type(c) == str and c[0] >= 'A' and c[0] <= 'Z']:
                for fps in [f.replace('FR',
                                      '') for f in Video.FrameRate.__dict__
                            if type(f) == str and f[0] >= 'A' and f[0] <= 'Z']:
                    self.goprocam.video_settings(res, fps)


class VideoSettingsAuthTest(GoProCameraAuthTest):
    def test_video_settings_resolution(self):
        with self.monkeypatch.context() as m:
            def control_verify(self, param, value):
                assert param == Hero3Commands.VIDEO_RESOLUTION
                assert value == self.expected_resolution

            m.setattr(GoProCamera.GoPro, 'sendCamera', control_verify)
            for res, val in [('4k', '06'), ('4K_Widescreen', '08'),
                             ('2kCin', '07'), ('2_7k', '05'),
                             ('1440p', '04'), ('1080p', '03'),
                             ('960p', '02'), ('720p', '01'),
                             ('480p', '00')]:
                self.goprocam.expected_resolution = val
                self.goprocam.video_settings(res)

    def test_video_settings_resolution_and_fps(self):
        with self.monkeypatch.context() as m:
            def control_verify(self, param, value):
                assert param in [Hero3Commands.VIDEO_RESOLUTION,
                                 Hero3Commands.FRAME_RATE]
                if param == Hero3Commands.VIDEO_RESOLUTION:
                    assert value == self.expected_resolution
                else:
                    assert value == self.expected_fps

            m.setattr(GoProCamera.GoPro, 'sendCamera', control_verify)
            for res, val in [('4k', '06'), ('4K_Widescreen', '08'),
                             ('2kCin', '07'), ('2_7k', '05'),
                             ('1440p', '04'), ('1080p', '03'),
                             ('960p', '02'), ('720p', '01'),
                             ('480p', '00')]:
                self.goprocam.expected_resolution = val
                # v. ugly
                for fps in [f for f in Hero3Commands.FrameRate.__dict__
                            if type(f) == str and f[0] >= 'A' and f[0] <= 'Z']:
                    self.goprocam.expected_fps =\
                        eval('Hero3Commands.FrameRate.' + fps)
                    self.goprocam.video_settings(res, fps.replace('FPS', ''))

    def test_video_settings_unknown_resolution(self):
        with self.monkeypatch.context() as m:
            m.setattr('builtins.print', verify_uncalled)
            m.setattr(GoProCamera.GoPro, 'sendCamera', verify_uncalled)
            self.goprocam.video_settings('unknown')
