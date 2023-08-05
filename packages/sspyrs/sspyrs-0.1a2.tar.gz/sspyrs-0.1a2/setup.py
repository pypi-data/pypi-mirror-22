from setuptools import setup

setup(name='sspyrs',
      version='0.1a2',
      description='Lightweight interface for SSRS reports to python',
      long_description='',
      url='',
      author='James Nix',
      author_email='james.k.nix@gmail.com',
      license='MIT',
      packages=['sspyrs'],
      install_requires=[
           'pandas>=0.18.1',
           'xmltodict>=0.10.2',
           'requests_ntlm>=1.0.0'
      ],
      keywords=['ssrs report reporting sql'],
      zip_safe=False)
