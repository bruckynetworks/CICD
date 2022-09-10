from nornir import InitNornir
from nornir_netconf.plugins.tasks import netconf_get_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="inventory/config.yaml")

def get_thing(task):
    task.run(task=netconf_get_config, source="running", filter_type="xpath", path="/native/router")

results = nr.run(task=get_thing)
print_result(results)
