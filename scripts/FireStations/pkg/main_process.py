import json, os, sys
import logging
import pandas as pd
from numpy import nan

from data_collectors import DataCollectorFactory
from data_converters import DataConverterFactory
from data_tabulators import DataTabulatorFactory
from data_fillers import DataFillerFactory
from data_filters import DataFilterFactory
from deduplicators import DeduplicatorFactory
from deduplicators.DuplicateMerger import DuplicateMerger
from geocoders import GeocoderFactory
from pipelines import Pipeline, PipelineCollection, Merger, BinarySplitter

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
        

        pipelines.add_pipeline(pipeline)

    pipelines.broadcast_connect()

    #all_data.to_file(os.path.join(main_cfg["cache_dir"], "miscuglione.json"), driver="GeoJSON")
    #all_data.to_csv(os.path.join(main_cfg["cache_dir"], "miscuglione.csv"))

    merger = Merger({})
    merger.set_logger(logger)
    merger.set_source(pipelines)

    # second part of the pipeline: Geocoder, splitter
    pipeline2 = Pipeline("Geocoder_Splitter")
    pipeline2.set_logger(logger)

    csd_finder = GeocoderFactory(logger).get_element(main_cfg)
    
    pipeline2.push_back(csd_finder)

    binary_splitter = BinarySplitter(main_cfg)
    binary_splitter.set_logger(logger)

    pipeline2.push_back(binary_splitter)

    pipeline2.set_source(merger)
    
    

    #csd_finder.set_source(merger)

    #ds = BinarySplitter(cfg)
    #ds.set_logger(log)

    pipeline2.connect_elements()

    pipelines2 = PipelineCollection()

    p0 = Pipeline("Splitter: false")
    p0.set_logger(logger)
    p1 = Pipeline("Splitter: true")
    p1.set_logger(logger)

    p0.set_source(binary_splitter.get_slot(0))
    p1.set_source(binary_splitter.get_slot(1))

    # use Deduplicator on false branch
    geo_compare = DeduplicatorFactory(logger).get_element(main_cfg)
    p0.push_back(geo_compare)
    dup_merge = DuplicateMerger(main_cfg["dedupe_config"]) 
    dup_merge.set_logger(logger)
    p0.push_back(dup_merge)

    pipelines2.add_pipeline(p0)
    pipelines2.add_pipeline(p1)

    pipelines2.broadcast_connect()

    merger2 = Merger({})
    merger2.set_logger(logger)
    merger2.set_source(pipelines2)

    merger2.pass_data().to_file(os.path.join(main_cfg["cache_dir"], "miscuglione3.json"), driver="GeoJSON")

    logger.info("Pipelines completed.")

if __name__ == "__main__":
    main()