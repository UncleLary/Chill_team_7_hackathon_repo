import os
import logging
import logging.config
import yaml
import socket

def setup_logging():
    config_path = os.environ["LOG_CFG_PATH"]
    replica_name = socket.gethostname()
    with open(config_path, 'rt') as f:
        config = yaml.safe_load(f.read().replace("${REPLICA_NAME}", replica_name))
        logging.config.dictConfig(config)
