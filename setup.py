from setuptools import setup


requirements = [
    "PyYAML==6.0"
]

setup(
    install_requires=requirements,
    extras_require={
        "dev": [
            "pylint==2.12.2",
            "pytest==7.0.1"
        ]
    },
    entry_points={
        'console_scripts': [
            'mkpkg = mkpkg.mymodule:some_func',
        ]
    }
)
