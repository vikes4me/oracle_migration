#!/usr/bin/env python

"""
transfer_files_to_bridge.py:
This module is used to transfer dump files from on-prem to ec2 bridge which sits in the same vpc as RDS instance
"""
from __future__ import print_function
from read_config import read_config
import paramiko
import sys
import time
import logger


def transfer_files(config_file):

    # logger.log.info("TRANSFER_FILES_TO_BRIDGE\n")

    config_dict = read_config(config_file)

    ec2_username = config_dict["ec2Info"]["username"]
    ec2_hostname = config_dict["ec2Info"]["hostname"]
    ec2_priv_key_loc = config_dict["ec2Info"]["private_key_loc"]
    ec2_priv_key_name = config_dict["ec2Info"]["private_key_name"]
    ec2_source_hostname = config_dict["ec2Info"]["source_hostname"]

    priv_key_name = ec2_priv_key_loc + ec2_priv_key_name
    priv_key = paramiko.RSAKey.from_private_key_file(priv_key_name)
    '''
    commands = ["sudo yum -y install wget.x86_64", "sudo yum -y install make", "sudo yum -y install automake",
                "sudo yum -y install gcc", "sudo yum -y install autoconf", "sudo yum -y install cvs",
                "wget http://sourceforge.net/projects/tsunami-udp/files/latest/download?test=goal -O tsunami.tar.gz",
                "tar -xzvf tsunami.tar.gz", "cd tsunami-udp-v*", "sudo ./recompile.sh", "sudo make install"]
    '''
    commands = ["yum -y install wget.x86_64", "yum -y install make", "yum -y install automake",
                "yum -y install gcc", "yum -y install autoconf", "yum -y install cvs",
                "wget http://sourceforge.net/projects/tsunami-udp/files/latest/download?test=goal -O tsunami.tar.gz",
                "tar -xzvf tsunami.tar.gz", "cd tsunami-udp-v*", "./recompile.sh", "make install"]

    get_files = "tsunami connect " + ec2_source_hostname + " get \*"

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        client.load_system_host_keys()
        client.connect(hostname=ec2_hostname, username=ec2_username, pkey=priv_key)

        for command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            logger.log.info(command)
            logger.log.info(stdout.read())

        stdin, stdout, stderr = client.exec_command(get_files)
        logger.log.info(get_files)
        # wait for tsunami to finish since exec_command is a non-blocking call
        while not stdout.channel.exit_status_ready() and not stdout.channel.recv_ready():
            time.sleep(1)
            #logger.log.info(stdout.read())

    finally:
        client.close()

if __name__ == '__main__':

    print("This module can not be run as a stand-alone.")
    sys.exit()
