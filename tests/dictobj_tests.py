from nose.tools import istest, assert_equal

import dodge


@istest
def conversion_from_dict_to_obj_uses_items_as_constructor_args():
    User = dodge.data_class("User", ["username", "password"])
    
    input_dict = {"username": "bob", "password": "password1"}
    converted_user = dodge.dict_to_obj(input_dict, User)
    
    expected_user = User("bob", "password1")
    assert_equal(expected_user, converted_user)


@istest
def arguments_with_camelcase_names_are_converted_to_use_underscores():
    User = dodge.data_class("User", ["is_root"])
    
    input_dict = {"isRoot": True}
    converted_user = dodge.dict_to_obj(input_dict, User)
    
    expected_user = User(is_root=True)
    assert_equal(expected_user, converted_user)


@istest
def unrecognised_fields_are_ignored():
    User = dodge.data_class("User", ["username"])
    
    input_dict = {"username": "bob", "password": "password1"}
    converted_user = dodge.dict_to_obj(input_dict, User)
    
    expected_user = User("bob")
    assert_equal(expected_user, converted_user)


@istest
def conversion_from_obj_to_dict_uses_hacktastic_fields_property():
    User = dodge.data_class("User", ["username", "password"])
    
    user = User("bob", "password1")
    result = dodge.obj_to_dict(user)
    
    expected_dict = {"username": "bob", "password": "password1"}
    assert_equal(expected_dict, result)


@istest
def conversion_from_obj_to_dict_converts_underscores_to_camel_case():
    User = dodge.data_class("User", ["is_root"])
    
    input_user = User(is_root=True)
    result = dodge.obj_to_dict(input_user)
    
    expected_dict = {"isRoot": True}
    assert_equal(expected_dict, result)


@istest
def converting_object_to_dict_preserves_ordering():
    User = dodge.data_class("User", [
        "username", "salt", "password", "email_address"
    ])
    
    user = User("bob", "!%ksdg", "password1", "bob@example.com")
    result = dodge.obj_to_dict(user)
    
    assert_equal(["username", "salt", "password", "emailAddress"], list(result.keys()))


@istest
def can_convert_nested_data_classes_to_and_from_dict():
    Profile = dodge.data_class("Profile", ["bio"])
    
    User = dodge.data_class("User", [
        "username",
        dodge.field("profile", type=Profile),
    ])
    
    user = User("bob", Profile("I'm Bob."))
    serialised_user = dodge.obj_to_dict(user)
    unserialised_user = dodge.dict_to_obj(serialised_user, User)
    assert_equal(user, unserialised_user)


@istest
def can_convert_data_classes_to_and_from_string():
    User = dodge.data_class("User", ["username", "password"])
    
    user = User("bob", "password1")
    serialised_user = dodge.dumps(user)
    unserialised_user = dodge.loads(serialised_user, User)
    
    expected_user = User("bob", "password1")
    assert_equal(unserialised_user, expected_user)



@istest
def can_convert_nested_data_classes_to_and_from_string():
    Profile = dodge.data_class("Profile", ["bio"])
    
    User = dodge.data_class("User", [
        "username",
        dodge.field("profile", type=Profile),
    ])
    
    user = User("bob", Profile("I'm Bob."))
    serialised_user = dodge.dumps(user)
    unserialised_user = dodge.loads(serialised_user, User)
    assert_equal(user, unserialised_user)
    

@istest
def can_convert_data_classes_to_and_from_flat_list():
    User = dodge.data_class("User", ["username", "password"])
    
    user = User("bob", "password1")
    serialised_user = dodge.obj_to_flat_list(user)
    unserialised_user = dodge.flat_list_to_obj(serialised_user, User)
    
    expected_user = User("bob", "password1")
    assert_equal(unserialised_user, expected_user)


@istest
def can_convert_nested_data_classes_to_and_from_flat_list():
    Profile = dodge.data_class("Profile", ["bio"])
    
    User = dodge.data_class("User", [
        "username",
        dodge.field("profile", type=Profile),
    ])
    
    user = User("bob", Profile("I'm Bob."))
    serialised_user = dodge.obj_to_flat_list(user)
    unserialised_user = dodge.flat_list_to_obj(serialised_user, User)
    assert_equal(user, unserialised_user)


@istest
def flat_list_for_nested_data_classes_contains_all_field_values_as_flat_list():
    Profile = dodge.data_class("Profile", ["bio"])
    
    User = dodge.data_class("User", [
        "username",
        dodge.field("profile", type=Profile),
    ])
    
    user = User("bob", Profile("I'm Bob."))
    
    assert_equal(["bob", "I'm Bob."], dodge.obj_to_flat_list(user))


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
