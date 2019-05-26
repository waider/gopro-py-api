from .conftest import GoProCameraTest
from goprocam import GoProCamera
import pytest
from socket import timeout


class GetMediaInfoTest(GoProCameraTest):
    def test_get_media_info_empty_no_option(self):
        assert self.goprocam.getMediaInfo(option="") is None

    def test_get_media_info_FS_no_option(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            self.responses[':8080/gp/gpMediaListEx'] = [[
                {'media': []},
                {'media': []}
            ]]
            # should really error out
            assert self.goprocam.getMediaInfo(option="") is None

    def test_get_media_info_FS_folder_back_front(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            self.responses[':8080/gp/gpMediaListEx'] = [[
                {'media': [
                    {'d': 'folderGBACK', 'fs': []}
                ]},
                {'media': []}
            ]]
            assert self.goprocam.getMediaInfo('folder') == [
                'folderGBACK', 'folderGFRNT'
            ]

    def test_get_media_info_FS_folder_front_back(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            self.responses[':8080/gp/gpMediaListEx'] = [[
                {'media': [
                    {'d': 'folderGFRNT', 'fs': []}
                ]},
                {'media': []}
            ]]
            assert self.goprocam.getMediaInfo('folder') == [
                'folderGFRNT', 'folderGBACK'
            ]

    def test_get_media_info_FS_file_empty_back_front(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            self.responses[':8080/gp/gpMediaListEx'] = [[
                {'media': [
                    {'d': 'folderGBACK', 'fs': []}
                ]},
                {'media': []}
            ]]
            assert self.goprocam.getMediaInfo('file') == [
                '', ''
            ]

    def test_get_media_info_FS_file_back_front(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            self.responses[':8080/gp/gpMediaListEx'] = [[
                {'media': [
                    {'d': 'folderGBACK', 'fs': [
                        {'n': 'file1', 's': '3'}
                    ]}
                ]},
                {'media': [
                    {'d': 'folderGFRNT', 'fs': [
                        {'n': 'file2', 's': '4'}
                    ]}
                ]}
            ]]
            assert self.goprocam.getMediaInfo('file') == [
                'file1', 'file2'
            ]

    # this is for coverage and the results seem questionable
    def test_get_media_info_FS_multiple_files_back_front(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            self.responses[':8080/gp/gpMediaListEx'] = [[
                {'media': [
                    {'d': 'folderGBACK', 'fs': [
                        {'n': 'file1', 's': '3'}
                    ]},
                    {'d': 'folderGFRNT', 'fs': [
                        {'n': 'file3', 's': '4'}
                    ]}
                ]},
                {'media': [
                    {'d': 'folderGFRNT', 'fs': [
                        {'n': 'file2', 's': '4'}
                    ]},
                    {'d': 'folderGBACK', 'fs': [
                        {'n': 'file4', 's': '3'}
                    ]},
                ]}
            ]]
            assert self.goprocam.getMediaInfo('file') == [
                'file3', 'file4'
            ]

    def test_get_media_info_FS_size_back_front(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'infoCamera', lambda s, x: 'FS')
            self.responses[':8080/gp/gpMediaListEx'] = [[
                {'media': [
                    {'d': 'folderGBACK', 'fs': [
                        {'n': 'file1', 's': '3'}
                    ]}
                ]},
                {'media': [
                    {'d': 'folderGFRNT', 'fs': [
                        {'n': 'file2', 's': '4'}
                    ]}
                ]}
            ]]
            assert self.goprocam.getMediaInfo('size') == [
                '3.0B', '4.0B'
            ]

    def test_get_media_info_folder_empty_folder(self):
        self.responses[':8080/gp/gpMediaList'] = {
            'media': [
                {'d': 'folder', 'fs': []}
            ]}
        assert self.goprocam.getMediaInfo('folder') == 'folder'

    def test_get_media_info_file_empty_folder(self):
        self.responses[':8080/gp/gpMediaList'] = {
            'media': [
                {'d': 'folder', 'fs': []}
            ]}
        assert self.goprocam.getMediaInfo('file') == ''

    def test_get_media_info_size_empty_folder(self):
        self.responses[':8080/gp/gpMediaList'] = {
            'media': [
                {'d': 'folder', 'fs': []}
            ]}
        with pytest.raises(ValueError):  # accidentally...
            assert self.goprocam.getMediaInfo('size') == ''

    def test_get_media_info_file(self):
        self.responses[':8080/gp/gpMediaList'] = {
            'media': [
                {'d': 'folder', 'fs': [{'n': 'file', 's': '1'}]}
            ]}
        assert self.goprocam.getMediaInfo('file') == 'file'

    def test_get_media_info_size(self):
        self.responses[':8080/gp/gpMediaList'] = {
            'media': [
                {'d': 'folder', 'fs': [{'n': 'file', 's': '1'}]}
            ]}
        assert self.goprocam.getMediaInfo('size') == '1.0B'

    def test_get_media_info_timeout(self):
        self.responses[':8080/gp/gpMediaList'] = timeout()
        assert self.goprocam.getMediaInfo('') == ''

    def test_get_media_info_error(self):
        del self.responses[':8080/gp/gpMediaList']
        assert self.goprocam.getMediaInfo('') == ''
