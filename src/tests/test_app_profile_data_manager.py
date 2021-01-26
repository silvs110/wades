import pytest


from paths import SAMPLE_APP_PROF_DATA_PATH, APP_PROF_DATA_DIR_PATH
from src.main.common.AppProfile import AppProfile
from src.main.common.AppProfileAttribute import AppProfileAttribute
from src.main.psHandler.AppProfileDataManager import AppProfileDataManager
from src.main.psHandler.ProcessHandler import ProcessHandler
from src.tests.test_helpers import check_app_profile_has_the_right_format

"""
Contains tests for AppProfileDataManager class

Functional tests:
* save_app_profiles()
* get_saved_profiles()
* get_saved_profiles_as_dict()

Input Validation tests:
* save_app_profiles()
* get_saved_profiles()
* get_saved_profiles_as_dict()
"""


# noinspection PyTypeChecker
def test_save_app_profiles_with_input_validation() -> None:
    """
    Test save_app_profiles() with input validation.
    Checks that an exception is thrown when an invalid input is provided.
    """
    # None input for app_profiles
    with pytest.raises(TypeError):
        AppProfileDataManager.save_app_profiles(app_profiles=None)

    # Empty string input for app_profiles
    with pytest.raises(TypeError):
        AppProfileDataManager.save_app_profiles(app_profiles="")

    # Invalid elements in list as input for app_profiles
    with pytest.raises(TypeError):
        AppProfileDataManager.save_app_profiles(app_profiles=["!2", "error"])

    with pytest.raises(TypeError):
        AppProfileDataManager.save_app_profiles(app_profiles=[2, 7])

    # None input for app_profile_file
    with pytest.raises(TypeError):
        AppProfileDataManager.save_app_profiles(app_profiles=list(), app_profile_file=None)

    # Invalid input type for app_profile_file
    with pytest.raises(TypeError):
        AppProfileDataManager.save_app_profiles(app_profiles=list(), app_profile_file=5)


def test_save_and_get_profile_data() -> None:
    """
    Test save_app_profiles() and get_saved_profiles().
    Checks that saving and retrieving the app profiles does not modify the data.
    """
    file_path_to_use = APP_PROF_DATA_DIR_PATH.absolute() / "app_data_manager_test.csv"

    process_handler = ProcessHandler()
    process_handler.collect_running_processes_information()
    actual_app_profiles = process_handler.get_registered_app_profiles_list()

    AppProfileDataManager.save_app_profiles(app_profiles=actual_app_profiles, app_profile_file=file_path_to_use)
    expected_app_profiles = AppProfileDataManager.get_saved_profiles(app_profile_file=file_path_to_use)
    file_path_to_use.unlink()

    assert len(expected_app_profiles) == len(actual_app_profiles)

    for index in range(0, len(expected_app_profiles)):
        expected_app_profile = expected_app_profiles[index]
        actual_app_profile = actual_app_profiles[index]

        assert (isinstance(actual_app_profile, AppProfile) and isinstance(expected_app_profile, AppProfile))
        expected_app_profile_dict = expected_app_profile.dict_format()
        actual_app_profile_dict = actual_app_profile.dict_format()

        # Removing attributes which order doesn't matter (opened_files and usernames)
        expected_usernames = expected_app_profile_dict.pop(AppProfileAttribute.usernames.name)
        actual_usernames = actual_app_profile_dict.pop(AppProfileAttribute.usernames.name)
        assert set(expected_usernames) == set(actual_usernames)
        expected_opened_files = expected_app_profile_dict.pop(AppProfileAttribute.opened_files.name)
        actual_opened_files = actual_app_profile_dict.pop(AppProfileAttribute.opened_files.name)
        assert expected_opened_files == actual_opened_files

        assert expected_app_profile_dict == actual_app_profile_dict


def test_get_app_profile_as_dict_with_valid_input() -> None:
    """
    Test get_saved_profiles_as_dict().
    Checks that get_saved_profiles_as_dict() can retrieve app_profiles as dict in the right format.
    """
    app_name = "common_case_app"
    app_profiles = AppProfileDataManager.get_saved_profiles_as_dict(SAMPLE_APP_PROF_DATA_PATH)
    app_profile_attribute_names = {enum.name for enum in AppProfileAttribute}

    assert isinstance(app_profiles, dict)
    assert len(app_profiles) > 0

    app_profile = app_profiles[app_name]
    actual_app_profile_attrs = app_profile.keys()
    assert actual_app_profile_attrs == app_profile_attribute_names

    check_app_profile_has_the_right_format(app_name, app_profile)


# noinspection PyTypeChecker
def test_get_app_profile_as_dict_with_invalid_input() -> None:
    """
    Test get_saved_profiles_as_dict() with invalid inputs.
    Checks that an exception is thrown when an invalid input is provided.
    """
    # None input for app_profile_file
    with pytest.raises(TypeError):
        AppProfileDataManager.get_saved_profiles_as_dict(app_profile_file=None)

    # Invalid input type for app_profile_file
    with pytest.raises(TypeError):
        AppProfileDataManager.get_saved_profiles_as_dict(app_profile_file=5)


# noinspection PyTypeChecker
def test_get_app_profile_with_invalid_input() -> None:
    """
    Test get_saved_profiles() with invalid inputs.
    Checks that an exception is thrown when an invalid input is provided.
    """
    # None input for app_profile_file
    with pytest.raises(TypeError):
        AppProfileDataManager.get_saved_profiles(app_profile_file=None)

    # Invalid input type for app_profile_file
    with pytest.raises(TypeError):
        AppProfileDataManager.get_saved_profiles(app_profile_file=5)
