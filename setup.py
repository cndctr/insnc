from setuptools import setup

setup(
    name="insnc",
    version="0.1",
    py_modules=["main"],
    install_requires=["requests", "pandas", "openpyxl"],
    entry_points={
        "console_scripts": [
            "insnc = main:main"
        ]
    },
)
