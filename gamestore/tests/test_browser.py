"""
Testing against browser with Selenium. Uses ``pytest-selenium`` package which
provides handy ``selenium`` fixture.

- Firefox
- Chrome
- Safari
- Opera
- Android

References

https://pytest-selenium.readthedocs.io/en/latest/user_guide.html#quick-start
https://medium.com/@unary/django-views-automated-testing-with-selenium-d9df95bdc926#.w0ijolfgn
"""
import pytest


@pytest.mark.skip
def test_browser(selenium):
    selenium.get('http://www.example.com')
    assert True

