#!/bin/bash

CAT=$(which cat)
CLASSAD="$(${CAT})"

env > /tmp/env
echo "${CLASSAD}" > /tmp/classad

cat <<EOF
Out = $HOME/out.txt
Err = $HOME/err.txt
EOF
