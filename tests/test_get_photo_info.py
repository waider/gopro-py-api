from .conftest import GoProCameraTest
from goprocam import GoProCamera
import pytest
import json


class GetPhotoInfoTest(GoProCameraTest):
    def test_get_photo_info(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: x if x == 'folder' else 'file.JPG')
            self.responses[':8080/gp/gpMediaMetadata?p=folder/' +
                           'file.JPG&t=v4info'] = 'boo'
            assert self.goprocam.getPhotoInfo() == 'boo'

    def test_get_photo_info_option(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: x if x == 'folder' else 'file.JPG')
            self.responses[':8080/gp/gpMediaMetadata?p=folder/' +
                           'file.JPG&t=v4info'] = '{"foo": "boo"}'
            assert self.goprocam.getPhotoInfo(option="foo") == 'boo'

    def test_get_photo_info_option_file(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: x if x == 'folder' else None)
            self.responses[':8080/gp/gpMediaMetadata?p=folder/' +
                           'file.JPG&t=v4info'] = '{"foo": "boo"}'
            assert self.goprocam.getPhotoInfo(option="foo",
                                              file='file.JPG') == 'boo'

    def test_get_photo_info_option_file_folder(self):
        self.responses[':8080/gp/gpMediaMetadata?p=fold/' +
                       'file.JPG&t=v4info'] = '{"foo": "boo"}'
        assert self.goprocam.getPhotoInfo(option="foo",
                                          folder="fold",
                                          file='file.JPG') == 'boo'

    # coverage for unhandled else clauses
    def test_get_photo_info_not_jpg(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: 'file.MP4')
            assert self.goprocam.getPhotoInfo() is None

    def test_get_photo_info_file(self):
        assert self.goprocam.getPhotoInfo(file='file.JPG') is None

    def test_get_photo_info_folder(self):
        assert self.goprocam.getPhotoInfo(folder='folder') is None

    def test_get_photo_info_option_not_jpg(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: 'file.MP4')
            with pytest.raises(json.decoder.JSONDecodeError):
                self.goprocam.getPhotoInfo(option='foo')

    def test_get_photo_info_option_file_not_jpg(self):
        with pytest.raises(json.decoder.JSONDecodeError):
            self.goprocam.getPhotoInfo(option='foo', file='file.MP4')
