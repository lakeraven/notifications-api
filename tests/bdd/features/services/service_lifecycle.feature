Feature: Service lifecycle
  As a platform admin
  I want to manage services
  So that teams can send notifications

  Background:
    Given a platform admin user exists

  Scenario: Create a new service
    When a new service "Test Service" is created
    Then the response status code should be 201
    And the response should contain the service details

  Scenario: Get a service by ID
    Given a service "My Service" exists
    When the service is retrieved by ID
    Then the response status code should be 200
    And the response should contain the service name "My Service"

  Scenario: Get all services
    Given a service "Service A" exists
    When all services are retrieved
    Then the response status code should be 200
    And the response should contain a list of services

  Scenario: Update a service
    Given a service exists
    When the service name is updated to "Updated Service"
    Then the response status code should be 200
    And the response should contain the service name "Updated Service"

  Scenario: Archive a service
    Given a service exists
    When the service is archived
    Then the response status code should be 204

  Scenario: Suspend a service
    Given a service exists
    When the service is suspended
    Then the response status code should be 204

  Scenario: Resume a suspended service
    Given a service exists
    And the service is suspended
    When the service is resumed
    Then the response status code should be 204

  Scenario: Get service history
    Given a service exists
    When the service history is retrieved
    Then the response status code should be 200
    And the response should contain service history data

  Scenario: Get service statistics
    Given a service exists
    When the service statistics are retrieved
    Then the response status code should be 200

  Scenario: Get service notification count
    Given a service exists
    When the service notification count is retrieved
    Then the response status code should be 200

  Scenario: Find services by name
    Given a service "Searchable Service" exists
    When services are searched by name "Searchable"
    Then the response status code should be 200
    And the response should contain the service name "Searchable Service"

  Scenario: Get live services data
    Given a service exists
    When live services data is retrieved
    Then the response status code should be 200

  Scenario: Get monthly data by service
    Given a service exists
    When monthly data by service is retrieved
    Then the response status code should be 200
