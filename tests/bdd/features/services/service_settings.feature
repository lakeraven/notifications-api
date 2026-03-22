Feature: Service settings
  As a platform admin
  I want to manage service settings
  So that services are configured correctly

  Background:
    Given a platform admin user exists
    And a service exists

  Scenario: Get email reply-to addresses
    When the email reply-to addresses are retrieved
    Then the response status code should be 200

  Scenario: Add an email reply-to address
    When an email reply-to address is added
    Then the response status code should be 201

  Scenario: Get a specific email reply-to address
    Given an email reply-to address exists
    When the email reply-to address is retrieved by ID
    Then the response status code should be 200

  Scenario: Update an email reply-to address
    Given an email reply-to address exists
    When the email reply-to address is updated
    Then the response status code should be 200

  Scenario: Get SMS senders
    When the SMS senders are retrieved
    Then the response status code should be 200

  Scenario: Add an SMS sender
    When an SMS sender is added
    Then the response status code should be 201

  Scenario: Get a specific SMS sender
    Given an SMS sender exists
    When the SMS sender is retrieved by ID
    Then the response status code should be 200

  Scenario: Update an SMS sender
    Given an SMS sender exists
    When the SMS sender is updated
    Then the response status code should be 200

  Scenario: Get the guest list
    When the guest list is retrieved
    Then the response status code should be 200

  Scenario: Update the guest list
    When the guest list is updated
    Then the response status code should be 204

  Scenario: Get data retention settings
    When the data retention settings are retrieved
    Then the response status code should be 200

  Scenario: Add data retention settings
    When data retention settings are added for email
    Then the response status code should be 201

  Scenario: Get a specific data retention setting
    Given data retention settings exist for email
    When the data retention setting is retrieved by ID
    Then the response status code should be 200

  Scenario: Update data retention settings
    Given data retention settings exist for email
    When the data retention setting is updated
    Then the response status code should be 200

  Scenario: Get service permissions
    When the service is retrieved by ID
    Then the response status code should be 200
    And the response should contain service permissions

  Scenario: Update service permissions
    When the service permissions are updated
    Then the response status code should be 200

  Scenario: Get organization for a service
    Given the service belongs to an organization
    When the service organization is retrieved
    Then the response status code should be 200
    And the response should contain organization details
