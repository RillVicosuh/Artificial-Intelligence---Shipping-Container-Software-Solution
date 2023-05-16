from container_load_balance import log_file_init,log_file_change_user,log_file_enter_comment,manifest_init,write_new_manifest,load_unload_ship,balance_ship,check_unbalance
import unittest
from unittest import mock
from unittest import TestCase
import os  # for file size
import numpy as np # fast, efficient arrays, and calculations

class TestLogFileMethods(TestCase):
    # Log File init, restart working
    @mock.patch('container_load_balance.input', create=True)
    def test_log_file_init(self, mocked_input):
        mocked_input.side_effect = ['y']
        test_log_file = log_file_init()
        self.assertTrue(os.stat(test_log_file).st_size == 0)

    # Log File change user, test if user signs in
    @mock.patch('container_load_balance.input', create=True)
    def test_log_file_change_user(self, mocked_input):
        mocked_input.side_effect = ['Test User']
        test_file = log_file_change_user()
        last_line = ""
        test_file.seek(0)
        for line in test_file:
            pass
            last_line = line
        user_list = last_line.split()[4:6]
        test_user_name = " ".join(user_list)
        self.assertTrue(test_user_name == "Test User")

    # Log file enter comment, if comment registers
    @mock.patch('container_load_balance.input', create=True)
    def test_log_file_enter_comment(self, mocked_input):
        mocked_input.side_effect = ['abcdef']
        test_file = log_file_enter_comment()
        last_line = ""
        test_file.seek(0)
        for line in test_file:
            pass
            last_line = line
        user_list = last_line.split()[4:6]
        test_comment = " ".join(user_list)
        self.assertTrue(test_comment == "abcdef")

class TestManifestMethods(TestCase):
    # Manifest initialization, does manifest initialize correctly with input file
    @mock.patch('container_load_balance.input', create=True)
    def test_manifest_init(self, mocked_input):
        mocked_input.side_effect = ['ShipCaseEmpty.txt']
        test_file_name, test_arr = manifest_init()
        self.assertEqual(test_file_name, "ShipCaseEmptyOUTBOUND.txt")
        correct_arr = np.empty([8,12], dtype='object')
        for i in range(8):
            for j in range(12):
                correct_arr[i][j] = ["UNUSED", 0]
        self.assertTrue(np.array_equiv(test_arr, correct_arr))

    # Write new manifest, updated manifest after alterations made
    @mock.patch('container_load_balance.input', create=True)
    def test_write_new_manifest(self, mocked_input):
        test_f_to_write = "testOUTBOUND.txt"
        test_arr = np.empty([8,12], dtype='object')
        for i in range(8):
            for j in range(12):
                test_arr[i][j] = ["UNUSED", 0]
        test_arr[0][11] = ["Test", 123] # 8,12 last entry of manifest
        write_new_manifest(test_f_to_write, test_arr)
        last_line = ""
        f = open(test_f_to_write)
        for line in f:
            pass
            last_line = line
        self.assertTrue(last_line == "[08,12], {00123}, Test")

class TestLoadUnloadMethods(TestCase):
    # Load, test loading of a container
    @mock.patch('container_load_balance.input', create=True)
    def test_load_1(self, mocked_input):
        mocked_input.side_effect = ['Test',123]
        test_arr = np.empty([8,12], dtype='object')
        for i in range(8):
            for j in range(12):
                test_arr[i][j] = ["UNUSED", 0]
        test_op = "l"
        test_new_arr, test_time = load_unload_ship(test_arr, test_op)
        test_arr[7][0] = ["Test", 123]
        self.assertTrue(np.array_equiv(test_arr, test_new_arr))
        self.assertTrue(test_time == 9)

    # Load first column full
    @mock.patch('container_load_balance.input', create=True)
    def test_load_2(self, mocked_input):
        mocked_input.side_effect = ['Test',123]
        test_arr = np.empty([8,12], dtype='object')
        for i in range(8):
            for j in range(12):
                test_arr[i][j] = ["UNUSED", 0]
                if j == 0:
                    test_arr[i][j] = ["FULL", 100]
        test_op = "l"
        test_new_arr, test_time = load_unload_ship(test_arr, test_op)
        test_arr[7][1] = ["Test", 123]
        self.assertTrue(np.array_equiv(test_arr, test_new_arr))
        self.assertTrue(test_time == 10)
    
    # Load first column empty, second column almost full
    @mock.patch('container_load_balance.input', create=True)
    def test_load_3(self, mocked_input):
        mocked_input.side_effect = ['Test',123]
        test_arr = np.empty([8,12], dtype='object')
        for i in range(8):
            for j in range(12):
                test_arr[i][j] = ["UNUSED", 0]
                if j == 1 and i != 0:
                    test_arr[i][j] = ["FULL", 100]
        test_op = "l"
        test_new_arr, test_time = load_unload_ship(test_arr, test_op)
        test_arr[0][1] = ["Test", 123]
        self.assertTrue(np.array_equiv(test_arr, test_new_arr))
        self.assertTrue(test_time == 3)

    # Unload, test unloading of a container
    @mock.patch('container_load_balance.input', create=True)
    def test_unload_1(self, mocked_input):
        mocked_input.side_effect = ['Test']
        test_arr = np.empty([8,12], dtype='object')
        for i in range(8):
            for j in range(12):
                test_arr[i][j] = ["UNUSED", 0]
        unload_arr = test_arr
        test_arr[7][0] = ["Test", 123]
        test_op = "u"
        test_new_arr, test_time = load_unload_ship(test_arr, test_op)
        test_arr[7][0] = ["Test", 123]
        self.assertTrue(np.array_equiv(test_new_arr, unload_arr))
        self.assertTrue(test_time == 9)

    # Unload: with a container above the one to unload
    @mock.patch('container_load_balance.input', create=True)
    def test_unload_2(self, mocked_input):
        mocked_input.side_effect = ['Test']
        test_arr = np.empty([8,12], dtype='object')
        for i in range(8):
            for j in range(12):
                test_arr[i][j] = ["UNUSED", 0]
        test_arr[6][1] = ["ABOVE", 123]
        unload_arr = test_arr
        test_arr[7][0] = ["Test", 123]
        test_arr[6][0] = ["ABOVE", 123]
        test_op = "u"
        test_new_arr, test_time = load_unload_ship(test_arr, test_op)
        test_arr[7][0] = ["Test", 123]
        self.assertTrue(np.array_equiv(test_new_arr, unload_arr))
        print(test_time)
        self.assertTrue(test_time == 11)

    # Unload: Full Column above container to remove
    @mock.patch('container_load_balance.input', create=True)
    def test_unload_3(self, mocked_input):
        mocked_input.side_effect = ['Test']
        test_arr = np.empty([8,12], dtype='object')
        for i in range(8):
            for j in range(12):
                test_arr[i][j] = ["UNUSED", 0]
                if j == 3 and i != 0:
                    test_arr[i][j] = ["FULL"+str(i), 100]
        unload_arr = test_arr
        for i in range(8):
            for j in range(12):
                test_arr[i][j] = ["UNUSED", 0]
                if j == 4 and i != 7:
                    test_arr[i][j] = ["FULL"+str(i), 100]
        test_arr[7][4] = ["Test", 123]
        test_op = "u"
        test_new_arr, test_time = load_unload_ship(test_arr, test_op)
        test_arr[7][0] = ["Test", 123]
        self.assertTrue(np.array_equiv(test_new_arr, unload_arr))
        self.assertTrue(test_time == 45)

class TestBalanceMethods(TestCase):
    # check unbalance, formula to determine legal unbalancing
    def test_check_unbalance(self):
        self.assertTrue(check_unbalance(15,1000) == True)
        self.assertTrue(check_unbalance(10,20) == True)
        self.assertTrue(check_unbalance(20,20) == False)
        self.assertTrue(check_unbalance(35,20) == True)
        self.assertTrue(check_unbalance(0,0) == False)
        self.assertTrue(check_unbalance(99,110) == False)
        self.assertTrue(check_unbalance(98,110) == True)
        self.assertTrue(check_unbalance(99,111) == True)

    # Balance, test balancable ship
    def test_balance_1(self):
        test_arr = np.empty([8,12], dtype='object')
        for i in range(8):
            for j in range(12):
                test_arr[i][j] = ["UNUSED", 0]
        test_arr[7][0] = ["Alpha", 100]
        test_arr[7][1] = ["Beta", 90]
        test_new_arr, time_taken = balance_ship(test_arr)
        test_arr[7][0] = ["UNUSED", 0]
        test_arr[7][6] = ["Alpha", 100]
        self.assertTrue(np.array_equiv(test_new_arr, test_arr))
        self.assertTrue(time_taken == 8)

    # Balance: Larger weights
    def test_balance_2(self):
        test_arr = np.empty([8,12], dtype='object')
        for i in range(8):
            for j in range(12):
                test_arr[i][j] = ["UNUSED", 0]
        test_arr[7][0] = ["Alpha", 10000]
        test_arr[7][1] = ["Beta", 9000]
        test_new_arr, time_taken = balance_ship(test_arr)
        test_arr[7][0] = ["UNUSED", 0]
        test_arr[7][6] = ["Alpha", 10000]
        self.assertTrue(np.array_equiv(test_new_arr, test_arr))
        self.assertTrue(time_taken == 8)
        
    # Balance, test unbalancable ship to perform SIFT
    def test_unbalance_1(self):
        test_arr = np.empty([8,12], dtype='object')
        for i in range(8):
            for j in range(12):
                test_arr[i][j] = ["UNUSED", 0]
        test_arr[7][0] = ["Alpha", 100]
        test_arr[7][1] = ["Beta", 89] # 11% difference no matter what
        test_new_arr, time_taken = balance_ship(test_arr)
        test_arr[7][0] = ["UNUSED", 0]
        test_arr[7][1] = ["UNUSED", 0]
        test_arr[7][5] = ["Alpha", 100]
        test_arr[7][6] = ["Beta", 89] 
        print(time_taken)
        self.assertTrue(np.array_equiv(test_new_arr, test_arr))
        self.assertTrue(time_taken == 41)
    
    # Balance, test unbalancable ship to perform SIFT larger weight
    def test_unbalance_2(self):
        test_arr = np.empty([8,12], dtype='object')
        for i in range(8):
            for j in range(12):
                test_arr[i][j] = ["UNUSED", 0]
        test_arr[7][0] = ["Alpha", 10000]
        test_arr[7][1] = ["Beta", 8999] # 11% difference no matter what
        test_new_arr, time_taken = balance_ship(test_arr)
        test_arr[7][0] = ["UNUSED", 0]
        test_arr[7][1] = ["UNUSED", 0]
        test_arr[7][5] = ["Alpha", 10000]
        test_arr[7][6] = ["Beta", 8999] 
        print(time_taken)
        self.assertTrue(np.array_equiv(test_new_arr, test_arr))
        self.assertTrue(time_taken == 41)
        
unittest.main()