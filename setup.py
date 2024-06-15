from setuptools import setup

setup(
    name="solar_as_judge",
    version="0.1",
    url="https://github.com/hunkim/solar-as-judge",
    author="Sung Kim",
    author_email="hunkim@gmail.com",
    py_modules=["solar_as_judge"],
    packages=["solar_as_judge"],
    install_requires=[
        "langchain",
        "langchain-upstage",
    ],
)
