from setuptools import setup, find_packages

setup(
    name="insnc",
    version="0.3",
    packages=find_packages(),
    install_requires=["requests", "openpyxl"],
    entry_points={
        "console_scripts": [
            "insnc = insnc.main:main"
        ]
    },
)
