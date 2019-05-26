from .conftest import GoProCameraTest, GoProCameraAuthTest,\
    GoProCameraUnknownTest, verify_uncalled
from goprocam import GoProCamera


class StreamUnknownTest(GoProCameraUnknownTest):
    def test_stream(self):
        with self.monkeypatch.context() as m:
            def livestream_verify(self, arg):
                assert arg == 'start'
            m.setattr(GoProCamera.GoPro, 'livestream', livestream_verify)
            m.setattr('subprocess.Popen', verify_uncalled)
            self.goprocam.stream(addr='addr')


class StreamTest(GoProCameraTest):
    def popen_verify(*args, **kwargs):
        # args[0] is our class instance, with testMethod set to the test name
        assert args[1] == 'ffmpeg -f mpegts -i udp://10.5.5.9:8554 -b 800k ' +\
            '-r 30 -f mpegts addr'
        assert kwargs['shell'] is True

    def test_stream(self):
        with self.monkeypatch.context() as m:
            def livestream_verify(self, arg):
                assert arg == 'start'
            m.setattr(GoProCamera.GoPro, 'livestream', livestream_verify)
            m.setattr(GoProCamera.GoPro, 'KeepAlive', lambda self: None)
            m.setattr('subprocess.Popen', self.popen_verify)
            self.goprocam.stream(addr='addr')

    def test_stream_quality_low(self):
        with self.monkeypatch.context() as m:
            def livestream_verify(self, arg):
                assert arg == 'start'

            def streamSettings_verify(self, arg1, arg2):
                assert arg1 == '250000'
                assert arg2 == '0'
            m.setattr(GoProCamera.GoPro, 'streamSettings',
                      streamSettings_verify)
            m.setattr(GoProCamera.GoPro, 'livestream', livestream_verify)
            m.setattr(GoProCamera.GoPro, 'KeepAlive', lambda self: None)
            m.setattr('subprocess.Popen', self.popen_verify)
            self.goprocam.stream(addr='addr', quality='low')

    def test_stream_quality_medium(self):
        with self.monkeypatch.context() as m:
            def livestream_verify(self, arg):
                assert arg == 'start'

            def streamSettings_verify(self, arg1, arg2):
                assert arg1 == '1000000'
                assert arg2 == '4'
            m.setattr(GoProCamera.GoPro, 'streamSettings',
                      streamSettings_verify)
            m.setattr(GoProCamera.GoPro, 'livestream', livestream_verify)
            m.setattr(GoProCamera.GoPro, 'KeepAlive', lambda self: None)
            m.setattr('subprocess.Popen', self.popen_verify)
            self.goprocam.stream(addr='addr', quality='medium')

    def test_stream_quality_high(self):
        with self.monkeypatch.context() as m:
            def livestream_verify(self, arg):
                assert arg == 'start'

            def streamSettings_verify(self, arg1, arg2):
                assert arg1 == '4000000'
                assert arg2 == '7'
            m.setattr(GoProCamera.GoPro, 'streamSettings',
                      streamSettings_verify)
            m.setattr(GoProCamera.GoPro, 'livestream', livestream_verify)
            m.setattr(GoProCamera.GoPro, 'KeepAlive', lambda self: None)
            m.setattr('subprocess.Popen', self.popen_verify)
            self.goprocam.stream(addr='addr', quality='high')

    def test_stream_quality_unset_hero4(self):
        with self.monkeypatch.context() as m:
            def livestream_verify(self, arg):
                assert arg == 'start'

            m.setattr(GoProCamera.GoPro, 'streamSettings', verify_uncalled)
            m.setattr(GoProCamera.GoPro, 'livestream', livestream_verify)
            m.setattr(GoProCamera.GoPro, 'KeepAlive', lambda self: None)
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'HERO4')
            m.setattr('subprocess.Popen', self.popen_verify)
            self.goprocam.stream(addr='addr')

    def test_stream_quality_low_hero4(self):
        with self.monkeypatch.context() as m:
            def livestream_verify(self, arg):
                assert arg == 'start'

            def streamSettings_verify(self, arg1, arg2):
                assert arg1 == '250000'
                assert arg2 == '0'
            m.setattr(GoProCamera.GoPro, 'streamSettings',
                      streamSettings_verify)
            m.setattr(GoProCamera.GoPro, 'livestream', livestream_verify)
            m.setattr(GoProCamera.GoPro, 'KeepAlive', lambda self: None)
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'HERO4')
            m.setattr('subprocess.Popen', self.popen_verify)
            self.goprocam.stream(addr='addr', quality='low')

    def test_stream_quality_medium_hero4(self):
        with self.monkeypatch.context() as m:
            def livestream_verify(self, arg):
                assert arg == 'start'

            def streamSettings_verify(self, arg1, arg2):
                assert arg1 == '1000000'
                assert arg2 == '4'
            m.setattr(GoProCamera.GoPro, 'streamSettings',
                      streamSettings_verify)
            m.setattr(GoProCamera.GoPro, 'livestream', livestream_verify)
            m.setattr(GoProCamera.GoPro, 'KeepAlive', lambda self: None)
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'HERO4')
            m.setattr('subprocess.Popen', self.popen_verify)
            self.goprocam.stream(addr='addr', quality='medium')

    def test_stream_quality_high_hero4(self):
        with self.monkeypatch.context() as m:
            def livestream_verify(self, arg):
                assert arg == 'start'

            def streamSettings_verify(self, arg1, arg2):
                assert arg1 == '2400000'
                assert arg2 == '6'
            m.setattr(GoProCamera.GoPro, 'streamSettings',
                      streamSettings_verify)
            m.setattr(GoProCamera.GoPro, 'livestream', livestream_verify)
            m.setattr(GoProCamera.GoPro, 'KeepAlive', lambda self: None)
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'HERO4')
            m.setattr('subprocess.Popen', self.popen_verify)
            self.goprocam.stream(addr='addr', quality='high')


class StreamAuthTest(GoProCameraAuthTest):
    def popen_verify(*args, **kwargs):
        assert args[1] == \
            'ffmpeg -i http://10.5.5.9:8080/live/amba.m3u8 -f mpegts addr'
        assert kwargs['shell'] is True

    def test_stream(self):
        with self.monkeypatch.context() as m:
            def livestream_verify(self, arg):
                assert arg == 'start'
            m.setattr(GoProCamera.GoPro, 'livestream', livestream_verify)
            m.setattr('subprocess.Popen', self.popen_verify)
            self.goprocam.stream(addr='addr')
