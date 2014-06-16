Feature: Editing entries
    Edit buttons on list view page
    Edit page

    Scenario: List view edit buttons
        Given I am not logged in
        When I visit the URI '/'
        Then the response should not contain '<button type="submit"/>Edit'

    Scenario: Edit entry
        Given I am not logged in
        When I visit the URI '/edit/1'
        Then I should be redirected

    Scenario: List view edit buttons (Logged in)
        Given I am logged in
        When I visit the URI '/'
        Then the response should contain '<button type="submit"/>Edit'

    Scenario: Edit entry (Logged in)
        Given I am logged in
        When I visit the URI '/edit/1'
        Then the response should contain 'value="#This is a post"'

    Scenario: View entry with markdown
        When I visit the URI '/'
        Then the response should contain '<h1>This is a post'

    Scenario: View entry with code block formatting
        When I visit the URI '/'
        Then the response should contain '<code>with some code'
