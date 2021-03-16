from behave import *
from libs.nso import get_device_list

use_step_matcher("re")


@given("NSO is setup in a default state")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given NSO is setup in a default state')