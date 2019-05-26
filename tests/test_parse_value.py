from .conftest import GoProCameraTest, GoProCameraAuthTest
from goprocam import constants


class ParseValueTest(GoProCameraTest):
    def test_parse_video_left(self):
        assert self.goprocam.parse_value('video_left', 0) == '00:00:00'

    def test_parse_rem_space(self):
        for inp, out in [(0, 'No SD'),
                         (1024, '1000.0KB'), (1024*1024, '1000.0MB'),
                         (1024 * 1024 * 1024, '1000.0GB'),
                         (1024 * 1024 * 1024 * 1024, '1000.0TB'),
                         ]:  # "TB", "PB", "EB", "ZB", "YB"
            assert self.goprocam.parse_value('rem_space', inp) == out

    def test_parse_rem_space_heri4_session(self):
        self.responses['/gp/gpControl']['info']['model_name'] = 'HERO4 Session'
        for inp, out in [(1, '1.0B'), (1024, '1.0KB'), (1024*1024, '1.0MB'),
                         (1024 * 1024 * 1024, '1.0GB'),
                         (1024 * 1024 * 1024 * 1024, '1.0TB'),
                         ]:  # "TB", "PB", "EB", "ZB", "YB"
            assert self.goprocam.parse_value('rem_space', inp) == out

    def test_parse_media_size(self):
        for inp, out in [(1024, '1.0KB'), (1024*1024, '1.0MB'),
                         (1024 * 1024 * 1024, '1.0GB'),
                         (1024 * 1024 * 1024 * 1024, '1.0TB'),
                         ]:  # "TB", "PB", "EB", "ZB", "YB"
            assert self.goprocam.parse_value('media_size', inp) == out

    def test_parse_mode(self):
        for inp, out in [(0, 'Video'), (1, 'Photo'), (2, 'Multi-Shot'),
                         (3, None)]:
            assert self.goprocam.parse_value('mode', inp) == out

    def test_parse_video_sub_mode(self):
        self.responses['/gp/gpControl/status'] = {
            'status': {
                constants.Status.STATUS.Mode: 0
                }
            }

        for inp, out in [(0, 'Video'), (1, 'TimeLapse Video'),
                         (2, 'Video+Photo'), (3, 'Looping'),
                         (4, None)]:
            assert self.goprocam.parse_value('sub_mode', inp) == out

    def test_parse_photo_sub_mode(self):
        self.responses['/gp/gpControl/status'] = {
            'status': {
                constants.Status.STATUS.Mode: 1
                }
            }

        for inp, out in [(0, 'Single Pic'), (1, 'Burst'),
                         (2, 'NightPhoto'), (3, None)]:
            assert self.goprocam.parse_value('sub_mode', inp) == out

    def test_parse_multishot_sub_mode(self):
        self.responses['/gp/gpControl/status'] = {
            'status': {
                constants.Status.STATUS.Mode: 2
                }
            }

        for inp, out in [(0, 'Burst'), (1, 'TimeLapse'),
                         (2, 'Night lapse'), (3, None)]:
            assert self.goprocam.parse_value('sub_mode', inp) == out

    def test_parse_recording(self):
        for inp, out in [(0, 'Not recording - standby'),
                         (1, 'RECORDING!'), (2, None)]:
            assert self.goprocam.parse_value('recording', inp) == out

    def test_parse_battery(self):
        for inp, out in [(0, 'Nearly Empty'), (1, 'LOW'), (2, 'Halfway'),
                         (3, 'Full'), (4, 'Charging'), (5, None)]:
            assert self.goprocam.parse_value('battery', inp) == out

    def test_parse_video_res(self):
        for inp, out in [(1, '4k'), (2, '4kSV'), (4, '2k'), (5, '2kSV'),
                         (6, '2k4by3'), (7, '1440p'), (8, '1080pSV'),
                         (9, '1080p'), (10, '960p'), (11, '720pSV'),
                         (12, '720p'), (13, '480p'), (14, '5.2K'), (15, '3K'),
                         (-1, 'out of scope')]:
            assert self.goprocam.parse_value('video_res', inp) == out

    def test_parse_vide_fr(self):
        for inp, out in [(0, '240'), (1, '120'), (2, '100'), (5, '60'),
                         (6, '50'), (7, '48'), (8, '30'), (9, '25'),
                         (10, '24'), (-1, 'out of scope')]:
            assert self.goprocam.parse_value('video_fr', inp) == out

    def test_parse_unknown(self):
        assert self.goprocam.parse_value('-x-x-x', None) is None


class ParseValueAuthTest(GoProCameraAuthTest):
    def test_mode(self):
        for inp, out in [('00', 'Video'), ('01', 'Photo'), ('02', 'Burst'),
                         ('03', 'Timelapse'), ('04', 'Settings'),
                         ('05', None)]:
            assert self.goprocam.parse_value(constants.Hero3Status.Mode,
                                             inp) == out

    def test_time_lapse_interval(self):
        for inp, out in [('00', '0.5s'), ('01', '1s'), ('02', '2s'),
                         ('03', '5s'), ('04', '10s'), ('05', '30s'),
                         ('06', '1min'), ('07', None)]:
            assert self.goprocam.parse_value(
                constants.Hero3Status.TimeLapseInterval, inp) == out

    def test_verious_booleans(self):
        for inp, out in [('00', 'OFF'), ('01', 'ON'), ('02', 'ON'),
                         ('03', None)]:
            for param in [constants.Hero3Status.LED,
                          constants.Hero3Status.Beep,
                          constants.Hero3Status.SpotMeter,
                          constants.Hero3Status.IsRecording]:
                assert self.goprocam.parse_value(param, inp) == out

    def test_fov(self):
        for inp, out in [('00', 'Wide'), ('01', 'Medium'), ('02', 'Narrow'),
                         ('04', None)]:
            assert self.goprocam.parse_value(constants.Hero3Status.FOV,
                                             inp) == out

    def test_picres(self):
        for inp, out in [('5', '12mp'), ('6', '7mp m'), ('4', '7mp w'),
                         ('3', '5mp m'), ('0', None)]:
            assert self.goprocam.parse_value(constants.Hero3Status.PicRes,
                                             inp) == out

    def test_videomode(self):
        for inp, out in [('00', 'WVGA'), ('01', '720p'), ('02', '960p'),
                         ('03', '1080p'), ('04', '1440p'), ('05', '2.7K'),
                         ('06', '2.7K Cinema'), ('07', '4K'),
                         ('08', '4K Cinema'), ('09', '1080p SuperView'),
                         ('0a', '720p SuperView'), ('ff', None)]:
            assert self.goprocam.parse_value(constants.Hero3Status.VideoRes,
                                             inp) == out

    def test_charging(self):
        for inp, out in [('3', 'NO'), ('4', 'YES'), ('5', None)]:
            assert self.goprocam.parse_value(constants.Hero3Status.Charging,
                                             inp) == out

    def test_protune(self):
        for inp, out in [('4', 'OFF'), ('6', 'ON'), ('7', None)]:
            assert self.goprocam.parse_value(constants.Hero3Status.Protune,
                                             inp) == out
