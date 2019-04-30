from unittest import TestCase
from goprocam import GoProCamera
import urllib.request
import io
import sys

import pytest
from _pytest.monkeypatch import MonkeyPatch

# this is optional
try:
    import getmac
except ImportError:
    pass


class ImportTest(TestCase):
    def setUp(self):
        self.monkeypatch = MonkeyPatch()

    def test_instantiate_gpcontrol(self):
        ''' GoPro object can be instantiated '''
        # need to prevent it from actually talking to the camera
        def fake_request(url, timeout=None):
            assert url == 'http://10.5.5.9/gp/gpControl'
            # return something that will show as a gpcontrol camera
            return io.BytesIO("""
{"info": {"firmware_version": "HD3.02", "model_name": "dummy"}}
""".encode('utf8'))
        self.monkeypatch.setattr(urllib.request, 'urlopen', fake_request)

        # if this optional module is available, stub it out
        if sys.modules.get('getmac'):
            def fakemac(ip=''):
                return 'DE:AD:BE:EF'
            self.monkeypatch.setattr(getmac, 'get_mac_address', fakemac)

        camera = GoProCamera.GoPro()
        assert camera, "got a camera object"
        assert camera.ip_addr == '10.5.5.9'
        assert camera._mac_address == fakemac(ip=None)
        assert camera._camera == 'gpcontrol'


