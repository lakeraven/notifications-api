Feature: Email branding
  As a platform admin
  I want to manage email branding
  So that emails have the correct look

  Background:
    Given a platform admin user exists

  Scenario: Get all email brandings
    When all email brandings are retrieved
    Then the response status code should be 200

  Scenario: Create an email branding
    When a new email branding "Test Brand" is created
    Then the response status code should be 201

  Scenario: Get an email branding by ID
    Given an email branding "My Brand" exists
    When the email branding is retrieved by ID
    Then the response status code should be 200
    And the response should contain the branding name "My Brand"

  Scenario: Update an email branding
    Given an email branding "Old Brand" exists
    When the email branding name is updated to "New Brand"
    Then the response status code should be 200

  Scenario: Create an email branding with logo
    When a new email branding is created with a logo
    Then the response status code should be 201

  Scenario: Get all email brandings includes custom brands
    Given an email branding "Custom Brand" exists
    When all email brandings are retrieved
    Then the response status code should be 200
    And the response should contain branding "Custom Brand"
