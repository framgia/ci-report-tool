#!/bin/bash

# For any discussion, issues and change requests,
# please send to Framgia CI/CD Team.
#
# Script to install the Framgia CI Command Line tool
#
# Run as root or insert `sudo -E` before `bash`

PACKAGE_URL="https://github.com/framgia/ci-report-tool/zipball/master"

print_status() {
  local outp=$(echo "$1")
  echo -e "## ${outp}"
}

bail() {
  echo 'Error executing command, exiting'
  exit 1
}

exec_cmd_nobail() {
  echo "+ $1"
  bash -c "$1"
}

exec_cmd() {
  exec_cmd_nobail "$1" || bail
}

setup() {
    print_status "Installing the Framgia CI Command Line Tool ..."
    print_status "Downloading release setup from Github ..."
    echo "+ mktemp"
    TMP=$(mktemp || bail)
    PKG_TMP="${TMP}.zip"
    TARGET="/usr/local/share/framgia-ci"
    TARGET_TMP="${TARGET}-tmp"
    exec_cmd "curl -sL -o '${PKG_TMP}' '${PACKAGE_URL}'"
    print_status "Extracting package ..."
    exec_cmd "unzip ${PKG_TMP} -d ${TARGET_TMP}"
    exec_cmd "mkdir ${TARGET}"
    print_status "Moving package ..."
    for FILE in `ls ${TARGET_TMP}`; do
        if [[ -d ${TARGET_TMP}/${FILE} ]]; then
            exec_cmd "cp -rf ${TARGET_TMP}/${FILE}/index.dist/* ${TARGET}"
        fi
    done
    exec_cmd "ln -s ${TARGET}/index.exe /usr/local/bin/framgia-ci"
    print_status "Cleaning up..."
    exec_cmd "rm -rf ${PKG_TMP} ${TARGET_TMP}"
    exit 0
}

setup
