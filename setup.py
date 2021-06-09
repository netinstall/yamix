from setuptools import setup


setup(
    name="yamix",
    version="0.1.10",
    scripts=["web.py"],
    description="Mix Yandex Music Playlist",
    install_requires=[
        "bottle",
        "requests"],
    packages=["yamix"],
    package_data={'yamix': ["main.tpl"]}
) 
