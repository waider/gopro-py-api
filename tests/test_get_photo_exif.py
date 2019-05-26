from .conftest import GoProCameraTest
from goprocam import GoProCamera
import pytest
import json


class GetPhotoEXIFTest(GoProCameraTest):
    def test_get_photo_exif(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: 'file1.JPG')
            self.responses[':8080/gp/gpMediaMetadata?p=file1.JPG/' +
                           'file1.JPG&t=exif'] = '{}'
            assert self.goprocam.getPhotoEXIF() == '{}'

    def test_get_photo_exif_folder(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: 'file1.JPG')
            assert self.goprocam.getPhotoEXIF(folder='folder') is None

    def test_get_photo_exif_file(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: 'file1.JPG')
            assert self.goprocam.getPhotoEXIF(file='file') is None

    def test_get_photo_exif_not_jpeg(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: 'file1.MP4')
            assert self.goprocam.getPhotoEXIF() is None

    def test_get_photo_exif_option(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: 'file1.JPG')
            self.responses[':8080/gp/gpMediaMetadata?p=file1.JPG/' +
                           'file1.JPG&t=exif'] = '{"foo": "bar"}'
            assert self.goprocam.getPhotoEXIF(option='foo') == "bar"

    def test_get_photo_exif_option_not_jpeg(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: 'file1.MP4')
            with pytest.raises(json.decoder.JSONDecodeError):
                self.goprocam.getPhotoEXIF(option='foo')

    def test_get_photo_exif_option_file_not_jpeg(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: 'file1.JPG')
            with pytest.raises(json.decoder.JSONDecodeError):
                self.goprocam.getPhotoEXIF(option='foo', file='file.MP4')

    def test_get_photo_exif_option_file_jpeg(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: 'file1.JPG')
            self.responses[':8080/gp/gpMediaMetadata?p=file1.JPG/' +
                           'file.JPG&t=exif'] = '{"foo": "bar"}'
            assert self.goprocam.getPhotoEXIF(option='foo',
                                              file='file.JPG') == 'bar'

    def test_get_photo_exif_option_folder(self):
        with self.monkeypatch.context() as m:
            m.setattr(GoProCamera.GoPro, 'getMediaInfo',
                      lambda s, x: 'file1.JPG')
            self.responses[':8080/gp/gpMediaMetadata?p=folder/' +
                           'file1.JPG&t=exif'] = '{"foo": "bar"}'
            assert self.goprocam.getPhotoEXIF(option='foo',
                                              file='file1.JPG',
                                              folder='folder') == "bar"
