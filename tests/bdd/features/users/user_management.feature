Feature: User management
  As a platform admin
  I want to manage users
  So that I can control platform access

  Background:
    Given a platform admin user exists

  Scenario: Create a user
    When a new user is created with email "newuser@example.gov.uk"
    Then the response status code should be 201
    And the response should contain the user details

  Scenario: Get a user by ID
    Given a user exists
    When the user is retrieved by ID
    Then the response status code should be 200
    And the response should contain the user details

  Scenario: Get all users
    When all users are retrieved
    Then the response status code should be 200

  Scenario: Update a user
    Given a user exists
    When the user name is updated to "Updated Name"
    Then the response status code should be 200

  Scenario: Archive a user
    Given a user exists
    When the user is archived
    Then the response status code should be 204

  Scenario: Find users by email
    Given a user exists
    When users are searched by email
    Then the response status code should be 200

  Scenario: Get user's organizations and services
    Given a user exists
    When the user's organizations and services are retrieved
    Then the response status code should be 200

  Scenario: Get all users report
    When the all users report is retrieved
    Then the response status code should be 200
