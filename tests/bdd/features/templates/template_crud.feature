Feature: Template CRUD
  As a service admin
  I want to manage notification templates
  So that I can define message content

  Background:
    Given a platform admin user exists
    And a service exists

  Scenario: Create an email template
    When an "email" template is created with name "Email Template"
    Then the response status code should be 201
    And the response should contain the template details

  Scenario: Create an SMS template
    When an "sms" template is created with name "SMS Template"
    Then the response status code should be 201

  Scenario: Get a template by ID
    Given an "email" template exists
    When the template is retrieved by ID
    Then the response status code should be 200
    And the response should contain the template details

  Scenario: Get all templates for a service
    Given an "email" template exists
    When all templates are retrieved for the service
    Then the response status code should be 200
    And the response should contain a list of templates

  Scenario: Update a template
    Given an "email" template exists
    When the template name is updated to "Updated Template"
    Then the response status code should be 200
    And the response should contain the template name "Updated Template"

  Scenario: Get a specific template version
    Given an "email" template exists
    When the template version 1 is retrieved
    Then the response status code should be 200

  Scenario: Get all template versions
    Given an "email" template exists
    When all template versions are retrieved
    Then the response status code should be 200

  Scenario: Preview a template
    Given an "email" template exists
    When the template preview is requested
    Then the response status code should be 200
    And the response should contain the template body

  Scenario: Create a template with personalisation
    When an "email" template is created with personalisation
    Then the response status code should be 201

  Scenario: Update a template content
    Given an "email" template exists
    When the template content is updated
    Then the response status code should be 200

  Scenario: Cannot create a template with invalid type
    When a template is created with invalid type "fax"
    Then the response status code should be 400

  Scenario: Cannot create a template with empty name
    When a template is created with an empty name
    Then the response status code should be 400
