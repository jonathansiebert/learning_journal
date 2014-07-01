# -*- coding: utf-8 -*-

import lettuce
import journal


@lettuce.step("I am not logged in")
def i_am_not_logged_in(step):
    with journal.app.test_client() as client:
        lettuce.world.client = client


@lettuce.step("I am logged in")
def i_am_logged_in(step):
    with journal.app.test_client() as client:
        with client.session_transaction() as sess:
            sess['logged_in'] = True
        lettuce.world.client = client


@lettuce.step("I visit the URI '(.*)'")
def i_visit_the_uri(step, a_string):
    lettuce.world.response = lettuce.world.client.get(a_string)


@lettuce.step("the response should not contain '(.*)'")
def the_response_should_not_contain(step, a_string):
    assert a_string not in lettuce.world.response.data


@lettuce.step("I should be redirected")
def i_should_be_redirected(step):
    assert lettuce.world.response.status_code // 100 == 3  # 300 code


@lettuce.step("the response should contain '(.*)'")
def the_response_should_contain(step, a_string):\
    assert a_string in lettuce.world.response.data
