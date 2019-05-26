from .conftest import GoProCameraTest
from goprocam import GoProCamera


class GetClipTest(GoProCameraTest):
    def test_get_clip(self):
        self.responses['/gp/gpControl/command/transcode/video_to_video?' +
                       'source=DCIM/file&res=resolution&fps_divisor=' +
                       'frame_rate&in_ms=start_ms&out_ms=stop_ms'] = {
                           'status': {'id': 'clip_id'}
                       }
        assert self.goprocam.getClip(file='file', resolution='resolution',
                                     frame_rate='frame_rate',
                                     start_ms='start_ms',
                                     stop_ms='stop_ms') == 'clip_id'

    def test_get_clip_hero4(self):
        with self.monkeypatch.context() as m:
            self.responses['/gp/gpControl/command/transcode/request?' +
                           'source=DCIM/file&res=resolution&fps_divisor=' +
                           'frame_rate&in_ms=start_ms&out_ms=stop_ms'] = {
                               'status': {'id': 'clip_id'}
                           }
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, t: 'HERO4')
            assert self.goprocam.getClip(file='file', resolution='resolution',
                                         frame_rate='frame_rate',
                                         start_ms='start_ms',
                                         stop_ms='stop_ms') == 'clip_id'
