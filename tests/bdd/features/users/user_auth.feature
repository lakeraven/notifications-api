Feature: User authentication
  As a user
  I want to authenticate
  So that I can access the platform securely

  Background:
    Given a platform admin user exists

  Scenario: Verify user password
    Given a user exists
    When the user's password is verified
    Then the response status code should be 204

  Scenario: Verify user password fails with wrong password
    Given a user exists
    When an incorrect password is verified
    Then the response status code should be 400

  Scenario: Request SMS verification code
    Given a user exists
    When an SMS verification code is requested
    Then the response status code should be 204

  Scenario: Request email verification code
    Given a user exists
    When an email verification code is requested
    Then the response status code should be 204

  Scenario: Verify SMS code
    Given a user exists
    And an SMS verification code has been sent
    When the SMS code is verified
    Then the response status code should be 204

  Scenario: Verify SMS code fails with wrong code
    Given a user exists
    When a wrong SMS code is verified
    Then the response status code should be 404

  Scenario: Reset failed login count
    Given a user exists
    When the user's failed login count is reset
    Then the response status code should be 200

  Scenario: Get user by email
    Given a user exists
    When the user is retrieved by email
    Then the response status code should be 200

  Scenario: Get user by email not found
    When a nonexistent user is retrieved by email
    Then the response status code should be 404

  Scenario: Activate a user
    Given a user exists
    When the user is activated
    Then the response status code should be 200

  Scenario: Deactivate a user
    Given a user exists
    When the user is deactivated
    Then the response status code should be 200

  Scenario: Send email verification
    Given a user exists
    When an email verification is sent
    Then the response status code should be 204
