Feature: Service callbacks
  As a service admin
  I want to manage callback URLs
  So that I can receive delivery notifications

  Background:
    Given a platform admin user exists
    And a service exists

  Scenario: Create a delivery receipt callback
    When a delivery receipt callback is created
    Then the response status code should be 201

  Scenario: Get a delivery receipt callback
    Given a delivery receipt callback exists
    When the delivery receipt callback is retrieved
    Then the response status code should be 200

  Scenario: Update a delivery receipt callback
    Given a delivery receipt callback exists
    When the delivery receipt callback URL is updated
    Then the response status code should be 200

  Scenario: Delete a delivery receipt callback
    Given a delivery receipt callback exists
    When the delivery receipt callback is deleted
    Then the response status code should be 204

  Scenario: Create an inbound API callback
    When an inbound API callback is created
    Then the response status code should be 201

  Scenario: Get an inbound API callback
    Given an inbound API callback exists
    When the inbound API callback is retrieved
    Then the response status code should be 200

  Scenario: Update an inbound API callback
    Given an inbound API callback exists
    When the inbound API callback URL is updated
    Then the response status code should be 200

  Scenario: Delete an inbound API callback
    Given an inbound API callback exists
    When the inbound API callback is deleted
    Then the response status code should be 204
