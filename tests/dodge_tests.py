from nose.tools import istest, assert_equal

import dodge


@istest
def error_if_constructor_has_extra_positional_argument():
    User = dodge.data_class("User", ["username"])
    try:
        User("bob", "password1")
        assert False, "Expected error"
    except TypeError as error:
        assert_equal("__init__ takes 2 positional arguments but 3 were given", str(error))
        
    Unit = dodge.data_class("Unit", [])
    try:
        Unit("bob")
        assert False, "Expected error"
    except TypeError as error:
        assert_equal("__init__ takes 1 positional argument but 2 were given", str(error))


@istest
def error_if_constructor_has_extra_keyword_argument():
    User = dodge.data_class("User", ["username"])
    try:
        User("bob", password="password1")
        assert False, "Expected error"
    except TypeError as error:
        assert_equal("User.__init__ does not take keyword argument 'password'", str(error))


@istest
def class_module_is_not_dodge():
    User = dodge.data_class("User", [])
    assert_equal("dodge_tests", User.__module__)


@istest
def data_class_arguments_can_be_passed_by_position_and_keyword():
    User = dodge.data_class("User", ["username", "salt", "password"])
    
    user = User("bob", "asf", password="password1")
    assert_equal("bob", user.username)
    assert_equal("password1", user.password)
    assert_equal("asf", user.salt)


@istest
def instances_of_data_class_are_equal_iff_all_fields_have_the_same_value():
    User = dodge.data_class("User", ["username", "password"])
    
    assert User("bob", "password1") == User("bob", "password1")
    assert not (User("jim", "password1") == User("bob", "password1"))
    assert not (User("bob", "password1") == User("bob", "password2"))
    assert not (User("jim", "password1") == User("bob", "password2"))


@istest
def instances_of_data_class_are_not_equal_iff_any_fields_have_different_values():
    User = dodge.data_class("User", ["username", "password"])
    
    assert not (User("bob", "password1") != User("bob", "password1"))
    assert User("jim", "password1") != User("bob", "password1")
    assert User("bob", "password1") != User("bob", "password2")
    assert User("jim", "password1") != User("bob", "password2")


@istest
def instances_of_data_class_are_not_equal_to_other_types():
    User = dodge.data_class("User", ["username", "password"])
    
    assert not (User("bob", "password1") == "bob")
    assert not ("bob" == User("bob", "password1"))
    assert User("bob", "password1") != "bob"
    assert "bob" != User("bob", "password1")


@istest
def can_convert_data_classes_with_non_string_fields_to_representation():
    Prime = dodge.data_class("Prime", ["index", "value"])
    
    assert_equal("Prime(0, 2)", repr(Prime(0, 2)))


@istest
def error_is_raised_if_fields_have_duplicate_names():
    assert_raises_regexp(
        ValueError, "^duplicate field name: 'username'$",
        lambda: dodge.data_class("User", ["username", "username"])
    )


@istest
def copying_data_class_creates_distinct_object_with_same_field_values():
    User = dodge.data_class("User", ["username", "password"])
    
    original = User("bob", "password1")
    copy = dodge.copy(original)
    
    assert original is not copy
    assert_equal("bob", copy.username)


@istest
def copy_of_data_object_has_values_changed_to_copy_kwargs():
    User = dodge.data_class("User", ["username", "password"])
    
    original = User("bob", "password1")
    copy = dodge.copy(original, password="password2")
    
    assert original is not copy
    assert_equal("password1", original.password)
    assert_equal("password2", copy.password)


@istest
def error_is_raised_if_copy_kwarg_is_not_field():
    User = dodge.data_class("User", ["username", "password"])
    
    original = User("bob", "password1")
    assert_raises_regexp(
        TypeError, "__init__ does not take keyword argument",
        lambda: dodge.copy(original, salt="salty")
    )


@istest
def field_is_set_to_default_if_value_not_provided():
    User = dodge.data_class("User", [
        "username",
        dodge.field("password", default="password1")
    ])
    
    user = User("bob")
    assert_equal("password1", user.password)


@istest
def field_with_default_is_shown_as_kwarg():
    User = dodge.data_class("User", [
        "username",
        dodge.field("password", default="password1")
    ])
    
    user = User("bob", "password2")
    assert_equal("User('bob', password='password2')", repr(user))


@istest
def keyword_only_field_is_shown_as_kwarg():
    User = dodge.data_class("User", [
        "username",
        dodge.field("password", keyword_only=True)
    ])
    
    user = User("bob", password="password1")
    assert_equal("User('bob', password='password1')", repr(user))


@istest
def field_value_is_shown_if_it_has_default_value():
    User = dodge.data_class("User", [
        "username",
        dodge.field("password", default="password1")
    ])
    
    user = User("bob")
    assert_equal("User('bob', password='password1')", repr(user))


@istest
def field_can_be_configured_to_be_hidden_in_repr_if_it_has_default_value():
    User = dodge.data_class("User", [
        "username",
        dodge.field("password", default="password1", show_default=False)
    ])
    
    user = User("bob")
    assert_equal("User('bob')", repr(user))


@istest
def error_is_raised_if_kwarg_field_is_passed_as_positional_arg():
    User = dodge.data_class("User", [
        "username",
        dodge.field("password", keyword_only=True)
    ])
    
    assert_raises_regexp(
        TypeError, "takes 1 positional argument but 2 were given",
        lambda: User("bob", "password2")
    )


@istest
def error_is_raised_if_init_value_is_missing():
    User = dodge.data_class("User", ["username", "password"])
    
    assert_raises_regexp(
        TypeError, "^Missing argument: password$",
        lambda: User("bob")
    )


@istest
def error_is_raised_if_too_many_positional_arguments_are_passed_to_init():
    User = dodge.data_class("User", ["username", "password"])
    
    assert_raises_regexp(
        TypeError, r"takes 2 positional arguments but 3 were given",
        lambda: User("bob", "password1", "salty")
    )


@istest
def error_of_number_of_positional_arguments_uses_correct_singular_wording():
    assert_raises_regexp(
        TypeError, r"takes 1 positional argument but 2 were given",
        lambda: dodge.data_class("User", ["username"])("bob", "password1")
    )
    assert_raises_regexp(
        TypeError, r"takes 0 positional arguments but 1 was given",
        lambda: dodge.data_class("User", [])("bob")
    )


import sys
if sys.version_info[:2] <= (2, 6):
    import re
    def assert_raises_regexp(cls, regex, func):
        try:
            func()
            assert False, "Expected {0}".format(cls)
        except cls as error:
            assert re.search(regex, str(error)), "{0} does not match {1}".format(str(error), regex)
else:
    from nose.tools import assert_raises_regexp
