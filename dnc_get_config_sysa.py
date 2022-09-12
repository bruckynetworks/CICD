"""
edit config, using just yaml files
"""

import os
import sys
from nornir import InitNornir
from nornir_netconf.plugins.tasks import netconf_edit_config
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result
from lxml import etree
from ruamel.yaml import YAML
from convertyamltoxml import yaml_conv


def edit_nc_config_from_yaml(task):
    with open(f"host_vars/{task.host}.yaml") as f:
        yaml = YAML(typ="safe")
        data = yaml.load(f)
        xml = yaml_conv.dict_to_xml(data, root="config")
        xml_str = etree.tostring(xml).decode("utf-8")
        result = task.run(task=netconf_edit_config, config=xml_str)
        return Result(host=task.host, result=result.result)


def main():
    config_file = sys.argv[1]
    nr = InitNornir(config_file=config_file)
    nr.inventory.defaults.username = os.getenv("USERNAME")
    nr.inventory.defaults.password = os.getenv("PASSWORD")    
    results = nr.run(task=edit_nc_config_from_yaml)
    print_result(results)


if __name__ == "__main__":
    main()
