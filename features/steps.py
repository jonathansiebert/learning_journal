# -*- coding: utf-8 -*-

from lettuce import *
import journal


def step_with_context(func, str):
    @step(str)
    def with_context(step):
        with app.test_request_context('/'):
            func(step)
            con = get_database_connection()
            con.rollback()
    return with_context


@step_with_context('I am not logged in')
def i_am_not_logged_in():
    journal.logout()


@step_with_context('I am logged in')
def i_am_logged_in():
    world.login_helper('admin', 'admin')


@step_with_context('I visit the URI (\w+)')
def i_visit_the_uri(uri):
    world.response = client.get(uri)


@step_with_context('the response should not contain')
def the_response_should_contain(step)

"""
    Scenario: List view edit buttons
        Given I am not logged in
        When I visit the URI /
        Then the response should not contain edit buttons

    Scenario: Edit entry
        Given I am not logged in
        When I visit the URI /edit/1
        Then I should be redirected to /

    Scenario: List view edit buttons (Logged in)
        Given I am logged in
        When I visit the URI /edit/1
        Then the response should contain edit buttons

    Scenario: Edit entry (Logged in)
        Given I am logged in
        When I visit the URI /edit/1
        Then the response should contain the values in entry 1
"""
