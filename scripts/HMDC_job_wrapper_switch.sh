#!/bin/bash

# This is a temporary wrapper.

HMDC_BETA_WRAPPER=$(/usr/bin/condor_config_val BETA_JOB_WRAPPER)
HMDC_STABLE_WRAPPER=$(/usr/bin/condor_config_val STABLE_JOB_WRAPPER)

(grep HMDCNewSubmit ${TEMP}/.job.ad > /dev/null 2>&1) && exec $HMDC_BETA_WRAPPER $@ || exec $HMDC_STABLE_WRAPPER $@
