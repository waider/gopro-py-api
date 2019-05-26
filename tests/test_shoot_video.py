from .conftest import GoProCameraTest, GoProCameraAuthTest,\
    GoProCameraUnknownTest, verify_uncalled
from goprocam import GoProCamera, constants


class ShootVideoUnknownTest(GoProCameraUnknownTest):
    def test_shoot_video(self):
        with self.monkeypatch.context() as m:
            def verify_mode(self, mode):
                assert mode == constants.Mode.VideoMode

            def verify_shutter(self, param):
                assert param in [constants.start, constants.stop]

            m.setattr(GoProCamera.GoPro, 'mode', verify_mode)
            m.setattr(GoProCamera.GoPro, 'shutter', verify_shutter)
            m.setattr(GoProCamera.GoPro, 'getMedia', verify_uncalled)
            assert self.goprocam.shoot_video(duration=3) is None


class ShootVideoTest(GoProCameraTest):
    def test_shoot_video_zero_duration(self):
        with self.monkeypatch.context() as m:
            def verify_mode(self, mode):
                assert mode == constants.Mode.VideoMode

            def verify_shutter(self, param):
                assert param == constants.start

            m.setattr(GoProCamera.GoPro, 'mode', verify_mode)
            m.setattr(GoProCamera.GoPro, 'shutter', verify_shutter)
            m.setattr(GoProCamera.GoPro, 'getMedia', verify_uncalled)
            assert self.goprocam.shoot_video() is None

    def test_shoot_video(self):
        with self.monkeypatch.context() as m:
            def verify_mode(self, mode):
                assert mode == constants.Mode.VideoMode

            def verify_shutter(self, param):
                if not self.started:
                    assert param == constants.start
                    self.started = True
                else:
                    assert param == constants.stop
                    self.started = False

            def fake_status(self, status, substatus):
                assert status == constants.Status.Status
                assert substatus == constants.Status.STATUS.IsBusy
                self.status = self.status + 1
                return self.status

            m.setattr(GoProCamera.GoPro, 'mode', verify_mode)
            m.setattr(GoProCamera.GoPro, 'shutter', verify_shutter)
            m.setattr(GoProCamera.GoPro, 'getMedia',
                      lambda self: 'http://10.5.5.9:8080/videos/DCIME/1/2')
            m.setattr(GoProCamera.GoPro, 'getStatus', fake_status)

            # storing state in object under test FIXME
            self.goprocam.started = False
            self.goprocam.status = 0

            # must record for > 2 seconds to trigger start + stop
            assert self.goprocam.shoot_video(duration=3) == \
                'http://10.5.5.9:8080/videos/DCIME/1/2'


class ShootVideoAuthTest(GoProCameraAuthTest):
    def test_shoot_video(self):
        with self.monkeypatch.context() as m:
            def verify_mode(self, mode):
                assert mode == constants.Mode.VideoMode

            def verify_shutter(self, param):
                if not self.started:
                    assert param == constants.start
                    self.started = True
                else:
                    assert param == constants.stop
                    self.started = False

            def fake_status(self, status):
                assert status == constants.Hero3Status.IsRecording
                if self.status == 0:
                    self.status = 1
                    return '01'
                else:
                    self.status = 0
                    return '00'

            m.setattr(GoProCamera.GoPro, 'mode', verify_mode)
            m.setattr(GoProCamera.GoPro, 'shutter', verify_shutter)
            m.setattr(GoProCamera.GoPro, 'getMedia',
                      lambda self: 'http://10.5.5.9:8080/videos/DCIME/1/2')
            m.setattr(GoProCamera.GoPro, 'getStatus', fake_status)

            # storing state in object under test FIXME
            self.goprocam.started = False
            self.goprocam.status = 0

            # must record for > 2 seconds to trigger start + stop
            assert self.goprocam.shoot_video(duration=3) == \
                'http://10.5.5.9:8080/videos/DCIME/1/2'
