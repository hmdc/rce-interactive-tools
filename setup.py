from os import chmod
from distutils.core import setup

setup(name='rce-interactive-tools',
      version='1.0',
      description='HMDC utilities and scripts to submit condor jobs.',
      url='https://github.com/hmdc/rce-interactive-tools',
      author='Evan Sarmiento',
      author_email='https://github.com/hmdc/rce-interactive-tools',
      license='MIT',
      cmdclass={'install': my_install},
      packages=['hmdccondor', 'rceapp'],
      requires=['pexpect', 'tabulate', 'progressbar', 'pyyaml'],
      data_files=[('/etc', ['rceapp.yml.example'])],
      scripts=[
        'scripts/rce_submit.py',
        'scripts/HMDC_interactive_prepare_job.py',
        'scripts/HMDC_job_wrapper.py',
        'scripts/pexpect_run.py'
        ]
)
