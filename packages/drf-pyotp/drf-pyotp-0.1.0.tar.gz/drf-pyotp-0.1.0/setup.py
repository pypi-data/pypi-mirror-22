from distutils.core import setup
from setuptools import find_packages

setup(
  name='drf-pyotp',
  packages=find_packages(exclude=['example']),
  version='0.1.0',
  description='Rest extension of PyOTP python library, Here OTP generation and Verification is done via DRF APIs.',
  author='Neeraj Dhiman',
  author_email='ndhiman08@gmail.com',
  license='GPL',
  url='https://github.com/inforian/drf-pyotp',
  download_url='https://github.com/inforian/drf-pyotp/archive/0.1.0tar.gz',
  keywords=['otp', 'pyotp', 'totp', 'hotp', 'drf-pyotp'],
  classifiers=[],
)