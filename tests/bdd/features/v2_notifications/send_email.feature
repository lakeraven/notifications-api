Feature: Send email notification via API
  As an API consumer
  I want to send email notifications
  So that I can communicate with users via email

  Background:
    Given a service with email permissions exists
    And the service has an email template with subject "Update" and content "Hello ((name))"
    And the service has a valid API key

  Scenario: Send a basic email notification
    When I send an email notification to "user@example.com" using the template
    Then the response status code should be 201
    And the response should contain a notification ID
    And the response content should include subject "Update"

  Scenario: Send an email with personalisation
    When I send an email notification to "user@example.com" with personalisation
    Then the response status code should be 201
    And the response body should contain "Hello Alice"

  Scenario: Send an email with a client reference
    When I send an email notification to "user@example.com" with reference "email-ref-456"
    Then the response status code should be 201
    And the response reference should be "email-ref-456"

  Scenario: Reject email with missing email address
    When I send an email notification without an email address
    Then the response status code should be 400
    And the response error should mention "email_address"

  Scenario: Reject email with invalid email address
    When I send an email notification to "not-an-email" using the template
    Then the response status code should be 400

  Scenario: Reject email when personalisation is missing
    When I send an email notification to "user@example.com" with empty personalisation
    Then the response status code should be 400

  Scenario: Send an email with a test API key
    Given the service has a test API key
    When I send an email notification to "user@example.com" using the test key
    Then the response status code should be 201

  Scenario: Schedule an email for future delivery
    When I send an email notification to "user@example.com" scheduled for tomorrow
    Then the response status code should be 201
    And the response scheduled_for should not be null
