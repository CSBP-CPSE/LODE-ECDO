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

    for c in cfg:
        #if c["data_type"] != "kml":
        if c["data_delivery"] != "file":
            continue

        # skip data if it already exists:
        out_path = r"I:\DEIL\Data\Prod\Projects\DEIL_ISC\4-Collection\Fire Protection Services\lode-v3\collection"
        out_file = "%(area)s_fd.%(data_type)s" % c

        #logger.debug("Output file %s exists: %s" % (os.path.join(out_path, out_file), os.path.exists(os.path.join(out_path, out_file))))

        #if os.path.exists(os.path.join(out_path, out_file)):
        #    continue

        dc = factories[0].get_element(c)
        dc.set_cache_dir(out_path)
        dc.set_cache_file(out_file)

        ds = factories[1].get_element(c)
        ds.set_source(dc)

        dk = factories[2].get_element(c)
        dk.set_source(ds)

        if dc.get_data():
            ds.get_data()
            logger.info(ds.get_attributes())
            dk.convert_data()
            dk._data.to_file(r"I:\DEIL\Data\Prod\Projects\DEIL_ISC\4-Collection\Fire Protection Services\lode-v3\output\fire_wiki.geojson", driver="GeoJSON")
        #    logger.info("Data read.")    
            #dc.save_data()


logger.info("Data Collection Done.")