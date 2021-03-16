from behave import *
from libs.nso import NsoLibs

use_step_matcher("re")


@given("Setup NSO Connection")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.nso = NsoLibs(hostname='192.168.20.60', un='root', pw='dvrlab')


@step("Verify Netconf device is installed (?P<device>.+)")
def step_impl(context, device):
    """
    :type context: behave.runner.Context
    """
    context.device = device
    device_list, error = context.nso.get_device_list()
    if context.device not in device_list:
        raise EnvironmentError(f'{context.device} netconf device is not installed')


@step("Disable Trace Logs")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    device_data, error = context.nso.get_device_dict(device_name=context.device)
    if device_data == {}:
        raise EnvironmentError(error["message"])

    if 'trace' in device_data['tailf-ncs:device'].keys():
        device_list, error = context.nso.remove_device_trace(device_name=context.device, xml_file='remove_trace.xml')
        if device_list is False:
            raise EnvironmentError(error["message"])


@step("Verify Cisco Netconf NED is installed (?P<ned>.+)")
def step_impl(context, ned):
    """
    :type context: behave.runner.Context
    """
    context.ned = ned
    pkg_list, error = context.nso.get_packages()
    if context.ned not in pkg_list:
        raise EnvironmentError(f'{context.ned} netconf ned is not installed')


@when("Configuration is submitted to NED (?P<config_xml>.+) (?P<config_path>.+)")
def step_impl(context, config_xml, config_path):
    """
    :type context: behave.runner.Context
    """
    result, error = context.nso.post_device_config(device_name=context.device, xml_file=config_xml, config_path=config_path)
    if result is False:
        raise ConnectionError(error['message'])


@then("Enable Trace Logs for Netconf Device")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    result, error = context.nso.install_device_trace(device_name=context.device, xml_file='set_trace.xml')
    if result is False:
        raise ConnectionError(error['message'])


@step("Sync From the Netconf Device")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    result, error = context.nso.sync_from_device(device_name=context.device)
    if result is False:
        raise ConnectionError(error['message'])


@step("Verify ios-xe interface configuration is seen in device CDB (?P<cdb_path>.+) (?P<ip>.+) (?P<netmask>.+)")
def step_impl(context, cdb_path, ip, netmask):
    """
    :type context: behave.runner.Context
    """
    device_data, error = context.nso.get_device_config_dict(device_name=context.device, path=cdb_path)
    if device_data == {}:
        raise LookupError(error['message'])

    if str(device_data['Cisco-IOS-XE-native:primary']['address']).lower() != str(ip).lower() or str(device_data['Cisco-IOS-XE-native:primary']['mask']).lower() != str(netmask).lower():
        raise LookupError('NED failed to save configuration in CDB')


@step("Verify ios-xe interface mtu is seen in device CDB (?P<path>.+) (?P<mtu>.+)")
def step_impl(context, path, mtu):
    """
    :type context: behave.runner.Context
    :type path: str
    :type mtu: str
    """
    device_data, error = context.nso.get_device_config_dict(device_name=context.device, path=path)
    if device_data == {}:
        raise LookupError(error['message'])

    if str(device_data['Cisco-IOS-XE-native:mtu']).lower() != str(mtu).lower():
        raise LookupError('NED failed to save configuration in CDB')
