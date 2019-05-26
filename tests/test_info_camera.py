from .conftest import GoProCameraTest, GoProCameraAuthTest,\
    GoProCameraUnknownTest
from socket import timeout
from goprocam.constants import Camera


class InfoCameraTest(GoProCameraTest):
    def test_default_info_camera(self):
        assert self.goprocam.infoCamera() ==\
            self.responses['/gp/gpControl']['info']

    def test_detailed_info_camera(self):
        # definitely hokey
        for detail in [c for c in Camera.__dict__
                       if type(c) == str and c[0] >= 'A' and c[0] <= 'Z']:
            assert self.goprocam.infoCamera(getattr(Camera, detail)) ==\
                self.responses['/gp/gpControl']['info'][getattr(Camera,
                                                                detail)]

    def test_default_info_camera_error(self):
        del(self.responses['/gp/gpControl'])
        assert self.goprocam.infoCamera() == ""

    def test_default_info_camera_timeout(self):
        self.responses['/gp/gpControl'] = timeout()
        assert self.goprocam.infoCamera() == ""


class InfoCameraAuthTest(GoProCameraAuthTest):
    def test_default_info_camera_auth(self):
        assert self.goprocam.infoCamera() is None

    def test_default_info_camera_model_name(self):
        self.responses['/camera/cv'] = 'Hero3'
        assert self.goprocam.infoCamera(option='model_name') == 'bHero3'

    def test_default_info_camera_firmware_version(self):
        self.responses['/camera/cv'] = 'Hero3'
        assert self.goprocam.infoCamera(option='firmware_version') == 'bHero3'

    def test_default_info_camera_ssid(self):
        self.responses['/bacpac/cv'] = 'fakessid'
        assert self.goprocam.infoCamera(option='ssid') == 'bfakessid'

    def test_default_info_camera_model_name_error(self):
        assert self.goprocam.infoCamera(option='model_name') == ''

    def test_default_info_camera_model_name_timeout(self):
        self.responses['/camera/cv'] = timeout()
        assert self.goprocam.infoCamera(option='model_name') == ''

    def test_default_info_camera_firmware_version_error(self):
        assert self.goprocam.infoCamera(option='firmware_version') == ''

    def test_default_info_camera_firmware_version_timeout(self):
        self.responses['/camera/cv'] = timeout()
        assert self.goprocam.infoCamera(option='firmware_version') == ''

    def test_default_info_camera_ssid_error(self):
        assert self.goprocam.infoCamera(option='ssid') == ''

    def test_default_info_camera_ssid_timeout(self):
        self.responses['/bacpac/cv'] = timeout()
        assert self.goprocam.infoCamera(option='ssid') == ''


class InfoCameraUnknownTest(GoProCameraUnknownTest):
    def test_default_info_camera_unknown(self):
        assert self.goprocam.infoCamera() is None
