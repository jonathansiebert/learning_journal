# -*- coding: utf-8 -*-

from lettuce import *
import journal




def step_with_context(a_string, *args, **kwargs):
    def wrap(func):
        @step(a_string)
        def wrapped_func(*args):
            with journal.app.test_request_context('/'):
                func(*args, **kwargs)
                con = journal.get_database_connection()
                con.rollback()
        return wrapped_func
    return wrap


@step_with_context('I am not logged in')
def i_am_not_logged_in(step):
    journal.logout()


@step_with_context('I am logged in')
def i_am_logged_in(step):
    world.login_helper('admin', 'admin')


@step_with_context('I visit the URI')
def i_visit_the_uri(step):
    world.response = journal.app.test_client().get(step.multiline)


@step_with_context('the response should not contain')
def the_response_should_not_contain(step):
    assert step.multiline not in world.response.data


@step_with_context('I should be redirected')
def i_should_be_redirected(step):
    assert world.response.status_code // 100 == 3  # 300 code


@step_with_context('the response should contain')
def the_response_should_contain(step):
    import pdb;pdb.set_trace()
    assert step.multiline in world.response.data
