from .conftest import GoProCameraTest, GoProCameraAuthTest,\
    GoProCameraUnknownTest, verify_uncalled
from goprocam import constants, GoProCamera


class IsRecordingUnknownTest(GoProCameraUnknownTest):
    def test_is_recording(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getStatus', verify_uncalled)
            assert self.goprocam.IsRecording() is None


class IsRecordingTest(GoProCameraTest):
    def test_is_recording(self):
        with self.monkeypatch.context() as m:
            def verify_status(self, param, value):
                assert param == constants.Status.Status
                assert value == constants.Status.STATUS.IsRecording
                return 1

            m.setattr(GoProCamera.GoPro, 'getStatus', verify_status)
            assert self.goprocam.IsRecording() == 1


class IsRecordingAuthTest(GoProCameraAuthTest):
    def test_is_recording(self):
        with self.monkeypatch.context() as m:
            def verify_status(self, param):
                assert param == constants.Hero3Status.IsRecording
                return '01'

            m.setattr(GoProCamera.GoPro, 'getStatus', verify_status)
            assert self.goprocam.IsRecording() == 1

    def test_is_not_recording(self):
        with self.monkeypatch.context() as m:
            def verify_status(self, param):
                assert param == constants.Hero3Status.IsRecording
                return '00'

            m.setattr(GoProCamera.GoPro, 'getStatus', verify_status)
            assert self.goprocam.IsRecording() == 0
