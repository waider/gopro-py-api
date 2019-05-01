import socket
import time

import pytest

from .conftest import GoProCameraTest


class KeepaliveTest(GoProCameraTest):
    def test_keepalive(self):
        # this is an infinite loop, so need to be tricksy
        # patch socket functions
        def fake_socket(family, socktype):
            assert family == socket.AF_INET
            assert socktype == socket.SOCK_DGRAM

            class FakeSocket():
                def sendto(self, *args, **kwargs):
                    assert args[0] == "_GPHD_:0:0:2:0.000000\n".encode()
                    ipaddr, port = args[1]
                    assert ipaddr == '10.5.5.9'  # sigh
                    assert port == 8554
            return FakeSocket()

        def fake_sleep(delay):
            assert delay == 2500/1000
            raise socket.timeout()  # to break the loop

        self.monkeypatch.setattr(socket, 'socket', fake_socket)
        self.monkeypatch.setattr(time, 'sleep', fake_sleep)
        with pytest.raises(socket.timeout):
            self.goprocam.KeepAlive()
