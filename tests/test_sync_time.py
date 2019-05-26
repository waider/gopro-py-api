from .conftest import GoProCameraTest, GoProCameraAuthTest
from goprocam import GoProCamera
import datetime


class MyDateTime(datetime.datetime):
    @classmethod
    def now(cls):
        return datetime.datetime(2019, 5, 1, 12, 45, 32)


class SyncTimeTest(GoProCameraTest):
    def test_sync_time(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, cmd):
                # (20)19 -> 0x13
                # 5 -> 0x5
                # 1 -> 0x1
                # 12 -> 0xc
                # 45 -> 0x2d
                # 32 -> 0x20
                assert cmd == 'setup/date_time?p=%13%5%1%c%2d%20'

            m.setattr(GoProCamera.GoPro, 'gpControlCommand', verify_cmd)
            m.setattr(datetime, 'datetime', MyDateTime)
            self.goprocam.syncTime()


class SyncTimeAuthTest(GoProCameraAuthTest):
    def test_sync_time(self):
        with self.monkeypatch.context() as m:
            def verify_cmd(self, cmd, param):
                assert cmd == 'TM'
                assert param == '%13%5%1%c%2d%20'  # see above

            m.setattr(GoProCamera.GoPro, 'sendCamera', verify_cmd)
            m.setattr(datetime, 'datetime', MyDateTime)
            self.goprocam.syncTime()
