Feature: Events
  As a platform admin
  I want to create events
  So that important actions are recorded

  Background:
    Given a platform admin user exists

  Scenario: Create an event
    When an event is created with type "sucessful_login"
    Then the response status code should be 201
