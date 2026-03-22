Feature: API keys
  As a service admin
  I want to manage API keys
  So that I can authenticate API calls

  Background:
    Given a platform admin user exists
    And a service exists

  Scenario: Create a normal API key
    When a "normal" API key is created for the service
    Then the response status code should be 201
    And the response should contain the API key data

  Scenario: Create a team API key
    When a "team" API key is created for the service
    Then the response status code should be 201

  Scenario: Create a test API key
    When a "test" API key is created for the service
    Then the response status code should be 201

  Scenario: Get all API keys for a service
    Given the service has a "normal" API key
    When all API keys are retrieved for the service
    Then the response status code should be 200
    And the response should contain a list of API keys

  Scenario: Get a specific API key
    Given the service has a "normal" API key
    When the API key is retrieved by ID
    Then the response status code should be 200

  Scenario: Revoke an API key
    Given the service has a "normal" API key
    When the API key is revoked
    Then the response status code should be 202

  Scenario: Cannot use a revoked API key
    Given the service has a "normal" API key
    And the API key is revoked
    When the revoked API key is used to access the service
    Then the response status code should be 404
