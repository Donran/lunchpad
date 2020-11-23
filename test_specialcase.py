#!/usr/bin/python3
"""
 Tests the specialcase feature
"""
import os
import datetime
from lunchpad import *


def create_test_specialcases_file():
    """
    Creates the specialcases test file
    """
    data = ["MFR,Monday,Tuesday,Wednesday,Thursday,Friday\n",
            "***REMOVED***,10:00-14:00,,,,\n",
            "***REMOVED***,,,10:00-14:00,,\n"
        ]

    with open(SPECIALCASE_FILENAME, "w") as f:
        f.writeliens(data)

def test_tag_in_specialcase(tag, expected):
    """
    Tests for correct output if tag in specialcase
    """
    result = get_specialcase_times(tag, SPECIALCASE_FILENAME)
    if result == expected:
        print("TEST COMPLETE")
    else:
        print("TEST FAILED")


def test_specialcase(tag, date, expected):
    """
    Tests for correct output if tag in specialcase
    and correct weekday
    """
    res = handle_input(tag, tags, times, date, [], DATA_FILENAME, SPECIALCASE_FILENAME)
    if res == expected:
        print("TEST COMPLETE")
    else:
        print("TEST FAILED")



if __name__ == "__main__":
    DATA_FILENAME = "test_data.csv"
    SPECIALCASE_FILENAME = "test_specialcases.csv"
    PATH = os.path.dirname(os.path.realpath(__file__))
    tags = get_file_data(PATH+"/id_tester.csv")
    times = get_file_data(PATH+"/tider_tester.csv")

    TAGS_WITH_SPECIALCASE = ["***REMOVED***", "***REMOVED***"]
    NO_SPECIALCASE_TAG = "***REMOVED***"

    # Creates the specialcase test file
    create_test_specialcases_file()

    print("[*] Testing with tag in specialcase csv")
    test_tag_in_specialcase(TAGS_WITH_SPECIALCASE[0], ["Mån", "Tis", "Ons", "Tors", "Fre"])

    print("[*] Testing with tag not in specialcase csv")
    test_tag_in_specialcase(NO_SPECIALCASE_TAG, [])

    print("[*] Testing with tag with specialcase on monday at wrong time")
    expected_result = False, "DIN LUNCHTID ÄR 10:00-14:00"
    test_date = datetime.datetime(2020, 11, 23, 15, 10, 10)
    test_specialcase(TAGS_WITH_SPECIALCASE[0], test_date, expected_result)

    print("[*] Testing with tag with specialcase on wednesday at wrong time")
    expected_result = False, "DIN LUNCHTID ÄR 10:00-14:00"
    test_date = datetime.datetime(2020, 11, 25, 15, 10, 10)
    test_specialcase(TAGS_WITH_SPECIALCASE[1], test_date, expected_result)

    print("[*] Testing with tag with specialcase on monday at correct time")
    expected_result = True, "GODKÄND SKANNING! SMAKLING MÅLTID!"
    test_date = datetime.datetime(2020, 11, 23, 13, 10, 10)
    test_specialcase(TAGS_WITH_SPECIALCASE[0], test_date, expected_result)

    print("[*] Testing with tag with specialcase on wednesday at correct time")
    expected_result = True, "GODKÄND SKANNING! SMAKLING MÅLTID!"
    test_date = datetime.datetime(2020, 11, 25, 13, 10, 10)
    test_specialcase(TAGS_WITH_SPECIALCASE[1], test_date, expected_result)

    print("[*] Testing with tag without specialcase for tuesday")
    expected_result = False, "DIN LUNCHTID ÄR 12:30-12:50"
    test_date = datetime.datetime(2020, 11, 24, 13, 10, 10)
    test_specialcase(TAGS_WITH_SPECIALCASE[1], test_date, expected_result)

    # Removes the specialcase test file
    os.remove(SPECIALCASE_FILENAME)
