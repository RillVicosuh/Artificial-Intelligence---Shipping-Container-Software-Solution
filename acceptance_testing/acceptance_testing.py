from unittest import TestCase
from container_load_balance import *
import numpy as np
import random

def generate_random_manifest():
    test_array = np.empty([8, 12], dtype='object')

    for i in range(8):
        for j in range(12):
            test_array[i][j] = ["UNUSED", 0]

    for i in range(7,0,-1):
        for j in range(12):
            if random.random() >= 0.25:
                if i == 7:
                    test_array[i][j] = [f"Container{i}{j}",(i+1)*(j+1)*random.random()]
                else:
                    if test_array[i+1][j] != ["UNUSED",0]:
                        test_array[i][j] = [f"Container{i}{j}", (i+1) * (j+1) * random.random()]

    return test_array

def generate_random_manifest_with_duplicates():
    test_array = np.empty([8, 12], dtype='object')

    for i in range(8):
        for j in range(12):
            test_array[i][j] = ["UNUSED", 0]

    for i in range(7,0,-1):
        for j in range(12):
            if random.random() >= 0.25:
                if i == 7:
                    test_array[i][j] = [f"Container{i}{j}",(i+1)*(j+1)*random.random()]
                else:
                    if test_array[i+1][j] != ["UNUSED",0]:
                        test_array[i][j] = [f"Container{i}{j}", (i+1) * (j+1) * random.random()]

    return test_array


class TestShipCases(TestCase):
    #Before testing out the other functions, we need to test that manifest_init is working so we can compare manifest files
    def test_sift(self):

        sift_count = 0

        for i in range(100):
                test_array = generate_random_manifest()
                balanced_array = balance_ship(test_array)

                if isinstance(balanced_array, tuple):
                    sift_count += 1

        self.assertLessEqual(sift_count,1, f"Sift count is {sift_count}")

    def test_balance(self):
        unbalance_count = 0

        for i in range(100):
                test_array = generate_random_manifest()
                balance_array = balance_ship(test_array)

                if check_if_ship_is_unbalanced(balance_array):
                    unbalance_count += 1

        self.assertLess(unbalance_count,1, f"Found {unbalance_count} unbalanced ships")

    def test_outbound_file(self):
        wrong_ship_config_count = 0

        for i in range(100):
            test_array = generate_random_manifest()
            load_array = load(test_array, "Name", 123)

            write_new_manifest("testmanifest.txt", load_array)
            manifest_loaded_array = manifest_init("testmanifest.txt")

            if not np.array_equal(load_array, manifest_loaded_array):
                wrong_ship_config_count += 1

        self.assertLess(wrong_ship_config_count, 1, f"Found {wrong_ship_config_count} wrong manifest files" )

    def test_duplicate_manifest_file(self):
        wrong_ship_config_count = 0

        for i in range(100):
            test_array = generate_random_manifest_with_duplicates()
            load_array = load(test_array, "Name", 123)

            write_new_manifest("testmanifest.txt", load_array)
            manifest_loaded_array = manifest_init("testmanifest.txt")

            if not np.array_equal(load_array, manifest_loaded_array):
                wrong_ship_config_count += 1

        self.assertLess(wrong_ship_config_count, 1, f"Found {wrong_ship_config_count} wrong manifest files")