#!/bin/sh

# make sure coverage3 is installed
if which coverage3 > /dev/null; then
    echo "Found Coverage.py"
else
    echo "Coverage.py not found. Before running this, try running:"
    echo
    echo "    sudo pip3 install coverage"
    echo

    exit
fi

# ensure all stale coverage data is removed
coverage3 erase

export PYTHONPATH=./

#
# Run the unit tests
#

# Framework:
coverage3 run -a tests/framework/framework_test.py > /dev/null
coverage3 run -a tests/framework/networklistener_test.py > /dev/null
coverage3 run -a tests/common/GlobalConfig_Test.py > /dev/null

# Database:

# Plugins:

# Report Server:

coverage3 run -a tests/reportserver/dateTimeUtilityTest.py > /dev/null
coverage3 run -a tests/reportserver/utilities_test.py > /dev/null

# generate coverage reports
coverage3 report | grep -v "__init__.py"
coverage3 html

# remove coverage data file
coverage3 erase

# Done!
echo
echo "Detailed coverage data:"
echo
echo "    $PWD/htmlcov/index.html"
echo

