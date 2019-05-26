from .conftest import GoProCameraTest
from goprocam import GoProCamera
import pytest
import json


class GetVideoInfoTest(GoProCameraTest):
    def test_get_video_info(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: x if x == 'folder' else 'file.MP4')
            self.responses[':8080/gp/gpMediaMetadata?p=folder/' +
                           'file.MP4&t=videoinfo'] = 'boo'
            assert self.goprocam.getVideoInfo() == "boo"

    def test_get_video_info_option(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: x if x == 'folder' else 'file.MP4')
            self.responses[':8080/gp/gpMediaMetadata?p=folder/' +
                           'file.MP4&t=videoinfo'] = '{"foo": "boo"}'
            assert self.goprocam.getVideoInfo(option="foo") == "boo"

    def test_get_video_info_option_file(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: x if x == 'folder' else None)
            self.responses[':8080/gp/gpMediaMetadata?p=folder/' +
                           'file.MP4&t=videoinfo'] = '{"foo": "boo"}'
            assert self.goprocam.getVideoInfo(option="foo",
                                              file='file.MP4') == 'boo'

    def test_get_video_info_option_file_folder(self):
        self.responses[':8080/gp/gpMediaMetadata?p=fold/' +
                       'file.MP4&t=videoinfo'] = '{"foo": "boo"}'
        assert self.goprocam.getVideoInfo(option="foo",
                                          folder="fold",
                                          file='file.MP4') == 'boo'

    # below here is poorly-handled 'else' clauses
    def test_get_video_info_not_mp4(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: 'file.JPG')
            assert self.goprocam.getVideoInfo() is None

    def test_get_video_info_folder_not_mp4(self):
        assert self.goprocam.getVideoInfo(folder='folder') is None

    def test_get_video_info_file_not_mp4(self):
        assert self.goprocam.getVideoInfo(file='file.JPG') is None

    def test_get_video_info_option_file_not_mp4(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: 'file.JPG')
            with pytest.raises(json.decoder.JSONDecodeError):
                self.goprocam.getVideoInfo(option='foo',
                                           file='file.JPG')
