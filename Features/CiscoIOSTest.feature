# Created by tonyg at 3/15/2021
Feature: validate netconf configurations work

  Scenario Outline: IOS-XE Interface IP Configuration
    Given Setup NSO Connection
    And Verify Netconf device is installed <device>
    And Disable Trace Logs
    And Verify Cisco Netconf NED is installed <ned>
    When Configuration is submitted to NED <config_xml> <config_path>
    Then Enable Trace Logs for Netconf Device
    And Sync From the Netconf Device
    And Verify ios-xe interface configuration is seen in device CDB <cdb_path> <ip> <netmask>

    Examples:
      | device | ned | config_xml | config_path | cdb_path | ip | netmask |
      | csr1000v | cisco-iosxe-nc-1.0 | interface_config.xml | ios:native/interface/ | /config/ios:native/interface/GigabitEthernet/2/ip/address/primary | 1.1.1.1 | 255.255.255.0 |


  Scenario Outline: IOS-XE Interface MTU Configuration
    Given Setup NSO Connection
    And Verify Netconf device is installed <device>
    And Disable Trace Logs
    And Verify Cisco Netconf NED is installed <ned>
    When Configuration is submitted to NED <config_xml> <config_path>
    Then Enable Trace Logs for Netconf Device
    And Sync From the Netconf Device
    And Verify ios-xe interface mtu is seen in device CDB <cdb_path> <mtu>

    Examples:
      | device | ned | config_xml | config_path | cdb_path | mtu |
      | csr1000v | cisco-iosxe-nc-1.0 | mtu_config.xml | ios:native/interface/ | /config/ios:native/interface/GigabitEthernet/2/mtu | 1500 |
