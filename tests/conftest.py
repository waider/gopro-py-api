import io
import json
import logging
import sys
import time
import urllib.request
import socket
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

        # Default response to pretend I'm a GoPro HERO+ with no media
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
            },
            ':8080/gp/gpMediaList': {
                'media': []
            }
        }

        def fake_request(url, timeout=None, context=None):
            path = url.replace("http://10.5.5.9", "")
            try:
                if isinstance(self.responses[path], list):
                    response = self.responses[path][0]
                    self.responses[path] = self.responses[path][1:]
                else:
                    response = self.responses[path]
                if isinstance(response, Exception):
                    raise response
                if isinstance(response, str):
                    res = io.BytesIO(response.encode("utf8"))
                elif isinstance(response, bytes):
                    res = io.BytesIO(response)
                else:
                    res = io.BytesIO(json.dumps(
                            response).encode("utf8"))
                # v. ropey. We want to pretend our result is a HTTP response,
                # a little.

                class Info(object):
                    def __iter__(self):
                        return iter([])

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
            return "00:00:DE:AD:BE:EF"

        if sys.modules.get("getmac"):
            self.monkeypatch.setattr(getmac, "get_mac_address", fakemac)

        # stop it from sending the WoL packet during __init__
        def fake_socket(family, socktype):
            assert family == socket.AF_INET
            assert socktype == socket.SOCK_DGRAM

            class FakeSocket():
                def sendto(self, *args, **kwargs):
                    assert args[0] in [
                        "_GPHD_:0:0:2:0.000000\n".encode(),  # keepalive
                        b"\xff\xff\xff\xff\xff\xff" +
                        (b"\x00\x00\xde\xad\xbe\xef") * 16,  # wakeup
                        b"\xff\xff\xff\xff\xff\xff" +
                        (b"\xaa\xbb\xcc\xdd\xee\xff") * 16,  # wakeup
                        ], "unexpected message '{}'".format(args[0])
                    ipaddr, port = args[1]
                    assert ipaddr == '10.5.5.9'  # sigh
                    assert port in [
                        8554,  # keepalive
                        9,     # wakeup
                        7      # wakeup
                        ]

            return FakeSocket()

        self.monkeypatch.setattr(socket, 'socket', fake_socket)

        self.goprocam = GoProCamera.GoPro(
            camera="gpcontrol", mac_address=fakemac(ip=None)
        )


class GoProCameraAuthTest(GoProCameraTest):
    def setUp(self):
        super().setUp()
        self.goprocam._camera = 'auth'
        self.responses = {
            '/bacpac/sd': 'password'
            }


class GoProCameraUnknownTest(GoProCameraTest):
    def setUp(self):
        super().setUp()
        self.goprocam._camera = 'unknown'


def mock_mediainfo_txt(self, option):
    if option == 'file':
        return 'file.TXT'
    elif option == 'size':
        return '1.0B'
    elif option == 'folder':
        return 'folder'
    else:
        raise ValueError(option)


def mock_mediainfo_jpg(self, option):
    if option == 'file':
        return 'file.JPG'
    elif option == 'size':
        return '1.0B'
    elif option == 'folder':
        return 'folder'
    else:
        raise ValueError(option)


def mock_mediainfo_txt_fs(self, option):
    if option == 'file':
        return ['front.TXT', 'back.TXT']
    elif option == 'size':
        return ['1.0B', '2.0B']
    elif option == 'folder':
        return ['GFRNT', 'GBACK']
    else:
        raise ValueError(option)


def mock_mediainfo_jpg_fs(self, option):
    if option == 'file':
        return ['front.JPG', 'back.JPG']
    elif option == 'size':
        return ['1.0B', '2.0B']
    elif option == 'folder':
        return ['GFRNT', 'GBACK']
    else:
        raise ValueError(option)


def verify_uncalled(*args, **kwargs):
    assert False, 'unexpected call to function'
