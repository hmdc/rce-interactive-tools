import distutils
from os import chmod
from distutils.core import setup

class my_install(distutils.command.install_lib.install_lib):
  def run(self):
    distutils.command.install_lib.install_lib.run(self)
    for fn in self.get_outputs():
      if <this is one of the binaries I want to be executable>:
        # copied from distutils source - make the binaries executable
        mode = ((os.stat(fn).st_mode) | 0555) & 0755
        distutils.log.info("changing mode of %s to %o", fn, mode)
        os.chmod(fn, mode)

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

# This needs to be world-readable
# chmod('/etc/rceapp.yml.example', 0644)
