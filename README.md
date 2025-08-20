# Initialize Differential Machine

## 1. Introduce

A script for the *Differential Universe* of *Honkai: Star Rail*.

Designed to roll for a desired starting props combination (boon & equation).

*The original intention of developing this tool is not to undermine the game's roguelike element, but to enable a better and more convenient experience of the interesting combination developed by players.*

## 2. File Structure

```plaintext
InitializeDifferentialMechine/
├─ main.py 				# Program entry, execute the core logic
├─ requirements.txt 	# Project dependencies list
├─ README.md 			# Project documentation
├─ idm.log 				# Program runtime log file
└─ mypackage/ 			# Core function package
	├─ __init__.py 		# Package initialization file
	├─ operate.py 		# Encapsulation operation logic
	├─ recognize.py 	# Encapsulation recognize logic
	├─ exceptions.py 	# Custom exception class
	├─ utils.py 		# Utility functions
	└─ config.py 		# Configuration file
└─ interface_templates/ # Image files used by interface matching
└─ option_templates/ 	# Image files used by option matching
```

## 3. Instruction

### 3.1. Download Python

*Search by yourself.*

*Don't forget to install **pip** and add Python to the **system environment variables**.*

### 3.2. Launch Command

Press **Win+R**, type "**cmd**", then press **Ctrl+Shift+Enter**.

*The program uses functions from the **pywin32** library to implement mouse and keyboard operations, and these functions require **administrator privileges**.*

### 3.3. Preparation

1. Navigate to the project directory, e.g.:

    ```cmd
    cd c:
    cd C:\Users\...\Desktop\InitializeDifferentialMachine
    ```

2. Install dependencies:

	```cmd
	pip install -r requirements.txt
	# If downloading too slow, press Ctrl+C to interrupt
	# Then install using a domestic mirror source. For example:
	pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
	```

3. Open the game "Honkai: Star Rail", ensure the screen is in **1920×1080 fullscreen** mode, and the player has entered the **"Start Game" interface** in "Differentiated Universe".

### 3.4. Run the Program

Switch to the command window, and enter the following command to run the program:

```cmd
python mian.py
```

Enter the **Chinese Pinyin** names of the desired boon and equation successively.

*If you don’t know what you need, check the **file name (excluding extension)** of images in folder “**option_templates**” in project directory;*

*If you don’t know what you want, please read **Patr 4. Cases**.*

### 3.5. Completion

After the program finishes running, the game will stay on the equation's confirmation selection interface, where the player can continue operating.

*Alternatively, you can switch to the **command** window at any time and press **Ctrl+C** to forcefully terminate the program.*

## 4. Cases

Here are some of my personal favorite sharing about interesting combinations, along with their corresponding introduction videos:

- *Waiting for video creator to grant permission…*
