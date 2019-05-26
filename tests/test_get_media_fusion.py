from .conftest import GoProCameraTest
from socket import timeout


class GetMediaFusionTest(GoProCameraTest):
    def test_get_media_empty(self):
        self.responses[':8080/gp/gpMediaListEx'] = [[
            {'media': []},
            {'media': []}
        ]]
        # again, should raise or return None
        assert self.goprocam.getMediaFusion() == [
            'http://10.5.5.9:8080/videos/DCIM//',
            'http://10.5.5.9:8080/videos2/DCIM//'
        ]

    def test_get_media_empty_folder1_back_front(self):
        self.responses[':8080/gp/gpMediaListEx'] = [[
            {'media': [
                {'d': 'folderGBACK', 'fs': []}
            ]},
            {'media': []}
        ]]
        assert self.goprocam.getMediaFusion() == [
            'http://10.5.5.9:8080/videos/DCIM/folderGBACK/',
            'http://10.5.5.9:8080/videos2/DCIM/folderGFRNT/'
        ]

    def test_get_media_empty_folder1_front_back(self):
        self.responses[':8080/gp/gpMediaListEx'] = [[
            {'media': [
                {'d': 'folderGFRNT', 'fs': []}
            ]},
            {'media': []}
        ]]
        assert self.goprocam.getMediaFusion() == [
            'http://10.5.5.9:8080/videos/DCIM/folderGFRNT/',
            'http://10.5.5.9:8080/videos2/DCIM/folderGBACK/'
        ]

    def test_get_media_folder1_empty_folder2(self):
        self.responses[':8080/gp/gpMediaListEx'] = [[
            {'media': [
                {'d': 'folderGBACK', 'fs': [{'n': 'file'}]}
            ]},
            {'media': []}
        ]]
        assert self.goprocam.getMediaFusion() == [
            'http://10.5.5.9:8080/videos/DCIM/folderGBACK/file',
            'http://10.5.5.9:8080/videos2/DCIM/folderGFRNT/'
        ]

    def test_get_media_folder2_empty_folder1(self):
        self.responses[':8080/gp/gpMediaListEx'] = [[
            {'media': [
                {'d': 'folderGBACK', 'fs': []}
            ]},
            {'media': [
                {'d': 'folderGFRNT', 'fs': [{'n': 'file'}]}
            ]}
        ]]
        assert self.goprocam.getMediaFusion() == [
            'http://10.5.5.9:8080/videos/DCIM/folderGBACK/',
            'http://10.5.5.9:8080/videos2/DCIM/folderGFRNT/file'
        ]

    # contrived. I don't think this could happen but the code caters for it.
    def test_get_media_no_empty_folders(self):
        self.responses[':8080/gp/gpMediaListEx'] = [[
            {'media': [
                {'d': 'folderGBACK', 'fs': [{'n': 'file1'}]},
                {'d': 'folderGFRNT', 'fs': [{'n': 'file3'}]}
            ]},
            {'media': [
                {'d': 'folderGFRNT', 'fs': [{'n': 'file2'}]},
                {'d': 'folderGBACK', 'fs': [{'n': 'file4'}]}
            ]}
        ]]
        assert self.goprocam.getMediaFusion() == [
            'http://10.5.5.9:8080/videos/DCIM/folderGFRNT/file3',
            'http://10.5.5.9:8080/videos2/DCIM/folderGBACK/file4',
        ]

    def test_get_media_timeout(self):
        self.responses[':8080/gp/gpMediaListEx'] = timeout()
        assert self.goprocam.getMediaFusion() == ''

    def test_get_media_fusion_httperror(self):
        assert self.goprocam.getMediaFusion() == ''
