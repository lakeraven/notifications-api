Feature: Billing usage
  As a platform admin
  I want to view billing data
  So that I can track service usage

  Background:
    Given a platform admin user exists
    And a service exists

  Scenario: Get monthly usage for a service
    When the monthly usage is retrieved for the current year
    Then the response status code should be 200

  Scenario: Get yearly usage summary
    When the yearly usage summary is retrieved
    Then the response status code should be 200

  Scenario: Get free SMS fragment limit
    When the free SMS fragment limit is retrieved
    Then the response status code should be 200

  Scenario: Set free SMS fragment limit
    When the free SMS fragment limit is set to 250000
    Then the response status code should be 201

  Scenario: Update free SMS fragment limit
    Given a free SMS fragment limit exists
    When the free SMS fragment limit is set to 100000
    Then the response status code should be 201
