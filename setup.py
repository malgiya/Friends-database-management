from setuptools import setup, find_packages

setup(
    name="PUT FRNDS",
    version="0.1.0",
    description="Your project description",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "jinja2",
        "mysqlclient",
        "python-dotenv"
    ],
    setup_requires=["setuptools>=42", "wheel"],
)
