import requests
from requests.auth import HTTPBasicAuth
import json
import os
import xmltodict


class NsoLibs:
    def __init__(self, hostname, un, pw):
        self.hostname = hostname
        self.un = un
        self.pw = pw

    def get_device_list(self):
        """
        return a list of devices from the nso cdb
        :return:
        """
        error = None
        device_list = []
        headers = {"Accept": "application/vnd.yang.collection+json"}
        r = requests.get(
            url=f'http://{self.hostname}:8080/api/running/devices/device',
            auth=HTTPBasicAuth(self.un, self.pw),
            headers=headers
        )
        if r.status_code == 200:
            response = json.loads(r.text)
            if len(response['collection']['tailf-ncs:device']) > 0:
                for _device in response['collection']['tailf-ncs:device']:
                    device_list.append(_device['name'])
        else:
            error = {
                'message': 'failed to retrieve device list'
            }
        return device_list, error

    def check_api_running(self):
        headers = {"Accept": "application/vnd.yang.datastore+json"}
        r = requests.get(
            url=f'http://{self.hostname}:8080/api/running/',
            auth=HTTPBasicAuth(self.un, self.pw),
            headers=headers
        )
        print(r.status_code)
        print(r.text)

    def get_device_dict(self, device_name):
        error = None
        headers = {"Accept": "application/vnd.yang.data+json"}
        r = requests.get(
            url=f'http://{self.hostname}:8080/api/running/devices/device/{device_name}',
            auth=HTTPBasicAuth(self.un, self.pw),
            headers=headers
        )
        if r.status_code != 200:
            error = {"message": "failed to get device data"}
            return {}, error
        else:
            return json.loads(r.text), error

    def check_api(self):
        headers = {"Accept": "application/vnd.yang.api+json"}
        r = requests.get(
            url=f'http://{self.hostname}:8080/api',
            auth=HTTPBasicAuth(self.un, self.pw),
            headers=headers
        )
        print(r.status_code)
        print(r.text)

    def check_api_operational(self):
        headers = {"Accept": "application/vnd.yang.datastore+json"}
        r = requests.get(
            url=f'http://{self.hostname}:8080/api/operational',
            auth=HTTPBasicAuth(self.un, self.pw),
            headers=headers
        )
        print(r.status_code)
        print(r.text)

    def get_packages(self):
        pkg_list = []
        error = None
        headers = {"Accept": "application/vnd.yang.data+json"}
        r = requests.get(
            url=f'http://{self.hostname}:8080/api/operational/packages',
            auth=HTTPBasicAuth(self.un, self.pw),
            headers=headers
        )
        if r.status_code == 200:
            response = json.loads(r.text)
            for _pkg in response['tailf-ncs:packages']['package']:
                pkg_list.append(_pkg['name'])
        else:
            error = {
                'message': 'failed to retrieve package list'
            }
        return pkg_list, error

    def reload_packages(self):
        error = None
        headers = {"Accept": "application/vnd.yang.data+json"}
        r = requests.post(
            url=f'http://{self.hostname}:8080/api/operational/packages/_operations/reload',
            auth=HTTPBasicAuth(self.un, self.pw),
            headers=headers
        )
        if r.status_code == 200:
            response = json.loads(r.text)
            for _result in response['tailf-ncs:output']['reload-result']:
                if _result['result'] != 'true':
                    error = {f"message': f'failed to reload package: {_result['package']}"}
                    return False, error
        return True, error

    def post_device_config(self, device_name, xml_file, config_path):
        print(os.getcwd())
        error = None
        path = f'C:/Users/steph/Documents/behave/xml/{xml_file}'
        with open(path) as file:
            xml_data = xmltodict.parse(file.read())

        payload = xmltodict.unparse(xml_data)
        headers = {"Accept": "application/vnd.yang.datastore+xml"}
        r = requests.patch(
            url=f'http://{self.hostname}:8080/api/running/devices/device/{device_name}/config/{config_path}',
            auth=HTTPBasicAuth(self.un, self.pw),
            headers=headers,
            data=payload
        )

        if r.status_code != 204:
            error = {'message': 'failed to post configuration'}
            return False, error
        else:
            return True, error

    def remove_device_trace(self, device_name, xml_file):
        error = None
        path = f'C:/Users/steph/Documents/behave/xml/{xml_file}'
        with open(path) as file:
            xml_data = xmltodict.parse(file.read())

        payload = xmltodict.unparse(xml_data)
        headers = {"Accept": "application/vnd.yang.data+json"}
        r = requests.patch(
            url=f'http://{self.hostname}:8080/api/running/devices/device/{device_name}/trace',
            auth=HTTPBasicAuth(self.un, self.pw),
            headers=headers,
            data=payload
        )
        if r.status_code != 204:
            error = {"message": f"failed to remove device trace: {device_name}"}
            return False, error
        else:
            return True, error

    def install_device_trace(self, device_name, xml_file):
        error = None
        path = f'C:/Users/steph/Documents/behave/xml/{xml_file}'
        with open(path) as file:
            xml_data = xmltodict.parse(file.read())

        payload = xmltodict.unparse(xml_data)
        headers = {"Accept": "application/vnd.yang.data+json"}
        r = requests.put(
            url=f'http://{self.hostname}:8080/api/running/devices/device/{device_name}/trace',
            auth=HTTPBasicAuth(self.un, self.pw),
            headers=headers,
            data=payload
        )
        if r.status_code != 204:
            error = {"message": f"failed to install device trace: {device_name}"}
            return False, error
        else:
            return True, error

    def sync_from_device(self, device_name):
        error = None
        headers = {"Accept": "application/vnd.yang.data+json"}
        r = requests.post(
            url=f'http://{self.hostname}:8080/api/running/devices/device/{device_name}/_operations/sync-from',
            auth=HTTPBasicAuth(self.un, self.pw),
            headers=headers
        )
        if r.status_code != 200:
            error = {"message": f"failed to sync from device: {device_name}"}
            return False, error
        else:
            response = json.loads(r.text)
            if str(response['tailf-ncs:output']['result']).lower() != 'true':
                error = {"message": f"failed to sync from device: {device_name}"}
                return False, error
            else:
                return True, error

    def get_device_config_dict(self, device_name, path):
        error = None
        headers = {"Accept": "application/vnd.yang.data+json"}
        r = requests.get(
            url=f'http://{self.hostname}:8080/api/running/devices/device/{device_name}{path}',
            auth=HTTPBasicAuth(self.un, self.pw),
            headers=headers
        )
        if r.status_code != 200:
            error = {"message": "failed to get device data"}
            return {}, error
        else:
            return json.loads(r.text), error

if __name__ == '__main__':
    nso = NsoLibs(hostname='192.168.20.60', un='root', pw='dvrlab')
    """
    get device list
    device_list, error = nso.get_device_list()
    print(f'device_list: {device_list}')
    print(f'error: {error}')

    get package list
    pkg_list, error = nso.get_packages()
    print(f'pkg _list: {pkg_list}')
    print(f'error: {error}')
    
    result, error = nso.post_cisco_interface_config(device_name='csr1000v', xml_file='interface_config.xml')
    """
    # nso.install_device_trace(device_name='csr1000v', xml_file='set_trace.xml')
    device_data, error = nso.post_device_config(device_name='csr1000v', config_path='ios:native/interface/', xml_file='mtu_config.xml')
    print(device_data)
