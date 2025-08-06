from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sharda-attendance-bot",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A bot to check Sharda University attendance and send notifications via Telegram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sharda-attendance-bot",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "selenium>=4.0.0",
        "python-telegram-bot>=20.0",
        "python-dotenv>=0.19.0",
        "webdriver-manager>=3.8.0",
        "requests>=2.26.0",
        "python-dateutil>=2.8.2",
        "schedule>=1.1.0",
    ],
    entry_points={
        'console_scripts': [
            'sharda-attendance=src.__main__:main',
        ],
    },
    include_package_data=True,
)
