Feature: Complaints
  As a platform admin
  I want to view complaints
  So that I can monitor email issues

  Background:
    Given a platform admin user exists

  Scenario: Get all complaints
    Given a complaint exists
    When all complaints are retrieved
    Then the response status code should be 200
    And the response should contain a list of complaints

  Scenario: Get complaint count by date range
    Given a complaint exists
    When the complaint count is retrieved for today
    Then the response status code should be 200
