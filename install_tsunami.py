import sh
import sys
from subprocess import call, Popen, CalledProcessError, PIPE, STDOUT
import logger


def install_dependencies():

    sh.sudo("yum", "-y", "install", "wget.x86_64", _fg=True)
    sh.sudo("yum", "-y", "install", "make", _fg=True)
    sh.sudo("yum", "-y", "install", "automake", _fg=True)
    sh.sudo("yum", "-y", "install", "gcc", _fg=True)
    sh.sudo("yum", "-y", "install", "autoconf", _fg=True)
    sh.sudo("yum", "-y", "install", "cvs", _fg=True)


def install_tsunami():

    sh.wget("http://sourceforge.net/projects/tsunami-udp/files/latest/download?test=goal", "-O", "tsunami.tar.gz", _fg=True)
    sh.tar("-xzvf", "tsunami.tar.gz", _fg=True)
    directory = sh.glob("tsunami-udp-v*")

    try:
        sh.cd(directory[0])
    except OSError as e:
        logger.log.error(e.errno)
        logger.log.error(e.strerror)
        raise

    try:
        p = Popen(["sudo", "./recompile.sh"], stdout=PIPE, stderr=STDOUT)

        stdout, stderr = p.communicate()
        logger.log.info(stdout)
        logger.log.info(stderr)
    except CalledProcessError as e:
        error, = e.args
        logger.log.error(error.code)
        logger.log.error(error.message)
        raise

    try:
        p = Popen(["sudo", "make", "install"], stdout=PIPE, stderr=STDOUT)

        stdout, stderr = p.communicate()
        logger.log.info(stdout)
        logger.log.info(stderr)
    except CalledProcessError as e:
        error, = e.args
        logger.log.error(error.code)
        logger.log.error(error.message)
        raise

if __name__ == '__main__':

    print("This module can not be run as a stand-alone.")
    sys.exit()
