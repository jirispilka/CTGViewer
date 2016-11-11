# -*- coding: utf-8 -*-
#
# Created on Sept, 23 2014
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)

import os
import shutil
import io
import sys

sOldVersion = "0.3.00"
sNewVersion = "0.3.10"


def run():

    print('Setting version: ' + sNewVersion)

    afiles = 'setup.py', 'AboutUI.ui', 'copy_to_web.sh', 'setup_inno.iss', 'doc/conf.py'
    file_temp = 'temp.txt'

    cnt_error = 0
    for fname in afiles:

        # create backup file (if something goes wrong)
        fname_backup = fname + '_backup'
        shutil.copy(fname, fname_backup)

        with io.open(file_temp, "wt", encoding='utf-8') as fout:
            with io.open(fname, "rt", encoding='utf-8') as fin:
                for line in fin:
                    fout.write(line.replace(sOldVersion, sNewVersion))

        fout.close()
        fin.close()

        try:
            shutil.copy(file_temp, fname)
            print fname + ' ... done'
            os.remove(fname_backup)
        except:
            cnt_error += 1
            shutil.copy(fname_backup, fname)
            print fname + 'error - original file was restored'

    if sys.platform == 'linux2':
        os.system("pyuic4 AboutUI.ui -o AboutUI.py")
        os.system("chmod 775 copy_to_web.sh")
    else:
        os.system('c:\Python26\Lib\site-packages\PyQt4\pyuic4.bat AboutUI.ui -o AboutUI.py')

    os.remove(file_temp)

    if cnt_error > 0:
        print 'Version number not proerly set in all files!'
    else:
        print('All versions were replaced')

if __name__ == '__main__':
    run()
