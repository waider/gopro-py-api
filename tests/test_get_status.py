from .conftest import GoProCameraTest
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
        self.goprocam.getStatus(param, value)

    def test_get_status_gpcontrol_error(self):
        param = Status.Settings
        value = Status.STATUS.Battery
        self.goprocam.getStatus(param, value)

    def test_get_status_gpcontrol_timeout(self):
        param = Status.Settings
        value = Status.STATUS.Battery
        self.responses['/gp/gpControl/status'] = timeout()
        self.goprocam.getStatus(param, value)

    def test_get_Status_auth(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getPassword',
                      lambda self: 'password')
            self.goprocam._camera = 'auth'
            param = (0, 1)  # this is a bit weird

            self.responses['/camera/sx?t=password'] = 'AB'

            status = self.goprocam.getStatus(param)
