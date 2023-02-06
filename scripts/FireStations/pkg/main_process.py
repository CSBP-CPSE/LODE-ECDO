import json, os, sys
import logging
import pandas as pd
from numpy import nan

from data_collectors import DataCollectorFactory
from data_converters import DataConverterFactory
from data_tabulators import DataTabulatorFactory
from data_fillers import DataFillerFactory
from data_filters import DataFilterFactory
from geocoders import GeocoderFactory
from pipelines import Pipeline, PipelineCollection, Merger

def main():
    logger = logging.getLogger("main_process_logger")
    logger.setLevel(logging.DEBUG)

    logFormatter = logging.Formatter(fmt=' %(name)s :: %(levelname)-8s :: %(message)s')

    # create console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(logFormatter)

    # Add console handler to logger
    logger.addHandler(consoleHandler)

    # Add file handler
    fileHandler = logging.FileHandler(filename="main_process.log")
    logger.addHandler(fileHandler)

    logger.info("Starting Data Collection.")

    # read sources
    sources = pd.read_json(os.path.join(os.path.dirname(__file__), "sources.json"), orient="records")
    configs = pd.read_json(os.path.join(os.path.dirname(__file__), "configs.json"), orient="records")

    cfg_df = sources.merge(configs, how="left", on="source_id").fillna(nan).replace([nan], [None])

    # load main configuration, and join the two
    main_cfg = json.loads(open(os.path.join(os.path.dirname(__file__), "process_config.json"), "r").read())

    joint_cfg = cfg_df.to_dict(orient="records")

    [d.update(main_cfg) for d in joint_cfg]

    logger.debug("Loaded config: %s" % joint_cfg)

    # instantiate factories
    factories = [DataCollectorFactory(logger), DataConverterFactory(logger), DataFillerFactory(logger), DataFilterFactory(logger), DataTabulatorFactory(logger)]

    pipelines = PipelineCollection()

    for c in joint_cfg:

        logger.debug("Config: %s" % c)

        pipeline = Pipeline(c["area"])

        # TODO: pass a template, and let the element figure it out?
        c["cache_file"] =  "%(area)s_fd.%(data_type)s" % c

        for fact in factories:
            pipeline.push_back(fact.get_element(c))

        pipeline.set_logger(logger)
        pipeline.connect_elements()

        pipelines.add_pipeline(pipeline)

    #all_data.to_file(os.path.join(main_cfg["cache_dir"], "miscuglione.json"), driver="GeoJSON")
    #all_data.to_csv(os.path.join(main_cfg["cache_dir"], "miscuglione.csv"))

    merger = Merger({})
    merger.set_logger(logger)
    merger.set_source(pipelines)

    csd_finder = GeocoderFactory(logger).get_element(main_cfg)
    csd_finder.set_source(merger)

    csd_finder.pass_data().to_file(os.path.join(main_cfg["cache_dir"], "miscuglione2.json"), driver="GeoJSON")

    logger.info("Pipelines completed.")

if __name__ == "__main__":
    main()