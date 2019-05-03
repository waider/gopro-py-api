import urllib.request
import io

from .conftest import GoProCameraTest
from goprocam import GoProCamera

from socket import timeout


class GpControlExecuteTest(GoProCameraTest):
    def test_send_camera_default(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getPassword',
                      lambda self: 'password')

            # this returns nothing so we need to be a bit more clever
            # to verify it
            def fake_urlopen(url, *args, **kwargs):
                assert url == 'http://10.5.5.9/camera/foo?t=password'
                return io.BytesIO('{}'.encode('utf8'))
            m.setattr(urllib.request, 'urlopen', fake_urlopen)
            self.goprocam.sendCamera('foo')

    def test_send_camera_with_value(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getPassword',
                      lambda self: 'password')

            def fake_urlopen(url, *args, **kwargs):
                assert url == 'http://10.5.5.9/camera/foo?t=password&p=bar'
                return io.BytesIO('{}'.encode('utf8'))
            m.setattr(urllib.request, 'urlopen', fake_urlopen)
            self.goprocam.sendCamera('foo', 'bar')

    def test_send_camera_with_hex_value(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getPassword',
                      lambda self: 'password')

            def fake_urlopen(url, *args, **kwargs):
                assert url == 'http://10.5.5.9/camera/foo?t=password&p=%FF'
                return io.BytesIO('{}'.encode('utf8'))
            m.setattr(urllib.request, 'urlopen', fake_urlopen)
            self.goprocam.sendCamera('foo', 'FF')

    def test_send_camera_error(self):
        # just for coverage, really. can't test as it stands.
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getPassword',
                      lambda self: 'password')
            self.goprocam.sendCamera('foo', 'bar')

    def test_send_camera_timeout(self):
        # same
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getPassword',
                      lambda self: 'password')
            self.responses['/camera/foo?t=password&p=bar'] = timeout()
            self.goprocam.sendCamera('foo', 'bar')
