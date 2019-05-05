from .conftest import GoProCameraTest, GoProCameraAuthTest
from goprocam import GoProCamera


class DeleteTest(GoProCameraTest):
    def test_delete_last(self):
        with self.monkeypatch.context() as m:

            def verify_cmd(self, text):
                assert text == 'storage/delete/last'
            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.delete('last')

    def test_delete_all(self):
        with self.monkeypatch.context() as m:

            def verify_cmd(self, text):
                assert text == 'storage/delete/all'
            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.delete('all')

    def test_delete_some(self):
        with self.monkeypatch.context() as m:

            def verify_cmd(self, text):
                self.counter = self.counter + 1
                assert text == 'storage/delete/last'

            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            self.goprocam.counter = 0
            self.goprocam.delete(2)

            assert self.goprocam.counter == 2


class DeleteAuthTest(GoProCameraAuthTest):
    def test_delete_last(self):
        with self.monkeypatch.context() as m:

            def verify_cmd(self, text):
                assert text == 'DL'
            m.setattr(GoProCamera.GoPro, 'sendCamera', verify_cmd)
            self.goprocam.delete('last')

    def test_delete_all(self):
        with self.monkeypatch.context() as m:

            def verify_cmd(self, text):
                assert text == 'DA'
            m.setattr(GoProCamera.GoPro, 'sendCamera', verify_cmd)
            self.goprocam.delete('all')

    def test_delete_some(self):
        with self.monkeypatch.context() as m:

            def verify_cmd(self, text):
                self.counter = self.counter + 1
                assert text == 'DL'

            m.setattr(GoProCamera.GoPro, 'sendCamera', verify_cmd)
            self.goprocam.counter = 0
            self.goprocam.delete(2)

            assert self.goprocam.counter == 2
