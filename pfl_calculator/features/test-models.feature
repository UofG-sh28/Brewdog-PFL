Feature: testing calculator's models

  Scenario: Test the user model
    Given we have some user
    When we check that users username with a matching string
    Then the usernames will match

  Scenario: Test the business model
    Given we have a business object belonging to a user
    When we check what user owns that business
    Then the users will match

  Scenario: Test the Carbon-Footprint model
    Given a Carbon-Footprint object
    When we check that it is owned by a business for a particular year
    Then there will be no NULL fields
