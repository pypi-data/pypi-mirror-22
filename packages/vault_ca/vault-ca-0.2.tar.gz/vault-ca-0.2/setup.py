import sys
import codecs
from distutils.core import setup
from setuptools import find_packages, Command


class FormatCommand(Command):
    description = "Python auto-formatter"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import yapf
        yapf.main([sys.executable, '--in-place', '--recursive', 'bin', 'vault_ca', 'tests'])


cmdclass = {
    'format': FormatCommand
}

with codecs.open('README.md', 'r', 'utf-8') as fd:
    setup(
        name='vault-ca',
        version='0.2',
        description='Set of utils to create your own CA using hashicorp Vault',
        long_description=fd.read(),
        author='Matteo Bigoi',
        author_email='bigo@crisidev.org',
        url='https://github.com/crisidev/vault-ca',
        license='GPLv3',
        download_url='https://github.com/crisidev/vault-ca/archive/0.2.tar.gz',
        keywords=['ssl', 'certificate-authority', 'vault'],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Unix Shell',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
        packages=find_packages(exclude=['docs', 'tests']),
        scripts=['bin/fetch-ssl-cert', 'bin/create-vault-ca'],
        install_requires=['appdirs', 'pyparsing', 'pyopenssl', 'requests'],
        cmdclass=cmdclass,
        setup_requires=['pytest-runner'],
        tests_require=['pytest', 'pytest-cov', 'requests-mock']
    )
