from setuptools import setup, find_packages

setup(
    name='veripress',
    version='1.0.6',
    packages=find_packages(),
    url='https://github.com/veripress/veripress',
    license='MIT License',
    author='Richard Chien',
    author_email='richardchienthebest@gmail.com',
    description='A blog engine for hackers.',
    install_requires=[
        'Flask', 'Flask-Caching', 'PyYAML', 'markdown',
        'Pygments', 'pytz'
    ],
    include_package_data=True,
    platforms='any',
    entry_points=dict(
        console_scripts=['veripress=veripress_cli:main']
    )
)
