from distutils.core import setup
setup(
    name='flashback',
    packages=['flashback'],
    version='0.4',
    description='The handiest Flashback scraper in the game',
    author='Robin Linderborg',
    author_email='robin.linderborg@gmail.com',
    install_requires=[
        'beautifulsoup4==4.4.1',
        'requests==2.20.0'
    ],
    url='https://github.com/miroli/flashback',
    download_url='https://github.com/miroli/flashback/tarball/0.4',
    keywords=['flashback', 'scraping'],
    classifiers=[],
)
