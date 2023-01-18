import json, os
import logging

from data_collectors import DataCollectorFactory

logger = logging.getLogger("dc_test_logger")
logger.setLevel(logging.DEBUG)

logFormatter = logging.Formatter(fmt=' %(name)s :: %(levelname)-8s :: %(message)s')

# create console handler
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(logFormatter)

# Add console handler to logger
logger.addHandler(consoleHandler)

logger.info("Starting Data Collection.")

with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as f:
    cfg = json.loads(f.read())
    logger.debug("Loaded config: %s" % cfg)

    # instantiate factory
    fact = DataCollectorFactory()

    for c in cfg:
        # skip data if it already exists:
        out_path = r"I:\DEIL\Data\Prod\Projects\DEIL_ISC\4-Collection\Fire Protection Services\lode-v3\collection"
        out_file = "%(area)s_fd.%(data_type)s" % c

        logger.debug("Output file %s exists: %s" % (os.path.join(out_path, out_file), os.path.exists(os.path.join(out_path, out_file))))

        if os.path.exists(os.path.join(out_path, out_file)):
            continue

        dc = fact.get_data_collector(c)

        dc.set_logger(logger)

        if dc.get_data():
            dc.set_output_dir(out_path)
            dc.set_output_file(out_file)
            dc.save_data()


logger.info("Data Collection Done.")