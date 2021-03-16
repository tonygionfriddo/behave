# Created by tonyg at 3/15/2021
Feature: validate cisco netconf ned works

  Scenario: configure an interface with the cisco netconf ned
    Given NSO is setup in a default state
    And Netconf device is installed
    And Cisco Netconf NED is installed
    When Configuration is submitted to NED
    Then Enable Trace Logs for Netconf Device
    And Sync From the Netconf Device
    And Verify intended configuration is seen in Sync From Trace