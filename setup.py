from setuptools import setup


setup(
    name='gitlab-build-hooks-python',
    version="0.1",
    description='A collection of tools to use in gitlab builds.',
    author='zeeke',
    py_modules=['trello_commit_to_card'],
    include_package_data=True,
    test_suite='tests',
    install_requires=['ConfigArgParse', 'python-gitlab', 'py-trello']
)
