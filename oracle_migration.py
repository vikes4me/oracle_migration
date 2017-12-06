#!/usr/bin/env python

"""
oracle_migration.py:
This module is used to export all user schemas from db instance and transfer them over to ec2 instance
"""

from datetime import datetime
from subprocess import call, Popen, CalledProcessError, PIPE, STDOUT
import cx_Oracle
import multiprocessing
import sys
import install_tsunami
from read_config import read_config
import transfer_files_to_bridge
import logger
from os import environ

__author__ = "AWS RDS Support"
__version__ = "1.0"
__requirements = "Must be executed as 'oracle' shell account and oracle user must be 'system'"


def exec_sql(sql):

    dsn = cx_Oracle.makedsn(hostip, port, service_name=service_name)

    try:
        db = cx_Oracle.connect(username, password, dsn)
        cursor = db.cursor()
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        logger.log.error(error.code)
        logger.log.error(error.message)
        raise
    try:
        cursor.execute(sql)
        return cursor
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        logger.log.error(error.code)
        logger.log.error(error.message)
        cursor.close()
        db.close()
        raise


def dp_dir_exists():

    sql = """
           select count(1) 
           from dba_directories 
           where directory_name='DATA_PUMP_DIR'
        """

    result = exec_sql(sql)
    count = result.fetchone()[0]

    if count == 1:
        return True
    else:
        return False


def oracle_edition():

    sql = """
           select case instr(product, 'Enterprise') when 0 then 'N' else 'Y' end, version 
           from product_component_version 
           where product like 'Oracle%'"""

    result = exec_sql(sql)
    is_enterprise, db_version = result.fetchone()

    logger.log.info("is_enterprise = %s", is_enterprise)
    logger.log.info("db_version = %s", str(db_version))

    return is_enterprise


def get_instance_name():

    sql = """
          select lower(sys_context('USERENV','DB_NAME')) as instance from dual"""

    result = exec_sql(sql)
    instance_name = result.fetchone()[0]

    return instance_name


def get_dp_path():

    sql = """
          select directory_path 
          from dba_directories 
          where directory_name='DATA_PUMP_DIR'"""

    result = exec_sql(sql)
    dp_path = result.fetchone()[0]

    return dp_path


def get_schemas():

    sql = """
          select username 
          from dba_users 
          where default_tablespace not in ('SYSAUX','SYSTEM', 'RDSADMIN') 
          and account_status='OPEN' order by username"""

    result = exec_sql(sql)
    schema_list = result.fetchall()

    return schema_list


def create_par_file():

    dp_dir = get_dp_path()
    get_instance_name()
    is_enterprise = oracle_edition()
    schema_list = get_schemas()

    try:
        with open(dp_dir + "expdp_" + instance_name + ".par", 'w') as fh:
            fh.write("directory=data_pump_dir\n")
            fh.write("dumpfile=expdp_" + instance_name + "_%u.dmp\n")
            fh.write("filesize=2GB\n")
            fh.write("flashback_time=systimestamp\n")
            fh.write("logfile=expdp_" + instance_name + ".log\n")
            fh.write("reuse_dumpfiles=Y\n")
            if is_enterprise == 'Y':
                num_of_cores = multiprocessing.cpu_count()
                fh.write("parallel=" + str(num_of_cores / 2) + "\n")

            fh.write("schemas=")
            num_schemas = len(schema_list)
            i = 1

            for schema in schema_list:
                if i != num_schemas:
                    fh.write(str(schema[0]) + ",")
                    i += 1
                else:
                    fh.write(str(schema[0]) + "\n")
    except EnvironmentError as e:
        logger.log.error(e.message)
        raise


def begin_export():

    dp_dir = get_dp_path()
    expdp_args = "parfile=" + dp_dir + "expdp_" + instance_name + ".par"

    try:
        p = Popen([ORACLE_HOME + "/bin/expdp", username + "/" + password + "@" + service_name + " " + expdp_args], stdout=PIPE, stderr=STDOUT)

        stdout, stderr = p.communicate()
        logger.log.info(stdout)
    except CalledProcessError as e:
        '''error, = e.args
        logger.log.error(error.code)
        logger.log.error(error.message)
        raise'''
        logger.log.error(str(e))

        raise


def main():

    logger.log.info('Started at %s', str(datetime.now()))

    passed = dp_dir_exists()

    if not passed:
        logger.log.error("Please make sure DATA_PUMP_DIR exists before running this script.")
        sys.exit(1)

    create_par_file()
    begin_export()
    install_tsunami.install_dependencies()
    install_tsunami.install_tsunami()
    dp_dir = get_dp_path()

    p1 = Popen(["tsunamid " + dp_dir + "expdp_" + instance_name + "*"], shell=True)
    transfer_files_to_bridge.transfer_files()
    p1.kill()

    logger.log.info('Finished at ' + str(datetime.now()))


if __name__ == '__main__':

    config_dict = read_config()

    try:
        ORACLE_HOME = environ["ORACLE_HOME"]
    except KeyError as e:
        logger.log.error(str(e))
        sys.exit(1)

    username = config_dict["dbInfo"]["username"]
    password = config_dict["dbInfo"]["password"]
    hostip = config_dict["dbInfo"]["hostip"]
    service_name = config_dict["dbInfo"]["service_name"]
    port = config_dict["dbInfo"]["port"]
    instance_name = get_instance_name()

    main()
    sys.exit()