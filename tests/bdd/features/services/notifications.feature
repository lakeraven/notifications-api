Feature: Service notifications
  As a service admin
  I want to manage notifications for a service
  So that I can track message delivery

  Background:
    Given a platform admin user exists
    And a service exists

  Scenario: Get notifications for a service
    Given the service has sent notifications
    When the service notifications are retrieved
    Then the response status code should be 200
    And the response should contain a list of notifications

  Scenario: Get notification by ID
    Given the service has sent a notification
    When the notification is retrieved by ID
    Then the response status code should be 200

  Scenario: Get notification count for a service
    Given the service has sent notifications
    When the service notification count is retrieved
    Then the response status code should be 200

  Scenario: Get monthly notification stats
    Given the service has sent notifications
    When the monthly notification stats are retrieved
    Then the response status code should be 200

  Scenario: Get notification statistics by type
    Given the service has sent notifications
    When notification statistics are retrieved for today
    Then the response status code should be 200

  Scenario: Get notifications returns empty list for new service
    When the service notifications are retrieved
    Then the response status code should be 200
    And the response should contain an empty notifications list
