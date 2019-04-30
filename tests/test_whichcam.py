from unittest import TestCase
from goprocam import GoProCamera
import urllib.request
import io
import sys
import json
import time
import http

import pytest
from _pytest.monkeypatch import MonkeyPatch
from urllib.error import HTTPError, URLError
from socket import timeout

try:
    import getmac
except ImportError:
    pass

class WhichCamTest(TestCase):
    def setUp(self):
        self.monkeypatch = MonkeyPatch()

        self.responses = {
            '/gp/gpControl': {
                'info': {
                    'firmware_version': 'HD3.02',
                    'model_name': 'dummy',
                    },
                },
            }

        def fake_request(url, timeout=None):
            path = url.replace('http://10.5.5.9', '')
            try:
                if isinstance(self.responses[path], Exception):
                    raise self.responses[path]
                if type(self.responses[path]) == str:
                    res = io.BytesIO(self.responses[path].encode('utf8'))
                else:
                    res = io.BytesIO(json.dumps(self.responses[path]).encode('utf8'))
                # v. ropey
                class Info(object):
                    def get_content_charset(self, charset):
                        return 'utf8'
                res.info = Info
                return res
            except KeyError as e:
                raise HTTPError(url, 404, 'Not Found', None, None)
        self.monkeypatch.setattr(urllib.request, 'urlopen', fake_request)

        # if this optional module is available, stub it out
        def fakemac(ip=''):
            return 'DE:AD:BE:EF'
        if sys.modules.get('getmac'):
            self.monkeypatch.setattr(getmac, 'get_mac_address', fakemac)

        # stop it from sending the WoL packet
        self.monkeypatch.setattr(GoProCamera.GoPro, 'power_on', lambda s, mac_address: s)

        # and disable this as we'll test it separately
        self.monkeypatch.setattr(GoProCamera.GoPro, 'prepare_gpcontrol', lambda self: self)

        self.goprocam = GoProCamera.GoPro(camera='gpcontrol', mac_address=fakemac(ip=None))

    def test_already_deetected(self):
        assert self.goprocam.whichCam() == 'gpcontrol'

    def test_detection_exceptions(self):
        # this would, of course, be better as a parametrised test
        for firmware_version in ['HX', 'FS', 'HD3.02', 'H18', 'HD3.22.01.50']:
            self.goprocam._camera = ''
            self.responses['/gp/gpControl']['info']['firmware_version'] = firmware_version
            assert self.goprocam.whichCam() == 'gpcontrol'

    def test_auth_detection(self):
        self.goprocam._camera = ''
        self.responses['/camera/cv'] = 'Hero3'
        for firmware_version in ['HD2', '4', 'HD3.1']:
            self.responses['/gp/gpControl']['info']['firmware_version'] = firmware_version
            assert self.goprocam.whichCam() == 'auth'

    def test_auth_detecation_without_gpcontrol(self):
        self.goprocam._camera = ''
        self.responses = {'/camera/cv': 'Hero3'}
        assert self.goprocam.whichCam() == 'auth'

    def test_gpcontrol_detecation_without_gpcontrol(self):
        self.goprocam._camera = ''
        del(self.responses['/gp/gpControl'])
        self.responses['/camera/cv'] = 'Hero2'
        assert self.goprocam.whichCam() == '' # srsly

    def test_gpcontrol_detection_without_gpcontrol(self):
        # this will attempt to power on the camera - which we have intercepted
        self.goprocam._camera = ''
        self.responses = {}
        self.monkeypatch.setattr(time, 'sleep', lambda x: False)
        assert self.goprocam.whichCam() == ''

    def test_cv_timeout_while_detecting(self):
        self.goprocam._camera = ''
        self.responses = {'/camera/cv': timeout()}
        self.monkeypatch.setattr(time, 'sleep', lambda x: False)
        assert self.goprocam.whichCam() == ''

    def test_gpcontrol_timeout_while_detecting_hero3(self):
        self.goprocam._camera = ''
        self.responses['/gp/gpControl'] = timeout()
        # this copes poorly with errors, so help it along
        self.responses['/camera/cv'] = 'Hero3'
        self.monkeypatch.setattr(time, 'sleep', lambda x: False)
        assert self.goprocam.whichCam() == 'auth'

    def test_gpcontrol_timeout_while_detecting_hero2(self):
        self.goprocam._camera = ''
        self.responses['/gp/gpControl'] = timeout()
        # this copes poorly with errors, so help it along
        self.responses['/camera/cv'] = 'Hero2'
        self.monkeypatch.setattr(time, 'sleep', lambda x: False)
        assert self.goprocam.whichCam() == ''

    def test_gpcontrol_exception_while_detecting(self):
        self.goprocam._camera = ''
        self.responses['/gp/gpControl'] = http.client.HTTPException()
        # this copes poorly with errors, so help it along
        self.responses['/camera/cv'] = 'Hero3'
        self.monkeypatch.setattr(time, 'sleep', lambda x: False)
        # different power-on!
        self.monkeypatch.setattr(GoProCamera.GoPro, 'power_on_auth', lambda self: self)
        assert self.goprocam.whichCam() == 'auth'
