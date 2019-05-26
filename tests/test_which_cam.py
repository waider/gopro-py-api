import http
from socket import timeout

from goprocam import GoProCamera

from .conftest import GoProCameraTest


class WhichCamTest(GoProCameraTest):
    def setUp(self):
        super().setUp()
        # disable this so we can test it separately
        self.monkeypatch.setattr(GoProCamera.GoPro, 'prepare_gpcontrol',
                                 lambda self: self)

    def test_already_deetected(self):
        assert self.goprocam.whichCam() == 'gpcontrol'

    def test_detection_exceptions(self):
        # this would, of course, be better as a parametrised test
        for firmware_version in ['HX', 'FS', 'HD3.02', 'H18', 'HD3.22.01.50']:
            self.goprocam._camera = ''
            self.responses['/gp/gpControl']['info']['firmware_version'] = \
                firmware_version
            assert self.goprocam.whichCam() == 'gpcontrol'

    def test_auth_detection(self):
        self.goprocam._camera = ''
        self.responses['/camera/cv'] = 'Hero3'
        for firmware_version in ['HD2', '4', 'HD3.1']:
            self.responses['/gp/gpControl']['info']['firmware_version'] = \
                firmware_version
            assert self.goprocam.whichCam() == 'auth'

    def test_auth_detection_not_hero3(self):
        self.goprocam._camera = ''
        self.responses['/camera/cv'] = 'Hero2'
        for firmware_version in ['HD2', '4', 'HD3.1']:
            self.responses['/gp/gpControl']['info']['firmware_version'] = \
                firmware_version
            assert self.goprocam.whichCam() == ''

    def test_auth_detection_without_gpcontrol(self):
        self.goprocam._camera = ''
        self.responses = {'/camera/cv': 'Hero3'}
        assert self.goprocam.whichCam() == 'auth'

    def test_gpcontrol_detection_without_gpcontrol_not_hero3(self):
        self.goprocam._camera = ''
        del(self.responses['/gp/gpControl'])
        self.responses['/camera/cv'] = 'Hero2'
        assert self.goprocam.whichCam() == ''

    def test_gpcontrol_detection_without_gpcontrol(self):
        # this will attempt to power on the camera - which we have intercepted
        self.goprocam._camera = ''
        self.responses = {}
        assert self.goprocam.whichCam() == ''

    def test_cv_timeout_while_detecting(self):
        self.goprocam._camera = ''
        self.responses = {'/camera/cv': timeout()}
        assert self.goprocam.whichCam() == ''

    def test_gpcontrol_timeout_while_detecting_hero3(self):
        self.goprocam._camera = ''
        self.responses['/gp/gpControl'] = timeout()
        # this copes poorly with errors, so help it along
        self.responses['/camera/cv'] = 'Hero3'
        assert self.goprocam.whichCam() == 'auth'

    def test_gpcontrol_timeout_while_detecting_hero2(self):
        self.goprocam._camera = ''
        self.responses['/gp/gpControl'] = timeout()
        # this copes poorly with errors, so help it along
        self.responses['/camera/cv'] = 'Hero2'
        assert self.goprocam.whichCam() == ''

    def test_gpcontrol_exception_while_detecting(self):
        self.goprocam._camera = ''
        self.responses['/gp/gpControl'] = http.client.HTTPException()
        # this copes poorly with errors, so help it along
        self.responses['/camera/cv'] = 'Hero3'
        # different power-on!
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert isinstance(args, http.client.HTTPException) or \
                    args == 'HERO3/3+'
            m.setattr('builtins.print', print_verify)
            m.setattr(GoProCamera.GoPro, 'power_on_auth', lambda self: self)
            assert self.goprocam.whichCam() == 'auth'

    def test_gpcontrol_exception_while_detecting_not_hero3(self):
        self.goprocam._camera = ''
        self.responses['/gp/gpControl'] = http.client.HTTPException()
        # this copes poorly with errors, so help it along
        self.responses['/camera/cv'] = 'Hero2'
        # different power-on!
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert isinstance(args, http.client.HTTPException)
            m.setattr('builtins.print', print_verify)
            m.setattr(GoProCamera.GoPro, 'power_on_auth', lambda self: self)
            assert self.goprocam.whichCam() == 'auth'
