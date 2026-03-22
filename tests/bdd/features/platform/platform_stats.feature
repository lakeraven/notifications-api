Feature: Platform statistics
  As a platform admin
  I want to view platform-wide statistics
  So that I can monitor overall usage

  Background:
    Given a platform admin user exists

  Scenario: Get platform statistics
    Given a service exists
    When the platform statistics are retrieved
    Then the response status code should be 200

  Scenario: Get usage for all services
    Given a service exists
    When usage for all services is retrieved
    Then the response status code should be 200

  Scenario: Get data for billing report
    Given a service exists
    When data for the billing report is retrieved
    Then the response status code should be 200

  Scenario: Get daily volumes report
    Given a service exists
    When the daily volumes report is retrieved
    Then the response status code should be 200

  Scenario: Get volumes by service
    Given a service exists
    When volumes by service are retrieved
    Then the response status code should be 200
