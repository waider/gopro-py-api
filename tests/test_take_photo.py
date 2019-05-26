from .conftest import GoProCameraTest, GoProCameraAuthTest,\
    GoProCameraUnknownTest
from goprocam import GoProCamera, constants


class TakePhotoUnknownTest(GoProCameraUnknownTest):
    def test_take_photo(self):
        with self.monkeypatch.context() as m:
            def verify_shutter(self, cmd):
                assert cmd == constants.start

            def fake_busy(self, p1, p2):
                """ look busy first time we're called, then not """
                if self.is_busy == 1:
                    self.is_busy = 0
                    return 1
                return 0

            def verify_mode(self, mode, submode=None):
                assert mode == constants.Mode.PhotoMode

            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, p: 'HERO1')
            m.setattr(GoProCamera.GoPro, 'mode', verify_mode)
            m.setattr(GoProCamera.GoPro, 'shutter', verify_shutter)
            m.setattr(GoProCamera.GoPro, 'getStatus', fake_busy)
            m.setattr(GoProCamera.GoPro, 'getMedia', lambda s: 'PIC')

            self.goprocam.is_busy = 1

            assert self.goprocam.take_photo() is None


class TakePhotoTest(GoProCameraTest):
    def test_take_photo(self):
        with self.monkeypatch.context() as m:
            def verify_shutter(self, cmd):
                assert cmd == constants.start

            def fake_busy(self, p1, p2):
                """ look busy first time we're called, then not """
                if self.is_busy == 1:
                    self.is_busy = 0
                    return 1
                return 0

            def verify_mode(self, mode, submode=None):
                assert mode == constants.Mode.PhotoMode

            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, p: 'HERO1')
            m.setattr(GoProCamera.GoPro, 'mode', verify_mode)
            m.setattr(GoProCamera.GoPro, 'shutter', verify_shutter)
            m.setattr(GoProCamera.GoPro, 'getStatus', fake_busy)
            m.setattr(GoProCamera.GoPro, 'getMedia', lambda s: 'PIC')

            self.goprocam.is_busy = 1

            assert self.goprocam.take_photo() == 'PIC'

    def test_take_photo_with_timer(self):
        with self.monkeypatch.context() as m:
            def verify_shutter(self, cmd):
                assert cmd == constants.start

            def fake_busy(self, p1, p2):
                """ look busy first time we're called, then not """
                if self.is_busy == 1:
                    self.is_busy = 0
                    return 1
                return 0

            def verify_mode(self, mode, submode=None):
                assert mode == constants.Mode.PhotoMode

            def verify_sleep(sleeptime):
                assert sleeptime == 2

            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, p: 'HERO1')
            m.setattr(GoProCamera.GoPro, 'mode', verify_mode)
            m.setattr(GoProCamera.GoPro, 'shutter', verify_shutter)
            m.setattr(GoProCamera.GoPro, 'getStatus', fake_busy)
            m.setattr(GoProCamera.GoPro, 'getMedia', lambda s: 'PIC1')
            m.setattr('time.sleep', verify_sleep)

            self.goprocam.is_busy = 1

            assert self.goprocam.take_photo(timer=2) == 'PIC1'

    def test_take_photo_hero5_black(self):
        with self.monkeypatch.context() as m:
            def verify_shutter(self, cmd):
                assert cmd == constants.start

            def fake_busy(self, p1, p2):
                """ look busy first time we're called, then not """
                if self.is_busy == 1:
                    self.is_busy = 0
                    return 1
                return 0

            def verify_mode(self, mode, submode=None):
                assert mode == constants.Mode.PhotoMode
                assert submode == constants.Mode.SubMode.Photo.Single_H5

            m.setattr(GoProCamera.GoPro, 'infoCamera',
                      lambda s, p: 'HERO5 Black')
            m.setattr(GoProCamera.GoPro, 'mode', verify_mode)
            m.setattr(GoProCamera.GoPro, 'shutter', verify_shutter)
            m.setattr(GoProCamera.GoPro, 'getStatus', fake_busy)
            m.setattr(GoProCamera.GoPro, 'getMedia', lambda s: 'PIC1')

            self.goprocam.is_busy = 1

            assert self.goprocam.take_photo() == 'PIC1'

    def test_take_photo_hero6(self):
        with self.monkeypatch.context() as m:
            def verify_shutter(self, cmd):
                assert cmd == constants.start

            def fake_busy(self, p1, p2):
                """ look busy first time we're called, then not """
                if self.is_busy == 1:
                    self.is_busy = 0
                    return 1
                return 0

            def verify_mode(self, mode, submode=None):
                assert mode == constants.Mode.PhotoMode
                assert submode == constants.Mode.SubMode.Photo.Single_H5

            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, p: 'HERO6')
            m.setattr(GoProCamera.GoPro, 'mode', verify_mode)
            m.setattr(GoProCamera.GoPro, 'shutter', verify_shutter)
            m.setattr(GoProCamera.GoPro, 'getStatus', fake_busy)
            m.setattr(GoProCamera.GoPro, 'getMedia', lambda s: 'PIC1')

            self.goprocam.is_busy = 1

            assert self.goprocam.take_photo() == 'PIC1'


class TakePhotoAuthTest(GoProCameraAuthTest):
    def test_take_photo(self):
        with self.monkeypatch.context() as m:
            def verify_shutter(self, cmd):
                assert cmd == constants.start

            def fake_busy(self, p1):
                """ look busy first time we're called, then not """
                if self.is_busy == 1:
                    self.is_busy = 0
                    return '01'
                return '00'

            def verify_mode(self, mode, submode=None):
                assert mode == constants.Mode.PhotoMode

            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, p: 'HERO1')
            m.setattr(GoProCamera.GoPro, 'mode', verify_mode)
            m.setattr(GoProCamera.GoPro, 'shutter', verify_shutter)
            m.setattr(GoProCamera.GoPro, 'getStatus', fake_busy)
            m.setattr(GoProCamera.GoPro, 'getMedia', lambda s: 'PIC')

            self.goprocam.is_busy = 1

            assert self.goprocam.take_photo() == 'PIC'
