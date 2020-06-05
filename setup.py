import setuptools
import x16cli.config as cfg


with open('README.md', 'r') as fh:
    long_description = fh.read()

requirements = [
    'click',
    'GitPython',
    'setuptools',
    'dotmap',
    'wheel',
    'twine',
    'toml',
    'gitchangelog',
]

setuptools.setup(
    name='x16cli',
    version=cfg.VERSION,
    author='Daniele Maccioni',
    author_email='komradstudios@gmail.com',
    description='X16 Command Line Interface for assembly projects.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/GendoIkari/x16cli',
    keywords=['x16', 'cx16', '6502', 'cc65'],
    python_requires='>=3.6',
    install_requires=requirements,
    packages=setuptools.find_packages(),
    scripts=['x16'],
)
