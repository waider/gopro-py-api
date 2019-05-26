from socket import timeout

import pytest

from .conftest import GoProCameraTest


class PrepareGpControlTest(GoProCameraTest):
    def test_prepare_gpcontrol_success(self):
        with self.monkeypatch.context() as m:
            def verify_print(args):
                assert args == 'Camera successfully connected!'
            m.setattr('builtins.print', verify_print)
            self.goprocam.prepare_gpcontrol()

    def test_prepare_gpcontrol_failed(self):
        del(self.responses['/gp/gpControl'])
        # this basically goes into infinite recursion if it fails
        with pytest.raises(RecursionError):
            self.goprocam.prepare_gpcontrol()

    def test_prepare_gpcontrol_timeout(self):
        self.responses['/gp/gpControl'] = timeout()
        with pytest.raises(RecursionError):
            self.goprocam.prepare_gpcontrol()

    def test_prepare_gpcontrol_hx(self):
        with self.monkeypatch.context() as m:
            def verify_print(args):
                assert args == 'Camera successfully connected!'
            m.setattr('builtins.print', verify_print)
            self.responses['/gp/gpControl']['info']['firmware_version'] = 'HX'
            # HX needs an extra URL
            # '31' >= 1 means we're ready
            self.responses['/gp/gpControl/status'] = [
                {'status': {'31': 0}},
                {'status': {'31': 1}}
            ]
            self.goprocam.prepare_gpcontrol()
