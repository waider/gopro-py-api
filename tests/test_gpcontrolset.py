from .conftest import GoProCameraTest

from socket import timeout

class GpControlSetTest(GoProCameraTest):
    def test_gp_control_set(self):
        # on success, this is an empty json blob
        # on failure, the blob includes an 'error_code'
        self.responses['/gp/gpControl/setting/foo/bar'] = '{}'
        assert '{}' == self.goprocam.gpControlSet('foo', 'bar')

    def test_gp_control_set_error(self):
        assert '' == self.goprocam.gpControlSet('foo', 'bar')

    def test_gp_control_set_timeout(self):
        self.responses['/gp/gpControl/setting/foo/bar'] = timeout()
        assert '' == self.goprocam.gpControlSet('foo', 'bar')
