from nose.tools import istest, assert_equal, assert_raises_regexp

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
