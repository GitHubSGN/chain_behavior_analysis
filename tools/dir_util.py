import os
import shutil
from datetime import datetime

def project_dir():
    # get root directory of the project
    # print(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(project_dir)
    return project_dir

def dir_mk_clr(res_dir, is_clear = False):
    # judge directory, mkdir <if> not exists <else> clear <if> is_clear
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)
    else:
        if is_clear:
            shutil.rmtree(res_dir, ignore_errors=True)
            os.mkdir(res_dir)



# EXP RESULT DIRECTORY RELATED
def dir_exp_today_sub():
    # return sub-directory of today exp, e.g., 'exp_result/20220530'
    return os.path.join('exp_result', datetime.today().strftime('%Y%m%d'))

def dir_exp_today():
    # return exp directory of today
    # v1: use project root directory
    # v2: use root directory indicated by environment variable for run on aws server
    return os.path.join( os.environ.get("OUTPUT_DIR"), dir_exp_today_sub() )

def dir_exp_sday(day):
    # return exp directory of specified day
    return os.path.join(project_dir(), 'exp_result', day)

def dir_exp_today_name(exp_name):
    # return directory for current experiment with name exp_name
    return os.path.join( dir_exp_today(), exp_name + datetime.now().strftime('_%H%M%S') )



# FILE OPERATION RELATED
def movefile(srcfile, dstpath):
    # move file from srcfile to destpath
    if not os.path.isfile(srcfile):
        print ("%s not exist!" % (srcfile) )
    else:
        fpath, fname = os.path.split(srcfile)
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)
        shutil.move(srcfile, os.path.join(dstpath, fname) )
        print ("move %s -> %s"%(srcfile, os.path.join(dstpath, fname)))
