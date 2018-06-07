# Tests

This file run tests for one minutes and output the result in test.txt.

## Run and Usage
### Run
```
$ C:\Python27\python.exe test_dist.py
-d (verbose for debug)
-b (big prism -- default = mini-prism)
-p "port" (ex: "COM1" -- This can be found in "Device Manager" on Windows)

```
### Usage
Use ```-h``` to show usage
```
  Options:
  -h,           --help            show this help message and exit
  -p PORT,      --port=PORT       specify used port [default: /dev/ttyUSB0]
  -b BAUDRATE,  --baudrate=BAUDRATE
                                  specify used baudrate [default: "COM3"]
  -d, --debug                     show debug information
  -B, --Big                       use 360 big prism
```

## Licenses

The original work was under the following copyright :

```
#Copyright (c) 2013, Marcel Schoch, ASL, ETH Zurich, Switzerland
#You can contact the author at <slynen at ethz dot ch>
#
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
#notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#notice, this list of conditions and the following disclaimer in the
#documentation and/or other materials provided with the distribution.
# * Neither the name of ETHZ-ASL nor the
#names of its contributors may be used to endorse or promote products
#derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL ETHZ-ASL BE LIABLE FOR ANY
#DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
