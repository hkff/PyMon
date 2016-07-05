"""
pymon version 0.1
Copyright (C) 2015 Walid Benghabrit

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
"""
from distutils.core import setup

setup(
    name='pymon',
    version='0.1',
    packages=['pymon', 'pymon/blackbox', 'pymon/whitebox'],
    url='https://github.com/hkff/PyMon',
    license='GPL3',
    author='Walid Benghabrit',
    author_email='benghabrit.walid@gmail.com',
    description='Temporal Logic monitoring framework for python.',
    install_requires=[
        'fodtlmon>=1.2',
    ]
)
