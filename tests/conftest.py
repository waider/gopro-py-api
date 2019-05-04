import io
import json
import logging
import sys
import time
import urllib.request
from unittest import TestCase
from urllib.error import HTTPError

from _pytest.monkeypatch import MonkeyPatch

from goprocam import GoProCamera

try:
    import getmac
except ImportError:
    pass


class GoProCameraTest(TestCase):
    def setUp(self):
        self.monkeypatch = MonkeyPatch()

        self.monkeypatch.setattr(
            time, "sleep",
            lambda x: logging.debug("sleeping for {}s".format(x))
            )

        # Default response to pretend I'm a GoPro HERO+
        self.responses = {
            "/gp/gpControl": {
                "info": {
                    "firmware_version": "HD3.02",
                    "model_name": "dummy",
                    "model_number": 1,
                    "serial_number": "X",
                    "board_type": "0x02",
                    "ap_mac": "ABCDEFABCDEF",
                    "ap_ssid": "ssid",
                    "ap_has_default_credentials": "1",
                    "git_sha1": "66fac36c7d9b3e3479c460fc827e8436c5634a60",
                }
            }
        }

        def fake_request(url, timeout=None):
            path = url.replace("http://10.5.5.9", "")
            try:
                if isinstance(self.responses[path], Exception):
                    raise self.responses[path]
                if isinstance(self.responses[path], str):
                    res = io.BytesIO(self.responses[path].encode("utf8"))
                elif isinstance(self.responses[path], bytes):
                    res = io.BytesIO(self.responses[path])
                else:
                    res = io.BytesIO(json.dumps(
                            self.responses[path]).encode("utf8"))
                # v. ropey. We want to pretend our result is a HTTP response,
                # a little.

                class Info(object):
                    def get_content_charset(self, charset):
                        return "utf8"

                res.info = Info
                return res
            except KeyError:
                raise HTTPError(url, 404, "Not Found ({})".format(url), None,
                                None)

        self.monkeypatch.setattr(urllib.request, "urlopen", fake_request)

        # if this optional module is available, stub it out
        def fakemac(ip=""):
            return "DE:AD:BE:EF"

        if sys.modules.get("getmac"):
            self.monkeypatch.setattr(getmac, "get_mac_address", fakemac)

        # stop it from sending the WoL packet during __init__
        self.monkeypatch.setattr(
            GoProCamera.GoPro, "power_on", lambda s, mac_address: s
        )

        # and disable this as we'll test it separately
        self.goprocam = GoProCamera.GoPro(
            camera="gpcontrol", mac_address=fakemac(ip=None)
        )
