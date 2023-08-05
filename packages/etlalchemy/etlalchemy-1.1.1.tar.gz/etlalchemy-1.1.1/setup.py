from distutils.core import setup
setup(
        name = 'etlalchemy',
        packages = ['etlalchemy'],
        version = '1.1.1',
        description = 'Extract, Transform, Load. Migrate any SQL Database in 4 lines of code',
        author = 'Sean Harrington',
        author_email='seanharr11@gmail.com',
        url='https://github.com/seanharr11/etlalchemy',
        download_url='https://github.com/seanharr11/etlalchemy/archive/1.1.1.tar.gz',
        keywords=['sql','migration','etl','database'],
        install_requires = [
            "py == 1.4.31",
            "six == 1.9.0",
            "SQLAlchemy == 1.0.13",
            "sqlalchemy-migrate == 0.9.7",
            "SQLAlchemy-Utils == 0.30.9"
        ],
        classifiers=[],
)
