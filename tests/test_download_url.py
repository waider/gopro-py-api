from .conftest import GoProCameraTest
import urllib.request
import urllib.error
import pytest


class DownloadUrlTest(GoProCameraTest):
    def test_download_url_short_read(self):
        with self.monkeypatch.context() as m:
            def broken_urlretrieve(url, path):
                raise urllib.error.ContentTooShortError('short read', 'brp')
            m.setattr(urllib.request, 'urlretrieve', broken_urlretrieve)
            with pytest.raises(urllib.error.ContentTooShortError):
                self.goprocam.download_url('foo', 'bar')
