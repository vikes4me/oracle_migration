from __future__ import print_function
import sys
from subprocess import Popen, CalledProcessError, PIPE, STDOUT
import logger
from glob import glob


def install_dependencies():

    try:
        p = Popen(["yum", "-y", "install", "wget.x86_64"], stdout=PIPE, stderr=STDOUT)
        stdout, stderr = p.communicate()
        logger.log.info(stdout)
    except CalledProcessError as e:
        logger.log.error(str(e))
        raise
    try:
        p = Popen(["yum", "-y", "install", "make"], stdout=PIPE, stderr=STDOUT)
        stdout, stderr = p.communicate()
        logger.log.info(stdout)
    except CalledProcessError as e:
        logger.log.error(str(e))
        raise
    try:
        p = Popen(["yum", "-y", "install", "automake"], stdout=PIPE, stderr=STDOUT)
        stdout, stderr = p.communicate()
        logger.log.info(stdout)
    except CalledProcessError as e:
        logger.log.error(str(e))
        raise
    try:
        p = Popen(["yum", "-y", "install", "gcc"], stdout=PIPE, stderr=STDOUT)
        stdout, stderr = p.communicate()
        logger.log.info(stdout)
    except CalledProcessError as e:
        logger.log.error(str(e))
        raise
    try:
        p = Popen(["yum", "-y", "install", "autoconf"], stdout=PIPE, stderr=STDOUT)
        stdout, stderr = p.communicate()
        logger.log.info(stdout)
    except CalledProcessError as e:
        logger.log.error(str(e))
        raise
    try:
        p = Popen(["yum", "-y", "install", "cvs"], stdout=PIPE, stderr=STDOUT)
        stdout, stderr = p.communicate()
        logger.log.info(stdout)
    except CalledProcessError as e:
        logger.log.error(str(e))
        raise


def install_tsunami():

    try:
        p = Popen(["wget", "http://sourceforge.net/projects/tsunami-udp/files/latest/download?test=goal",
                   "-O", "tsunami.tar.gz"], stdout=PIPE, stderr=STDOUT)
        stdout, stderr = p.communicate()
        logger.log.info(stdout)
    except CalledProcessError as e:
        logger.log.error(str(e))
        raise

    try:
        p = Popen(["tar", "-xzvf", "tsunami.tar.gz"], stdout=PIPE, stderr=STDOUT)
        stdout, stderr = p.communicate()
        logger.log.info(stdout)
    except CalledProcessError as e:
        logger.log.error(str(e))
        raise

    try:
        directory = glob("tsunami-udp-v*")
    except OSError as e:
        logger.log.error(str(e))
        raise

    try:
        p = Popen(["./recompile.sh"], cwd=directory[0], stdout=PIPE, stderr=STDOUT)

        stdout, stderr = p.communicate()
        logger.log.info(stdout)
    except CalledProcessError as e:
        logger.log.error(str(e))
        raise

    try:
        p = Popen(["make", "install"], cwd=directory[0], stdout=PIPE, stderr=STDOUT)

        stdout, stderr = p.communicate()
        logger.log.info(stdout)
    except CalledProcessError as e:
        logger.log.error(str(e))
        raise

if __name__ == '__main__':

    print("This module can not be run as a stand-alone.")
    sys.exit()

