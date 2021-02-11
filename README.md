<p align="center">
  <img src="https://www.lancaster.ac.uk/media/lancaster-university/content-assets/images/fst/logos/Physicslogo.svg" width="350" height="95">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://compositesuk.co.uk/sites/default/files/hub/logos/TFP%20logo%20new.PNG" width="100" height="100">
</p>

# Industrial-Group-Project
Software analysis code for the PHYS 355 Lancaster University Industrial Group Project with [TFP](https://www.tfpglobal.com/)

The aim of this project is to characterise defects in PEM fuel cell materials produced by Technical Fibre Products Ltd (TFP). In particular, the presence of visually unappealing lines in the gas diffusion layers (GDL) of fuel cells has plagued particular carbon-based nonwovens manufactured by TFP. Such defects do not appear to hinder the technical performance of the GDL, yet impair the customer perception of product quality. This has called for a quantitative testing method to be devised, providing both a quantifiable determination of line severity, and a clear procedure through which future improvements can be assessed. 

The analysis code seeks to provide an efficient testing process for batch samples, through automated image processing and analysis.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for personal use, as well as for testing and development purposes.

### Prerequisites
Ensure you have the following prerequisites on your development machine:
* Python - [Download & Install Python](https://www.python.org/downloads/). Ensure Python 3 is installed (not Python 2), and that you install for the correct OS
* Command Line - this should come in-built with all operating systems (e.g. Windows, macOS, Linux), and can be opened the following ways:
  * Windows: Press "Win+R," type "Powershell" and press "Enter"
  * macOS: Press "Cmd+Space" to open spotlight search, type "Terminal" and press "Enter"
  * Linux: Press "Ctrl+Alt+T"

The following Python packages will also require installation before use of the software:
- numpy
- scipy
- scikit-image
- pathlib
- matplotlib
- os
- sys
- glob
- warnings
---
Package installation is carried out in the command line, a text interface which takes in user commands and passes them to a device's operating system.
To install a package, enter the following in the command line:
```
> python -m pip install module-name
```
where `module-name` is the name of the module, e.g. `matplotlib`, `scikit-image`. These modules can all be entered in the same line, separated by spaces. 

_N.B pip, a package manager for Python, should already be installed if using Python 3.4 and above. If necessary you can upgrade it to the most recent version through:_
```
> python -m pip install -U pip
```

If you have previously installed any of these packages, ensure you update to the most recent release via:
```
> pip install --upgrade module-name
```
You can also view a list of all installed python packages using `pip list`. 

### Installation
To download the relevant files:
1) Navigate to the top of this repository
2) Click the green button with 'Code' and a drop-down arrow
3) Click 'Download ZIP'
4) The code will appear as the folder `Industrial-Group-Project` in your Downloads folder
4) Extract (by right clicking) the ZIP to a chosen folder in your local device directory

*N.B.* The only files required to run the code are:
- `linefinder.py` (Analysis Method to find MD Lines)
- `UI.py` (User Interface)
- `info.py` (Information about the program)

A collection of ineffective analysis methods can be found in the _didnt-work_ and _obsolete_ folders.


### Running the Code
Prior to running the code, please ensure the above prerequisites (installed Python and relevant packages) are met.

To run the software, you just need to run the `UI.py` file:
1) Open command line (terminal) for the appropriate operating system (See **Prerequisites**)
3) Find the path containing the extracted ZIP folder e.g. `C:\Documents\Bob\SampleScans\Carbon\LowAW\Industrial-Group-Project'` 
4) Change directory to the folder containing the `UI.py` file:
   - Append `\image-processing` to the path found in 2), since this contains the UI.py file
   - In command line, type `cd` then enter this new path in double quotes e.g:
   ```
   > cd "C:\Documents\Bob\SampleScans\Carbon\LowAW\Industrial-Group-Project\image-processing"
   ```
   - To run `UI.py`, enter:
   ```
   > python UI.py
   ```
   
*N.B.* The `>` signifies the prompt in Windows terminal (this will be a `$` in Linux and macOS) - do not type this!

(Just run `UI.py` `__init__` ~~(this is a bad pun I will delete)~~)

## Built With

* [Python](https://github.com/python/cpython)


## Contribution
### Core Contributors

<!--ALL-CONTRIBUTORS-LIST -->
| [<img src="https://avatars.githubusercontent.com/u/73170205?v=4" width="100px;"/><br /><sub><b>Tom Fell</b></sub>](https://github.com/twf2360)<br /> | [<img src="https://avatars.githubusercontent.com/u/68572453?v=4" width="100px;"/><br /><sub><b>Melissa Chung</b></sub>](https://github.com/msychung)<br /> | [<img src="https://avatars.githubusercontent.com/u/74320011?v=4>" width="100px;"/><br /><sub><b>Michael Revell</b></sub>](https://github.com/mjrevell)<br /> |
| :---: | :---: | :---: |
<!-- END ALL-CONTRIBUTORS-LIST -->

### Contributing
We welcome all contributions towards this analysis software. However, due to the nature of the project, there is no guaranteed regular maintenance beyond July 2021. Any contributions will be reviewed at the original contributors' discretion. 

To contribute using version control software (Git):
1) Create a new branch (and fork if applicable), labelling it appropriately
2) Make the changes on that branch
3) Commit to and push the changes
4) Create a pull request from your branch to master
5) An original contributor will then review your pull request


## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). This license is conducive to free, open-source software.
