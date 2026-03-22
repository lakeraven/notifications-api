Feature: Send SMS notification via API
  As an API consumer
  I want to send SMS notifications
  So that I can communicate with users via text message

  Background:
    Given a service with SMS permissions exists
    And the service has an SMS template with content "Hello ((name)), your code is ((code))"
    And the service has a valid API key

  Scenario: Send a basic SMS notification
    When I send an SMS notification to "+447700900855" using the template
    Then the response status code should be 201
    And the response should contain a notification ID
    And the response should include template details
    And the response body should contain "Hello Test"
    And the response type should be "sms"

  Scenario: Send an SMS with personalisation
    When I send an SMS notification to "+447700900855" with personalisation
    Then the response status code should be 201
    And the response body should contain "Hello Jo"

  Scenario: Send an SMS with a client reference
    When I send an SMS notification to "+447700900855" with reference "my-ref-123"
    Then the response status code should be 201
    And the response reference should be "my-ref-123"

  Scenario: Send an SMS without a reference
    When I send an SMS notification to "+447700900855" without a reference
    Then the response status code should be 201
    And the response reference should be null

  Scenario: Reject SMS with missing phone number
    When I send an SMS notification without a phone number
    Then the response status code should be 400
    And the response error should mention "phone_number"

  Scenario: Reject SMS with missing template ID
    When I send an SMS notification to "+447700900855" without a template ID
    Then the response status code should be 400

  Scenario: Reject SMS with invalid template ID
    When I send an SMS notification to "+447700900855" with template ID "not-a-uuid"
    Then the response status code should be 400

  Scenario: Reject SMS when personalisation is missing
    When I send an SMS notification to "+447700900855" with empty personalisation
    Then the response status code should be 400

  Scenario: Reject SMS using another service's template
    Given another service exists with an SMS template
    When I send an SMS notification using the other service's template
    Then the response status code should be 400

  Scenario: Send an SMS with a test API key
    Given the service has a test API key
    When I send an SMS notification to "+447700900855" using the test key
    Then the response status code should be 201

  Scenario: Send an SMS with a team API key
    Given the service has a team API key
    When I send an SMS notification to "+447700900855" using the team key
    Then the response status code should be 201

  Scenario: Schedule an SMS for future delivery
    When I send an SMS notification to "+447700900855" scheduled for tomorrow
    Then the response status code should be 201
    And the response scheduled_for should not be null

  Scenario: Reject SMS scheduled too far in advance
    When I send an SMS notification to "+447700900855" scheduled for next year
    Then the response status code should be 400
