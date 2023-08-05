from setuptools import setup
import os
import glob

exec(compile(open('hermes/_version.py').read(), 'hermes/_version.py', 'exec'))

setup(name='cfa_hermes',
      version=__version__,
      description='file tranfer monitor protocols ftp, sftp',
      url='https://github.com/cfauchard/hermes',
      author='Christophe Fauchard',
      author_email='christophe.fauchard@gmail.com',
      license='GPLV3',
      packages=['hermes'],
      scripts=['bin/hcmd.py','bin/hermesd.py'],
      data_files=[
            (
                  'sample/hermes', [
                        f for f in glob.glob(
                              os.path.join('sample', '*.hermes')
                        )
                  ]
            )
      ],
      install_requires=[
            'zeus >= 3.2.0.b1',
            'paramiko'
      ],
      zip_safe=False)
