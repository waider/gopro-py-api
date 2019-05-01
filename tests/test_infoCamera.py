from socket import timeout

from goprocam.constants import Camera

from .conftest import GoProCameraTest


class InfoCameraTest(GoProCameraTest):
    # gpcontrol camera
    def test_default_info_camera(self):
        with self.monkeypatch.context() as m:
            m.setattr(self.goprocam, 'whichCam', lambda: 'gpcontrol')
            info = self.goprocam.infoCamera()
        assert info == self.responses['/gp/gpControl']['info']

    def test_detailed_info_camera(self):
        with self.monkeypatch.context() as m:
            m.setattr(self.goprocam, 'whichCam', lambda: 'gpcontrol')
            # definitely hokey
            for detail in [c for c in Camera.__dict__
                           if type(c) == str and c[0] >= 'A' and c[0] <= 'Z']:
                info = self.goprocam.infoCamera(getattr(Camera, detail))
                assert info == \
                    self.responses['/gp/gpControl']['info'][getattr(Camera,
                                                                    detail)]

    def test_default_info_camera_error(self):
        with self.monkeypatch.context() as m:
            m.setattr(self.goprocam, 'whichCam', lambda: 'gpcontrol')
            del(self.responses['/gp/gpControl'])
            info = self.goprocam.infoCamera()
        assert info == ""

    def test_default_info_camera_timeout(self):
        with self.monkeypatch.context() as m:
            m.setattr(self.goprocam, 'whichCam', lambda: 'gpcontrol')
            self.responses['/gp/gpControl'] = timeout()
            info = self.goprocam.infoCamera()
        assert info == ""

    # Testing 'auth' cameras
    def test_default_info_camera_auth(self):
        with self.monkeypatch.context() as m:
            m.setattr(self.goprocam, 'whichCam', lambda: 'auth')
            info = self.goprocam.infoCamera()
        assert info is None

    def test_default_info_camera_model_name(self):
        with self.monkeypatch.context() as m:
            m.setattr(self.goprocam, 'whichCam', lambda: 'auth')
            self.responses['/camera/cv'] = 'Hero3'
            info = self.goprocam.infoCamera(option='model_name')
        assert info == 'bHero3'

    def test_default_info_camera_firmware_version(self):
        with self.monkeypatch.context() as m:
            m.setattr(self.goprocam, 'whichCam', lambda: 'auth')
            self.responses['/camera/cv'] = 'Hero3'
            info = self.goprocam.infoCamera(option='firmware_version')
        assert info == 'bHero3'

    def test_default_info_camera_ssid(self):
        with self.monkeypatch.context() as m:
            m.setattr(self.goprocam, 'whichCam', lambda: 'auth')
            self.responses['/bacpac/cv'] = 'fakessid'
            info = self.goprocam.infoCamera(option='ssid')
        assert info == 'bfakessid'

    def test_default_info_camera_model_name_error(self):
        with self.monkeypatch.context() as m:
            m.setattr(self.goprocam, 'whichCam', lambda: 'auth')
            info = self.goprocam.infoCamera(option='model_name')
        assert info == ''

    def test_default_info_camera_model_name_timeout(self):
        with self.monkeypatch.context() as m:
            m.setattr(self.goprocam, 'whichCam', lambda: 'auth')
            self.responses['/camera/cv'] = timeout()
            info = self.goprocam.infoCamera(option='model_name')
        assert info == ''

    def test_default_info_camera_firmware_version_error(self):
        with self.monkeypatch.context() as m:
            m.setattr(self.goprocam, 'whichCam', lambda: 'auth')
            info = self.goprocam.infoCamera(option='firmware_version')
        assert info == ''

    def test_default_info_camera_firmware_version_timeout(self):
        with self.monkeypatch.context() as m:
            m.setattr(self.goprocam, 'whichCam', lambda: 'auth')
            self.responses['/camera/cv'] = timeout()
            info = self.goprocam.infoCamera(option='firmware_version')
        assert info == ''

    def test_default_info_camera_ssid_error(self):
        with self.monkeypatch.context() as m:
            m.setattr(self.goprocam, 'whichCam', lambda: 'auth')
            info = self.goprocam.infoCamera(option='ssid')
        assert info == ''

    def test_default_info_camera_ssid_timeout(self):
        with self.monkeypatch.context() as m:
            m.setattr(self.goprocam, 'whichCam', lambda: 'auth')
            self.responses['/bacpac/cv'] = timeout()
            info = self.goprocam.infoCamera(option='ssid')
        assert info == ''

    # undefined camera
    def test_default_info_camera_unknown(self):
        with self.monkeypatch.context() as m:
            m.setattr(self.goprocam, 'whichCam', lambda: None)
            info = self.goprocam.infoCamera()
        assert info is None
