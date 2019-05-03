import urllib.request
import io

from .conftest import GoProCameraTest
from goprocam import GoProCamera

from socket import timeout


class SendBacPacTest(GoProCameraTest):
    def test_send_bacpac_default(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getPassword',
                      lambda self: 'password')

            # this returns nothing so we need to be a bit more clever
            # to verify it
            def fake_urlopen(url, *args, **kwargs):
                assert url == 'http://10.5.5.9/bacpac/foo?t=password&p=%FF'
                return io.BytesIO('{}'.encode('utf8'))
            m.setattr(urllib.request, 'urlopen', fake_urlopen)
            self.goprocam.sendBacpac('foo', 'FF')

    def test_send_bacpac_value_empty(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getPassword',
                      lambda self: 'password')

            # this returns nothing so we need to be a bit more clever
            # to verify it
            def fake_urlopen(url, *args, **kwargs):
                assert url == 'http://10.5.5.9/bacpac/foo?t=password'
                return io.BytesIO('{}'.encode('utf8'))
            m.setattr(urllib.request, 'urlopen', fake_urlopen)
            self.goprocam.sendBacpac('foo', '')

    def test_send_bacpac_error(self):
        # just for coverage, really. can't test as it stands.
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getPassword',
                      lambda self: 'password')
            self.goprocam.sendBacpac('foo', 'bar')

    def test_send_bacpac_timeout(self):
        # same
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getPassword',
                      lambda self: 'password')
            self.responses['/bacpac/foo?t=password&p=%FF'] = timeout()
            self.goprocam.sendBacpac('foo', 'FF')
