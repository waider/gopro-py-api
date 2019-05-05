from .conftest import GoProCameraTest


class GetInfoFromUrlTest(GoProCameraTest):
    def test_get_info_from_url_simple(self):
        expected = ['folder', 'file']
        url = 'http://' + self.goprocam.ip_addr + \
            ':8080/videos/DCIM/folder/file'
        assert self.goprocam.getInfoFromURL(url) == expected

    def test_get_info_from_url_deeper(self):
        expected = ['100-folder', 'file']
        url = 'http://' + self.goprocam.ip_addr + \
            ':8080/videos/DCIM/100/folder/file'
        assert self.goprocam.getInfoFromURL(url) == expected
