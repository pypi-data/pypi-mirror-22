from setuptools import setup

setup(name='genderly',
      version='0.102',
      description='A library to classify an indian name as Male or Female. Mainly focused around making the user onboarding smooth for eCommerce merchants by pre-filling the gender for their users during a signup.',
      url='https://github.com/rajdeltarobo/genderly',
      author='Raj Vardhan Singh',
      author_email='is.rajvardhan@gmail.com',
      license='MIT',
      packages=['genderly'],
      include_package_data=True,
      data_files=[('genderly/data/', ['*.*']),
                  ('genderly/model', ['*.*'])],
      zip_safe=False)