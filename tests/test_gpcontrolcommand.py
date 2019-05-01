from .conftest import GoProCameraTest

from socket import timeout


class GpControlCommandTest(GoProCameraTest):
    def test_gp_control_command(self):
        self.responses['/gp/gpControl/command/foo'] = '{}'
        assert '{}' == self.goprocam.gpControlCommand('foo')

    def test_gp_control_command_error(self):
        assert '' == self.goprocam.gpControlCommand('foo')

    def test_gp_control_command_timeout(self):
        self.responses['/gp/gpControl/command/foo'] = timeout()
        assert '' == self.goprocam.gpControlCommand('foo')
