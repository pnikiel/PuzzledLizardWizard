PuzzledLizardWizard
-------------------

Author: Piotr P. Nikiel <piotr@nikiel.info>

What is this?
-------------

PuzzledLizardWizard is a tool that makes software components (for example, hardware access libraries)
for AXI4 peripherals.

Assumptions and constraints
---------------------------

* the AXI4 component is generated using http://AirHdl.com
* the component is handled by the UserSpace I/O Linux kernel driver
* libUIO is used for user-space applications to talk to the corresponding /dev/uio device

Basic usage mode
----------------

1. Create your AXI4 regmap in AirHdl
1. Download the register map in JSON format
1. Clone this repository
1. Run `./generate.py <path_to_your_regmap_in_json` (for looking around, you can use one of our regmaps from `sample` directory)
1. In the output directory you will find (assume my_axi4_component is the regmap name):
  * An access library in C (my_axi4_component.h and my_axi4_component.c) which builds on top of libUIO. 
    Note: the future of C-based library is unsure, we're moving to C++ library.
  * An access library in C++ (camelCase file names: MyAxi4Component.hpp and MyAxi4Component.cpp) which builds on top of libUio.
  * A boost-python based C++ class which can be compiled to a Python module. (this isn't complete yet)
