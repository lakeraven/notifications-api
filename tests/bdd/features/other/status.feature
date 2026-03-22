Feature: Platform status
  As an operator
  I want to check the platform status
  So that I know the system is healthy

  Scenario: Health check returns OK
    When a GET request is made to "/_status"
    Then the response status code should be 200

  Scenario: Root returns OK
    When a GET request is made to "/"
    Then the response status code should be 200

  Scenario: Live service and organization counts
    Given a service exists
    When a GET request is made to "/_status/live-service-and-organization-counts"
    Then the response status code should be 200
