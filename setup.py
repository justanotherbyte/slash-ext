from setuptools import setup, find_packages
import os







DESCRIPTION = 'A discord.py slash commands extension'

# Setting up
setup(
    name="dpy-slash-ext",
    version="0.0.1a",
    author="quiktea",
    author_email="wishymovies@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    packages=find_packages(),
    install_requires=['discord.py', 'aiohttp'],
    keywords=['python', 'discord.py', 'slash commands', 'discord', 'api', 'discord api'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)