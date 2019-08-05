# REX
A pressure transducer calibration application.


What Is REX?
-------------

REX is a digital calibration aid for Aerojet Rocketdyne's metrology department. It
is a simple program capable of connecting to laboratory instruments, assisting
technicians through their calibration procedure, performing a linear regression on
the recorded data, providing a detailed analysis of the calibration results, and
logging all of the data into an accessible archive called the property manager.

This software is dedicated to Rex Gurney, whos legacy as head of Aerojet Rocketdyne's
Metrology Department has pioneered the techniques and procedures utilized in this
program.

REX was originally intended to be a complete replacement for the HP-85A Computer that
Rex used to code his original calibration programs. Due to time constraints, only his
pressure transducer calibration exists here.


How To Use REX
--------------------------

  1. Open REX by clicking the shortcut icon or EXE file.

  2. Ensure that your VISA (virtual instrument software architecture) is properly
  installed and configured before proceeding.

  3. When you are ready to perform a calibration, click New Calibration, and then
  select your calibration of choice.

  4. Follow the REX Calibration Assistant through all of the steps.

  5. When the calibration is finished, click the Finish button in the bottom right.

  6. REX will display an analysis of your calibration on the screen. At this point,
  you can either:

	- Take a screenshot of the results which will then save to a dedicated
	  screenshots folder, or
	- Exit out of the analysis screen and access the results later from the
  	  REX Property Manager.



How To Install REX
-----------------------


- REX Calibration Assistant

There are two methods to begin using REX on your computer:

Method 1 - RECOMMENDED: copy and paste a shortcut to REX to your computer from the
public folder on the drive. The shortcut file will be titled REX with
a blue polygonal logo. Paste it to your desired location for easy access.

Method 2 - For a more comprehensive install, you can move the REX folder with the
actual EXE file to your computer from the drive.

** It is still recommended to create a shortcut icon to REX once you've copied
the folder over, as the folder contains several dependencies and module
libraries REX uses to work properly. Simply find the REX.exe file, right click,
click create shortcut, and move the shortcut to your desired location. 


- VISA Resource Manager

REX requires a third-party software called a VISA (Virtual Instrument Software
Architecture) which is a standard for configuring, programming, and troubleshooting
instrumentation systems comprising of GPIB, VXI, PXI, Serial, Ethernet, and/or
USB interfaces. VISA provides the connective interface between the hardware and
REX.

The recommended VISA software for the Canoga Park metrology facility requires
the Keysight IO Libraries Suite:

	* https://www.keysight.com/en/pd-1985909/io-libraries-suite?cc=US&lc=eng

This is to interface with the Keysight GPIB located in the metrology department.

An installer for the Keysight IO Libraries Suite will be located in the same
location as the REX shortcut on the drive. You must first contact IT with a
software request to properly install it.

	NOTE: Keysight IO Libraries may require you to install or update your
	computer's .NET framework. The .NET Installer will be included in the
	same folder as the Keysight IO Libraries Suite Installer.

		This will require administrative privileges from IT as well.



Limitations
-----------------------

- Software

REX has been compiled from its source code to be usable on any PC running Windows
XP or above via its executable file, from its resource folder.

DO NOT move the REX.exe file from its REX resource folder, which contains all of
the modules, dependencies, and resources required for the .exe to run. If you wish
to have the program solely on your computer, first copy the entire resource folder
containing the .exe as-is to anywhere on your computer. REX will run as long as its
necessary files are within the same folder.

Unfortunately, due to limitations on compiling modules and libraries from Anaconda
2, the REX resource folder is quite large.



Further Development
-----------------------


- Running the Python Source Code

To edit and run the source code for REX, first download Anaconda 2 from your PC's
Software Center. Anaconda will download most of the Python libraries and modules
required to run the source code properly. This is only available from the software
center for Windows 10 users.

To download the additional modules needed (**Replace <PATH> with your given path**):

	>   cd /d C:\<PATH>\Anaconda2\Scripts
	>   conda install -c conda-forge pyvisa


	If you are having issues downloading PyVisa, you will have to create a
	virtual environment and install fresh modules. Input the following lines into
	the command prompt:

		>   conda update conda
		>   conda create -n rex python=2.7
		>   conda install -n rex pyqt
		>   conda install -n rex -c -conda-forge pyvisa
		>   conda install -n rex -c -conda-forge pyinstaller
		>   conda install -n rex numpy
		>   conda install -n rex pandas
		>   conda install -n rex matplotlib
		>   conda install -n rex seaborn
		>   activate rex

	From here you can use the following environment to run the Python script:

		>   python <PATH>\REX_Dev\REX.py

	To deactivate you virtual environment (when you are no longer running code)

		>   deactivate rex


The source code is located at
	
	* <PATH>\Source_Code\REX_Dev\REX.py

	**DO NOT move or delete any of the folders
	  or files located in the REX_Dev folder or the source code will not run
	  properly.

Using the command line, first set your path to your Python
executable. If you download Anaconda 2 from the Software Center it should install
to:
	* C:\engapps\Anaconda2 . In the command line, input the following lines:
	
	>   cd /d C:\engapps\Anaconda2
	>   python V:\MaxFung\Source_Code\REX_Dev\REX.py


- Re-Compiling to .exe Using PyInstaller

If you have made changes to the source code and wish to recompile it to a usable
.exe, you must first download PyInstaller using the conda environment. Then you may
package the .py file and its resources to a .exe which can be used by other
employees who have not downloaded Anaconda 2.

To download PyInstaller, input the following lines on the command line:

	>   cd /d C:\engapps\Anaconda2\Scripts
	>   conda install -c conda-forge pyinstaller

To compile edited source code to .exe, use the command line and input:

	>   cd /d C:\engapps\Anaconda2\Scripts
	>   pyinstaller --onedir --noconsole --icon=<PATH>\Source_Code\PXL_Dev\icon.ico PATH\TO\YOUR\REX.py-FILE

Once PXL has been compiled, you will need to add the following folders to the PXL
resource folder for it to run properly:

	* <PATH>\Anaconda2\Library\plugins\platforms
	* <PATH>\Anaconda2\Library\plugins\imageformats
	* ALL NON-.PY FILES LOCATED IN THE REX_DEV FOLDER
