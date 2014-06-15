Feature: Editing entries
    Edit buttons on list view page
    Edit page

    Scenario: List view edit buttons
        Given I am not logged in
        When I visit the URI /
        Then the page should not have edit buttons

    Scenario: Edit entry
        Given I am not logged in
        When I visit the URI /edit/1
        Then I should be redirected to /

    Scenario: List view edit buttons (Logged in)
        Given I am logged in
        When I visit the URI /edit/1
        Then the form on the page should contain the values in entry 1
        Then close the database connection

    Scenario: Edit entry (Logged in)
        Given I am logged in
        When I visit the URI /edit/1
        Then the form on the page should contain the values in entry 1
        Then close the database connection
