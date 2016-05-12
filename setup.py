from distutils.core import setup
# from setuptools.command.install import install
# import os
#
# class Recce7Install(install):
#     """ Post install scripts to install authbind """
#     def run (self):
#         os.system('sudo apt-get install -y authbind')
#         install.run(self)
# # cmdclass={'install': Recce7Install},

setup(name='recce7',
      version='1.0',
      description='Report Server',
      author='Jesse Nelson',
      author_email='jnels124@msudenver.edu',
      install_requires=['python-dateutil', 'p0f', 'requests'],
      data_files=[('/etc/recce7/configs/', ['install/configs/plugins.cfg', 'install/configs/global.cfg']),
                  ('/usr/sbin/recce7/database/sql_scripts', ['database/sql_scripts/sessions.sql'])],
      scripts=['install/scripts/startReportServer.sh',  'install/scripts/recce7.sh', 'install/scripts/authbind_recce7.sh'],
      packages=['framework', 'plugins', 'database', 'common', 'recon', 'reportserver',
                'reportserver.dao', 'reportserver.manager', 'reportserver.server'])
