from .conftest import GoProCameraTest
from goprocam import GoProCamera


class clipStatusTest(GoProCameraTest):
    def test_clipStatus(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, text):
                assert text == 'transcode/status?id=foo'
                return '{"status": {"status": 0}}'
            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            # todo: only tests status == 0; can also test up to 4
            assert self.goprocam.clipStatus(status='foo') == 'started'
