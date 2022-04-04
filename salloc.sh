#!/bin/bash
salloc --job-name=simone-job \
       --nodes=1 \
       --ntasks-per-node=4 \
       --cpus-per-task=1  \
       --reservation=eb_testing \
       --gres=gpu:pascal:2 \
       --mem=1G \
       --time=04:00:00
#       --mail-user=romiti@hiskp.uni-bonn.de  \
#       --output=hmc.cpu.log.out  \
#      --error=hmc.cpu.error.out  \

