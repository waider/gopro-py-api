from .conftest import GoProCameraTest, GoProCameraAuthTest,\
    GoProCameraUnknownTest
from goprocam import GoProCamera

from goprocam.constants import Status

from socket import timeout


class GetStatusTest(GoProCameraTest):
    def test_get_status_gpcontrol(self):
        param = Status.Settings
        value = Status.STATUS.Battery
        self.responses['/gp/gpControl/status'] = {
            param: {
                # dummy value for now as I don't know what the real ones are
                value: 1,
                }
            }
        # could check all of 'em, but ok for now
        assert self.goprocam.getStatus(param, value) == 1

    def test_get_status_gpcontrol_error(self):
        param = Status.Settings
        value = Status.STATUS.Battery
        assert self.goprocam.getStatus(param, value) == ''

    def test_get_status_gpcontrol_timeout(self):
        param = Status.Settings
        value = Status.STATUS.Battery
        self.responses['/gp/gpControl/status'] = timeout()
        assert self.goprocam.getStatus(param, value) == ''


class GetStatusAuthTest(GoProCameraAuthTest):
    def test_get_status(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getPassword',
                      lambda self: 'password')
            param = (0, 1)  # this is a bit weird

            self.responses['/camera/sx?t=password'] = b'\xAB'

            assert self.goprocam.getStatus(param) == 'A'


class GetStatusUnknownTest(GoProCameraUnknownTest):
    def test_get_status(self):
        assert self.goprocam.getStatus('dummy') is None
