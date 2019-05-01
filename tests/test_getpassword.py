from socket import timeout

from .conftest import GoProCameraTest


class GetPasswordTest(GoProCameraTest):
    def test_get_password(self):
        self.responses['/bacpac/sd'] = 'password0'
        assert self.goprocam.getPassword() == 'password0'

    def test_get_password_error(self):
        assert self.goprocam.getPassword() == ''

    def test_get_password_timeout(self):
        self.responses['/bacpac/sd'] = timeout()
        assert self.goprocam.getPassword() == ''
