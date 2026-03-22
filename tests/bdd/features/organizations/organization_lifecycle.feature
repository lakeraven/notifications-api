Feature: Organization lifecycle
  As a platform admin
  I want to manage organizations
  So that services can be grouped

  Background:
    Given a platform admin user exists

  Scenario: Create an organization
    When a new organization "Test Org" is created
    Then the response status code should be 201
    And the response should contain the organization details

  Scenario: Get an organization by ID
    Given an organization "My Org" exists
    When the organization is retrieved by ID
    Then the response status code should be 200
    And the response should contain the organization name "My Org"

  Scenario: Get all organizations
    Given an organization "Org A" exists
    When all organizations are retrieved
    Then the response status code should be 200
    And the response should contain a list of organizations

  Scenario: Update an organization
    Given an organization "Old Name" exists
    When the organization name is updated to "New Name"
    Then the response status code should be 204

  Scenario: Get services for an organization
    Given an organization "Service Org" exists
    And a service belongs to the organization
    When the organization's services are retrieved
    Then the response status code should be 200

  Scenario: Link a service to an organization
    Given an organization "Link Org" exists
    And a service exists
    When the service is linked to the organization
    Then the response status code should be 204

  Scenario: Get organization by domain
    Given an organization "Domain Org" exists with domain "example.gov.uk"
    When an organization is looked up by domain "example.gov.uk"
    Then the response status code should be 200
