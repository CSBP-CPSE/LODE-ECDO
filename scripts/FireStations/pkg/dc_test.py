import json, os, sys
import logging
import pandas as pd

from data_collectors import DataCollectorFactory
from data_sniffers import DataSnifferFactory
from data_converters import DataConverterFactory
from pipelines import Pipeline

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

# read sources
sources = pd.read_json(os.path.join(os.path.dirname(__file__), "sources.json"), orient="records")
configs = pd.read_json(os.path.join(os.path.dirname(__file__), "configs.json"), orient="records")

cfg_df = sources.merge(configs, how="left", on="source_id")

# configure pipeline environment
cfg_df["cache_dir"]  = r"I:\DEIL\Data\Prod\Projects\DEIL_ISC\4-Collection\Fire Protection Services\lode-v3\collection"

joint_cfg = cfg_df.to_dict(orient="records")

logger.debug("Loaded config: %s" % joint_cfg)

# instantiate factories
factories = [DataCollectorFactory(logger), DataConverterFactory(logger)]

for c in joint_cfg:

    logger.debug("Config: %s" % c)

    pipeline = Pipeline(c["area"], logger)

    # TODO: pass a template, and let the element figure it out?
    c["cache_file"] =  "%(area)s_fd.%(data_type)s" % c

    for fact in factories:
        pipeline.push_back(fact.get_element(c))

    pipeline.connect_elements()

    pipeline.run()

logger.info("Pipelines completed.")