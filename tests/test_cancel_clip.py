from .conftest import GoProCameraTest
from goprocam import GoProCamera


class CancelClipTest(GoProCameraTest):
    def test_cancelClip(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, text):
                assert text == 'transcode/cancel?id=foo'
            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.cancelClip(video_id='foo')
