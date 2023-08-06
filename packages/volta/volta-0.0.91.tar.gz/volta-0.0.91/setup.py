from setuptools import setup, find_packages

setup(
    name='volta',
    version='0.0.91',
    description='yandex package for mobile energy consumption measurements',
    longer_description='''
yandex package for mobile energy consumption measurements
''',
    maintainer='Alexey Lavrenuke (load testing)',
    maintainer_email='direvius@yandex-team.ru',
    url='https://github.com/yandex-load/volta',
    packages=find_packages(exclude=["tests", "tmp", "docs", "data"]),
    install_requires=[
        'tornado',
        'pandas',
        'seaborn',
        'numpy',
        'scipy',
        'matplotlib',
        'requests',
        'pyserial',
        'progressbar2',
        'pyusb',
        'pyyaml'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'volta = volta.wizard.ui:main',
            'volta-ui = volta.ui.ui:main',
            'volta-sync = volta.analysis.sync:main',
            'volta-grab = volta.analysis.grab:run',
            'volta-uploader = volta.analysis.uploader:run',
            'volta-wizard = volta.analysis.wizard:run',
            'volta-wizard-ui = volta.wizard.ui:main',
            'volta-realtime = volta.analysis.realtime:main',
            'volta2 = volta.core.cli:main',
        ],
    },
    license='MPLv2',
    package_data={
        'volta.ui': [
            'static/*',
            'handlers/*',
        ],
        'volta.wizard': [
            'static/*',
            'handlers/*',
            '*.html',
        ],
        'volta.analysis': [
            '*.db',
        ],
        'volta.Phones': [
            'binary/*.apk'
        ]
    },
    data_files=[
        ('/usr/local/bin', ['volta/reader/serial-reader']),
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Testing :: Traffic Generation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    use_2to3=True, )
