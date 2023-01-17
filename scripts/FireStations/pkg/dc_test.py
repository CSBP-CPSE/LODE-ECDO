import json, os

from data_collectors import DataCollectorFactory

with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as f:
    cfg = json.loads(f.read())
    #print(cfg)

    # instantiate factory
    fact = DataCollectorFactory()

    for c in cfg:
        # skip data if it already exists:
        out_path = r"I:\DEIL\Data\Prod\Projects\DEIL_ISC\4-Collection\Fire Protection Services\lode-v3\collection"
        out_file = "%(area)s_fd.%(data_type)s" % c

        if os.path.exists(os.path.join(out_path, out_file)):
            continue

        dc = fact.get_data_collector(c)

        if dc.get_data():
            dc.set_output_dir(out_path)
            dc.set_output_file(out_file)
            dc.save_data()



