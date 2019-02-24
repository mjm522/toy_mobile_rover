#!/bin/bash

TMR_ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export TMR_ROOT_DIR="${TMR_ROOT_DIR}"

MODULES='tmr_robot/src tmr_rover/src tmr_sensors/src'

for module in $MODULES
do
    module_path=$TMR_ROOT_DIR/$module
    echo "adding module: $module_path"
    export PYTHONPATH=$module_path:$PYTHONPATH
done

cd $TMR_ROOT_DIR

echo "PYTHON PATH IS: $PYTHONPATH"