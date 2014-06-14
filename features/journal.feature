As a user, when I request /edit/entry_id, I see a web page where I can
edit the entry

Feature: URI Routing for /edit/entry_id
    Implement an edit page

    Scenario Outline: Edit entry
        Given I am logged in
        When I visit the URI /edit/0
        Then the form on the page should contain the values in entry 0