from src.utils import common


def test_get_absolute_url(fixture_fake_get_setting):
    url = common.get_absolute_url("testpath")

    assert url == "https://test.host.com/testpath"
