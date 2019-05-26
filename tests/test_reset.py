from .conftest import GoProCameraTest
from goprocam import GoProCamera


class ResetTest(GoProCameraTest):
    def test_reset(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, param):
                assert param == 'x/protune/reset'

            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.reset(r='x')
