# AI-Migos Software - README for Ship Container Loading/Unloading and Balancing Software
## Project Description
This is a senior design project under the instruction of [Dr.Eamonn Keogh](https://www.cs.ucr.edu/~eamonn/) for the Winter 2023 Quarter at UCR. Here we are tasked with designing and implementing a software based solution to a shipping container problem. 

## Developers
* [Brandon Chea]
* [Anand Mahadevan]
* [David Tellez]
* [Ricardo Villacana]

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [How to Use](#how-to-use)
4. [Understanding the Code](#understanding-the-code)
5. [How To Run](#how-to-run)
6. [License](#license)

## Overview
This system is designed for managing container loading, unloading, and balancing operations in a cargo ship. This program contains a backend for the operations handling and a user-friendly frontend that interacts with this backend.

The software aids in managing the logistics of loading and unloading containers onto a ship, ensuring the weight distribution is balanced to meet safety regulations. The code provided is written in Python and is designed to handle the complex calculations and operations involved in these tasks.

## Prerequisites
- Python 3.6 or later.

## How to Use
This backend system provides an interface for loading, unloading, and balancing operations. It is designed to be used in tandem with a frontend user interface. The frontend will provide the inputs to the backend, and the backend will perform the necessary calculations and operations. 

The backend receives container data, processes it, and returns operations to execute for optimal load/unload and balance. It also writes logs for operations and issues, such as the inability to balance the ship.

## Understanding the Code
The system works with a 2D array representing the ship's container layout. Each cell in the array corresponds to a container with a name and a weight.

The main operations are:
1. **Loading**: The load() function receives a container's name and weight. It then finds the optimal location to place the container, which is determined by searching for the location with the least time required to insert the container. The estimated time for the load operation and the instructions for moving the container from the truck to the ship are printed out.
2. **Unloading**: The unload() function takes in the array representing the ship and the name of the container to unload. It records the unloading operation in a log file, then calls the move_c() function to move the container from its current location to the offloading area. This function returns the updated ship array, the coordinates of the container's path, and the total time taken for the unloading operation.
3. **Balancing**: `balance_ship()` function checks if the ship is balanced (no side is heavier than the other by more than 10%). If not, it attempts to rebalance by moving containers from the heavier side to the lighter side. If unable to balance within a certain time, it performs a SIFT operation, which involves moving all containers to a buffer zone and placing them back on the ship one by one, alternating between the two sides.

Helper functions assist in these operations. For example, `check_unbalance()` determines if the ship is unbalanced, `find_cell()` locates a container within the ship's array, `perform_sift()` executes the SIFT operation, and `move_c()` aids in moving a container from one location to another.

Absolutely, I'd be glad to help with that. Here's a simple "How To Run" guide that you can add to your README file:

---

## How To Run

This Python application includes a front-end graphical user interface (GUI) that interacts with a back-end process. To run the application, follow these steps:

### Prerequisites:

This application requires the tkinter library for the GUI. This is included with most Python installations, but if for some reason it isn't, you can install it using pip:

```bash
pip install tk
```

### Options to Run:

Option 1. **From Command Line:**
    - Open a terminal window or command prompt.
    
    - Navigate to the "src" directory with the command `cd path_to_src`. Replace "path_to_src" with the actual path to your "src" directory. For example, if your "src" directory is located at "/home/user/projects/src", the command would be `cd /home/user/projects/src`.
    
    - Run the "frontend_gui.py" file with the command `python frontend_gui.py` (you may need to use `python3` instead of `python` depending on your Python setup).

Option 2. **From an Integrated Development Environment (IDE):**
    - If you're using an IDE such as PyCharm or Visual Studio Code, you can open the "src" folder in your IDE.
    
    - Find the "frontend_gui.py" file in the file explorer of your IDE.
    
    - Right click on the "frontend_gui.py" file and choose the option to run the file.
    
 Please refer to the **Suggestions** section to see the video on how to follow along with the application.

---
## License
This project is licensed under the terms of the [MIT license](https://opensource.org/licenses/MIT).

## Suggestions
For a more complete illustration of the software, please refer to the Complete Project Report pdf file in this repository.
Here is the software running on sample data: https://www.youtube.com/watch?v=jZE7lWzeHM0 

