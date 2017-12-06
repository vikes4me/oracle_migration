import logging
import sys

LOG_FILE = "oracle_migration.log"
file_handler = logging.FileHandler(filename='oracle_migration.log')
stdout_handler = logging.StreamHandler(sys.stdout)

handlers = [file_handler, stdout_handler]
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=handlers)

log = logging.getLogger('LOGGER_NAME')
log.addHandler(file_handler)
log.addHandler(stdout_handler)

