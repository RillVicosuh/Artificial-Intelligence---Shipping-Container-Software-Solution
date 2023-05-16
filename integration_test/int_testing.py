from unittest import TestCase
from container_load_balance import *
import numpy as np

case_number = 5


class TestShipCases(TestCase):
    #Before testing out the other functions, we need to test that manifest_init is working so we can compare manifest files
    def test_manifest_to_array(self):
        array_from_file = manifest_init(f"test_cases/ShipCase1/ShipCase1.txt")
        generated_array = np.empty([8, 12], dtype='object')
        for i in range(8):
            for j in range(12):
                generated_array[i][j] = ["UNUSED", 0]

        generated_array[7][0] = ["NAN", 0]
        generated_array[7][1] = ["Cat", 99]
        generated_array[7][2] = ["Dog", 100]
        generated_array[7][11] = ["NAN", 0]

        self.assertTrue(np.array_equal(array_from_file,generated_array))

    def test_balance(self):
        array_from_file = manifest_init(f"test_cases/ShipCase{case_number}/ShipCase{case_number}.txt")
        balanced_ship = balance_ship(array_from_file)

        if isinstance(balanced_ship, tuple):
            balanced_ship = balanced_ship[0]
        else:
            for i in range(8):
                for j in range(12):
                    balanced_ship[i][j] = balanced_ship[i][j][:2]

        balance_ship_from_file = manifest_init(f"test_cases/ShipCase{case_number}/ShipCase{case_number}BALANCE.txt")

        self.assertTrue(np.array_equal(balanced_ship, balance_ship_from_file))

    def test_load(self):
        array_from_file = manifest_init(f"test_cases/ShipCase{case_number}/ShipCase{case_number}.txt")
        load_array, best_loc = load(array_from_file,"Test",123)

        load_array_from_file = manifest_init(f"test_cases/ShipCase{case_number}/ShipCase{case_number}LOAD.txt")

        self.assertTrue(np.array_equal(load_array, load_array_from_file))

    def test_unload(self):
        #Each test file has "Dog" in it
        array_from_file = manifest_init(f"test_cases/ShipCase{case_number}/ShipCase{case_number}.txt")
        unload_array = unload(array_from_file, "Dog")

        unload_array_from_file = manifest_init(f"test_cases/ShipCase{case_number}/ShipCase{case_number}UNLOAD.txt")

        self.assertTrue(np.array_equal(unload_array, unload_array_from_file))