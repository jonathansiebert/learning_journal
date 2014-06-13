As a user, when I request /edit/entry_id, I see a web page where I can
edit the entry

Feature: URI Routing for /edit/entry_id
    Implement an edit page

    Scenario Outline: Edit entry [just enough]
        Given an entry id <number>
        When I visit the URI /edit/<number>
        Then the form on the page should contain the values in entry <number>
        | number |
        | 0      |
        | 1      |
        | 2      |