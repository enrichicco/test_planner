from setuptools import setup, find_packages

setup(
    name="test_planner",
    version="0.1.0",
    description="A task planning service using PyJobShop and PostgreSQL",
    author="AI Generated",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyjobshop>=1.0.0",
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
        "alembic>=1.13.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
        ]
    },
    python_requires=">=3.9",
)
