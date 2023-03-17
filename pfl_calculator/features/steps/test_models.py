from behave import *
from calculator_site.models import *
from django.contrib.auth.models import User

# Scenario: Test the user model
user = User.objects.create_user(username="test", password="testpass")

@given('we have some user')
def step_impl(context):
    assert user is not None


@when('we check that users username with a matching string')
def step_impl(context):
    assert (user.username == "test")

@then('the usernames will match')
def step_impl(context):
    assert context.failed != True

# Scenario: Test the business model
business, _ = Business.objects.get_or_create(user=user)

@given('we have a business object belonging to a user')
def step_impl(context):
    assert business is not None and business.user is not None


@when('we check what user owns that business')
def step_impl(context):
    assert business.user == user

@then('the users will match')
def step_impl(context):
    assert context.failed != True

# Scenario: Test the Carbon-Footprint model
cf, _ = CarbonFootprint.objects.get_or_create(id=999, year=2023, business=business)

@given('a Carbon-Footprint object')
def step_impl(context):
    assert cf is not None


@when('we check that it is owned by a business for a particular year')
def step_impl(context):
    assert cf.business is not None and cf.year is not None


@then('there will be no NULL fields')
def step_impl(context):
    for field in CarbonFootprint._meta.get_fields():
        assert (getattr(cf, field.name) is not None)
