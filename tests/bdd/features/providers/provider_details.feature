Feature: Provider details
  As a platform admin
  I want to manage notification providers
  So that I can control how messages are sent

  Background:
    Given a platform admin user exists

  Scenario: Get all providers
    When all providers are retrieved
    Then the response status code should be 200
    And the response should contain a list of providers

  Scenario: Get a provider by ID
    When a provider is retrieved by ID
    Then the response status code should be 200
    And the response should contain the provider details

  Scenario: Get provider version history
    When the provider version history is retrieved
    Then the response status code should be 200

  Scenario: Update a provider priority
    When a provider priority is updated
    Then the response status code should be 200

  Scenario: Update a provider active status
    When a provider is set to inactive
    Then the response status code should be 200
