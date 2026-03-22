Feature: Service users
  As a platform admin
  I want to manage users on a service
  So that I can control access

  Background:
    Given a platform admin user exists
    And a service exists

  Scenario: Get users for a service
    When the service users are retrieved
    Then the response status code should be 200
    And the response should contain a list of users

  Scenario: Add a user to a service
    Given a new user exists
    When the user is added to the service
    Then the response status code should be 204

  Scenario: Remove a user from a service
    Given a new user exists
    And the user is added to the service
    When the user is removed from the service
    Then the response status code should be 204
