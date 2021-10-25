from setuptools import setup, find_packages

setup(
    name="pywu2d-client",
    version="0.3.1",
    description="Basic network client for UWU2D Framework",
    url="https://github.com/claybrooks/pywu2d-client",
    author="Clay Brooks",
    author_email="clay_brooks@outlook.com",
    license="The Unlicense (Unlicense)",
    packages=find_packages(),
    install_requires=[
        "websocket-client>=1.2.1",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ],
)
