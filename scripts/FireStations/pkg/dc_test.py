import json, os
import logging

from data_collectors import DataCollectorFactory
from data_sniffers import DataSnifferFactory
from data_converters import DataConverterFactory

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

    # instantiate factories
    factories = [DataCollectorFactory(logger), DataSnifferFactory(logger), DataConverterFactory(logger)]

    pipeline = []

    for c in cfg:
        #if c["data_type"] != "kml":
        #if c["data_delivery"] != "file":
        #    continue

        # configure pipeline environment
        c["cache_dir"]  = r"I:\DEIL\Data\Prod\Projects\DEIL_ISC\4-Collection\Fire Protection Services\lode-v3\collection"
        c["cache_file"] =  "%(area)s_fd.%(data_type)s" % c

        for fact in factories:
            pipeline.append(fact.get_element(c))

    # connect pipeline elements together, and pass the data
    for i in range(1, len(pipeline)):
        pipeline[i].set_source(pipeline[i-1])

    pipeline[-1].pass_data()

    #pipeline[-1]._data.to_file(r"I:\DEIL\Data\Prod\Projects\DEIL_ISC\4-Collection\Fire Protection Services\lode-v3\output\fire_wiki.geojson", driver="GeoJSON")


logger.info("Pipeline complete.")