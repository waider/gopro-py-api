from .conftest import GoProCameraTest, GoProCameraAuthTest
from goprocam import GoProCamera
import pytest
import sys


class ModuleTest(GoProCameraTest):
    def test_init(self):
        assert self.goprocam, "got a self.goprocam object"
        assert self.goprocam.ip_addr == '10.5.5.9'
        assert self.goprocam._mac_address == '00:00:DE:AD:BE:EF'
        assert self.goprocam._camera == 'gpcontrol'

    def test_init_pair(self):
        def fakepair(self):
            self.paired = True
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'pair', fakepair)
            self.goprocam = GoProCamera.GoPro(camera='startpair')
        assert self.goprocam.paired

    def test_init_detect(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'prepare_gpcontrol',
                      lambda self: None)
            self.goprocam = GoProCamera.GoPro(camera='detect')
        assert self.goprocam._camera == 'gpcontrol'

    def test_str(self):
        # avoid testing infoCamera by side-effect
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda self: 'stringy')
            assert str(self.goprocam) == 'stringy'

    # this is deeply silly, but I'm trying to cover the whole module...
    def test_getmac(self):
        with self.monkeypatch.context() as m:
            def mac_verify(*args, **kwargs):
                assert kwargs['ip'] == '10.5.5.9'
                return 'XX'
            if 'getmac' in sys.modules:
                m.setattr('getmac.get_mac_address', mac_verify)
                cleanup = False
            else:
                sys.modules['getmac'] = type(sys)('getmac')
                sys.modules['getmac'].get_mac_address = mac_verify
                cleanup = True
            m.setattr(GoProCamera.GoPro, 'whichCam', lambda x: 'fake')
            cam = GoProCamera.GoPro(camera='detect')
            assert cam._mac_address == 'XX'
            if cleanup:
                del(sys.modules['getmac'])

    def test_init_bad_python(self):
        with self.monkeypatch.context() as m:
            def print_verify(args):
                assert args == 'Needs Python v3, run again on a ' +\
                    'virtualenv or install Python 3'

            class ExitCalled(Exception):
                pass

            def mock_exit():
                raise ExitCalled()

            # setting this to 2 causes sys.exc_clear to be invoked, which
            # doesn't exist in py3
            m.setattr('sys.version_info', [2.9])
            m.setattr('builtins.print', print_verify)
            m.setattr('builtins.exit', mock_exit)

            with pytest.raises(ExitCalled):
                GoProCamera.GoPro()


class ModuleAuthTest(GoProCameraAuthTest):
    def test_init_auth(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'power_on_auth', lambda self: None)
            assert self.goprocam._camera == 'auth'
