import sh
import sys


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
        sh.sudo("./recompile.sh")
    except OSError as e:
        print e.errno
        print e.strerror
        raise

    sh.sudo("make", "install")


if __name__ == '__main__':
    print("This module can not be run as a stand-alone.")
    sys.exit()
