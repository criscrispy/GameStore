from setuptools import setup, find_packages

setup(
    name="wsdproject",
    version="0.1",
    packages=find_packages(),
    scripts=[],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['docutils>=0.3'],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.md'],
        # And include any *.msg files found in the 'hello' package, too:
        # 'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author="",
    author_email="",
    description="",
    license="MIT",
    keywords="",
    url="",   # project home page

    # could also include long_description, download_url, classifiers, etc.
)
