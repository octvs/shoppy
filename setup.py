from setuptools import setup

setup(
    name="shoppy",
    version="0.1",
    description="a simple script as a minimalist replacement for shopping list apps",
    url="https://github.com/cenktaskin/shoppy",
    author="C. Taskin",
    author_email="orhuncenktaskin@gmail.com",
    entry_points={"console_scripts": ["shoppy=shoppy.command_line:main"]},
    install_requires=["pyfzf", "termcolor"],
)
