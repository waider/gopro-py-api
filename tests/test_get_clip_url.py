from .conftest import GoProCameraTest


class GetClipURLTest(GoProCameraTest):
    def test_get_clip_url(self):
        self.responses['/gp/gpControl/command/transcode/status?id=clip_id'] = {
            'status': {'status': 0}}
        assert self.goprocam.getClipURL(status="clip_id") is None

    def test_get_clip_url_success(self):
        self.responses['/gp/gpControl/command/transcode/status?id=clip_id'] = {
            'status': {'status': 2, 'output': 'foo'}}
        assert self.goprocam.getClipURL(status="clip_id") ==\
            'http://10.5.5.9:80/videos/foo'
