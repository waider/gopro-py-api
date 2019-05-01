from unittest import TestCase
from goprocam import GoProCamera
import urllib.request
import io
import sys
import json
import time
import pytest
from _pytest.monkeypatch import MonkeyPatch
from urllib.error import HTTPError, URLError

try:
    import getmac
except ImportError:
    pass


class GoProCameraTest(TestCase):
    def setUp(self):
        self.monkeypatch = MonkeyPatch()

        # Default response to pretend I'm a GoPro HERO+
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
                # v. ropey. We want to pretend our result is a HTTP response,
                # a little.
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

        # stop it from sending the WoL packet during __init__
        self.monkeypatch.setattr(GoProCamera.GoPro, 'power_on', lambda s, mac_address: s)

        # and disable this as we'll test it separately
        self.goprocam = GoProCamera.GoPro(camera='gpcontrol', mac_address=fakemac(ip=None))
