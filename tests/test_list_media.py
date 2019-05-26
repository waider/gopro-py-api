from .conftest import GoProCameraTest
from goprocam import GoProCamera
from socket import timeout


class ListMediaTest(GoProCameraTest):
    def test_list_media(self):
        assert self.goprocam.listMedia() == '{\n  "media": []\n}'

    def test_list_media_fs(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            self.responses[':8080/gp/gpMediaListEx'] = {'foo': 'bar'}
            assert self.goprocam.listMedia() == '{\n  "foo": "bar"\n}'

    def test_list_media_fs_format_empty(self):
        with self.monkeypatch.context() as m:
            def print_verify(arg):
                assert False, "shouldn't be here"
            m.setattr('builtins.print', print_verify)
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            self.responses[':8080/gp/gpMediaListEx'] = {}
            assert self.goprocam.listMedia(format=True) is None

    def test_list_media_format_empty(self):
        with self.monkeypatch.context() as m:
            def print_verify(arg):
                assert False, "shouldn't be here"
            m.setattr('builtins.print', print_verify)
            assert self.goprocam.listMedia(format=True) is None

    def test_list_media_fs_format_files(self):
        with self.monkeypatch.context() as m:
            def print_verify(arg):
                assert arg == 'file'
            m.setattr('builtins.print', print_verify)
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            self.responses[':8080/gp/gpMediaListEx'] = [[{
                'media': [{'fs': [{'n': 'file'}]}]
            }]]
            assert self.goprocam.listMedia(format=True) is None

    def test_list_media_format_files(self):
        with self.monkeypatch.context() as m:
            def print_verify(arg):
                assert arg == 'file'
            m.setattr('builtins.print', print_verify)
            self.responses[':8080/gp/gpMediaList'] = {'media': [{
                'fs': [{'n': 'file'}]
            }]}
            assert self.goprocam.listMedia(format=True) is None

    def test_list_media_format_array_empty(self):
        assert self.goprocam.listMedia(format=True, media_array=True) == []

    def test_list_media_format_array_files(self):
        self.responses[':8080/gp/gpMediaList'] = {'media': [{
            'd': 'folder',
            'fs': [{'n': 'file', 's': '1', 'mod': '2'}]
        }]}
        assert self.goprocam.listMedia(format=True, media_array=True) ==\
            [['folder', 'file', '1', '2']]

    def test_list_media_fs_format_array_empty(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            self.responses[':8080/gp/gpMediaListEx'] = {}
            assert self.goprocam.listMedia(format=True, media_array=True) == []

    def test_list_media_fs_format_array_files(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            self.responses[':8080/gp/gpMediaListEx'] = [[{'media': [{
                'd': 'folder',
                'fs': [{'n': 'file', 's': '1', 'mod': '2'}]}]
            }]]
            assert self.goprocam.listMedia(format=True, media_array=True) ==\
                [['folder', 'file', '1', '2']]

    def test_list_media_timeout(self):
        self.responses[':8080/gp/gpMediaList'] = timeout()
        assert self.goprocam.listMedia() == ''

    def test_list_media_error(self):
        del self.responses[':8080/gp/gpMediaList']
        assert self.goprocam.listMedia('') == ''
