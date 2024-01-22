#!/usr/bin/bash

cd /home/jovyan/work

for d in */ ; do
  cd "${d}" || echo "Failed"
  git checkout . -f || echo "Failed"
  git pull -f || echo "Failed"
  done
