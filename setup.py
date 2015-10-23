from os import chmod
from distutils.core import setup

setup(name='rce-interactive-tools',
      version='1.5.15',
      description='HMDC utilities and scripts to submit condor jobs.',
      url='https://github.com/hmdc/rce-interactive-tools',
      author='Evan Sarmiento',
      author_email='https://github.com/hmdc/rce-interactive-tools',
      license='MIT',
      packages=['hmdccondor', 'rceapp'],
      requires=['pexpect', 'tabulate', 'progressbar', 'pyyaml'],
      data_files=[('/etc', ['rceapp.yml.example'])],
      scripts=[
        'scripts/rce-info.sh',
        'scripts/HMDC_job_wrapper_switch.sh',
        'scripts/rce_submit.py',
        'scripts/HMDC_interactive_prepare_job.py',
        'scripts/HMDC_periodic_job_is_idle.py',
        'scripts/HMDC_job_wrapper.py',
        'scripts/HMDC_clean_up.py',
        'scripts/pexpect_run.py'
        ]
)
