from .conftest import GoProCameraTest
from goprocam import GoProCamera
import pytest


class PrepareGpControlTest(GoProCameraTest):
    def test_prepare_gpcontrol_success(self):
        with self.monkeypatch.context() as m:
            def verify_print(args):
                assert args == 'Camera successfully connected!'
            m.setattr('builtins.print', verify_print)
            self.goprocam.prepare_gpcontrol()

    def test_prepare_gpcontrol_empty_firmware(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, f: '')
            # this basically goes into infinite recursion if it fails
            with pytest.raises(RecursionError):
                self.goprocam.prepare_gpcontrol()

    def test_prepare_gpcontrol_hx(self):
        with self.monkeypatch.context() as m:
            def verify_print(args):
                assert args == 'Camera successfully connected!'
            m.setattr('builtins.print', verify_print)
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, f: 'HX')
            # HX needs an extra URL
            # '31' >= 1 means we're ready
            # This has to go through regular getStatus to access the
            # multiple mock return functionality.
            self.responses['/gp/gpControl/status'] = [
                {'status': {'31': 0}},
                {'status': {'31': 1}}
            ]
            self.goprocam.prepare_gpcontrol()

    def test_prepare_gpcontrol_empty_status(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, f: 'HX')
            m.setattr(GoProCamera.GoPro, 'getStatus', lambda s, a, b: '')
            # this basically goes into infinite recursion if it fails
            with pytest.raises(RecursionError):
                self.goprocam.prepare_gpcontrol()
