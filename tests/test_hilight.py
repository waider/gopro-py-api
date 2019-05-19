from .conftest import GoProCameraTest, GoProCameraAuthTest
from goprocam import GoProCamera


class HilightTest(GoProCameraTest):
    def test_hilight(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, text):
                assert text == 'storage/tag_moment'
            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.hilight()


class HilightAuthTest(GoProCameraAuthTest):
    def test_hilight(self):
        with self.monkeypatch.context() as m:
            def verify_print(*args, **kwargs):
                assert args == ('Not supported.',)
            m.setattr('builtins.print', verify_print)
            self.goprocam.hilight()
