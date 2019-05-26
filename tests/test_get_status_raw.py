from .conftest import GoProCameraTest, GoProCameraAuthTest,\
    GoProCameraUnknownTest
from goprocam import GoProCamera

from goprocam.constants import Status

import json
from socket import timeout


class GetStatusRawTest(GoProCameraTest):
    def test_get_status_raw_gpcontrol(self):
        param = Status.Settings
        value = Status.STATUS.Battery
        self.responses['/gp/gpControl/status'] = {
            param: {
                # dummy value for now as I don't know what the real ones are
                value: 1,
                }
            }
        assert self.goprocam.getStatusRaw() ==\
            json.dumps(self.responses['/gp/gpControl/status'])

    def test_get_status_raw_gpcontrol_error(self):
        assert self.goprocam.getStatusRaw() == ''

    def test_get_status_raw_gpcontrol_timeout(self):
        self.responses['/gp/gpControl/status'] = timeout()
        assert self.goprocam.getStatusRaw() == ''


class GetStatusRawAuthTest(GoProCameraAuthTest):
    def test_get_status_raw_auth(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getPassword',
                      lambda self: 'password')
            self.responses['/camera/sx?t=password'] = b'\xAB'

            assert self.goprocam.getStatusRaw() == b'\xab'

    def test_get_status_raw_auth_error(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getPassword',
                      lambda self: 'password')
            assert self.goprocam.getStatusRaw() == ''

    def test_get_status_raw_auth_timeout(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getPassword',
                      lambda self: 'password')
            self.responses['/camera/sx?t=password'] = timeout()
            assert self.goprocam.getStatusRaw() == ''


class GetStatusRawUnknownTest(GoProCameraUnknownTest):
    def test_get_status_raw_undefined(self):
        assert self.goprocam.getStatusRaw() is None
