[![License](https://img.shields.io/badge/version-0.1-orange.svg)]()
[![License](https://img.shields.io/badge/license-GPL3-blue.svg)]()
[![License](https://img.shields.io/badge/python->%3D3.4-green.svg)]()

# PyMon

PyMon Last release : Version 0.1

What is it?
-----------

PylMon is a monitoring framework for python, it's based on FodtlMon which is a general moniotring framework based on distributed first order linear temporal logic.

Installation
------------

You can install pymon directly using pip3 :

    https://pypi.python.org/pypi/pymon
    $ sudo pip3 install pymon

Or manually :
You need PythonX.X.X >= Python3.4.0 installed on your system

    You need to install the following dependencies :
        $ sudo pip3 install fodtlmon

To install the framework run setup.py:

        $ sudo python3 setup.py install

Usage
-----

PyMon provides two monitoring modules, wh

#### 1. WhiteBox:

	from pymon.whitebox.whitebox import *

Using the decorator @mon_fx("") in order to monitor a property on a function/method.

	@mon_fx(formula="FODTL formula", debug=False, raise_on_error=False)

##### Systype module:
In order to use the runtime type checker first you need to import the systypes module.

	from pymon.whitebox.systypes import *

Then use the decorator @SIG on functions and methods

	@SIG(formula="Type formula", debug=False, raise_on_error=True)

The formula type have the following format:

    FORMULA  : ( ARG1, ARG2, ... ) [-> TYPE]
    ARG   : <arg_name> : TYPE
    TYPE  : TYPE ( '|' ) TYPE | STRING


###### Example
A simple example with native types:

	@SIG("(a:int, b:int)")
    def foo(a, b):
		return a+b

	foo(1, "2")

	>> Exception: Arguments type Error ! Expected <(int('a')) & (int('b')) >  Found : ["b: <class 'str'>", "a: <class 'int'>"]

for more examples see the examples folder.

#### 2. BlackBox:

Licensing
---------

GPL V3 . Please see the file called LICENSE.

Contacts
--------

###### Developer :
>   Walid Benghabrit        <Walid.Benghabrit@mines-nantes.fr>

###### Contributors :
>   Pr.Jean-Claude Royer  <Jean-Claude.Royer@mines-nantes.fr>  (Theory)  
>   Dr. Hervé Grall       <Herve.Grall@mines-nantes.fr>        (Theory)  

-------------------------------------------------------------------------------
Copyright (C) 2014-2016 Walid Benghabrit  
Ecole des Mines de Nantes - ARMINES  
ASCOLA Research Group  
A4CLOUD Project http://www.a4cloud.eu/

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
