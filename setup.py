from setuptools import setup, find_packages

setup(
    name="bacnet-adapter",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[
        "clearblade-python-sdk>=1.0.0",
        "paho-mqtt>=1.6.1",
        "bacpypes>=3.0.0",
    ],
    python_requires=">=3.7",
    author="ClearBlade",
    author_email="support@clearblade.com",
    description="A BACnet adapter that provides an interface between BACnet devices and MQTT messaging via the ClearBlade platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ClearBlade/BACnet-Adapter",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 