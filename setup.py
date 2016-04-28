from distutils.core import setup

setup(name='recce7',
      version='1.0',
      description='Report Server',
      author='Jesse Nelson',
      author_email='jnels124@msudenver.edu',
      data_files=[('/etc/recce7/configs/', ['config/plugins.cfg', 'config/global.cfg']),
                  ('/usr/local/sbin/recce7/database/sql_scripts', ['database/sql_scripts/sessions.sql'])],
      scripts=['startReportServer.sh'],
      packages=['framework', 'plugins', 'database', 'database.sql_scripts', 'common', 'reportserver', 'reportserver.dao', 'reportserver.manager', 'reportserver.server'])
