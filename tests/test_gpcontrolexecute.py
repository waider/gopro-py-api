from .conftest import GoProCameraTest

from socket import timeout


class GpControlExecuteTest(GoProCameraTest):
    def test_gp_control_execute(self):
        self.responses['/gp/gpControl/execute?foo'] = '{}'
        assert '{}' == self.goprocam.gpControlExecute('foo')

    def test_gp_control_execute_error(self):
        assert '' == self.goprocam.gpControlExecute('foo')

    def test_gp_control_execute_timeout(self):
        self.responses['/gp/gpControl/execute?foo'] = timeout()
        assert '' == self.goprocam.gpControlExecute('foo')
