#!/bin/bash

TOOLS=(pylint isort black)

# lint-staged passses a list of staged files as arguments.
# Note that not all staged files are passed but
# only those files filtered by glob pattens.
TARGET_FILES=$*

# Reset
ColorOff='\033[0m'       # Text Reset

# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White

# Bold
BBlack='\033[1;30m'       # Black
BRed='\033[1;31m'         # Red
BGreen='\033[1;32m'       # Green
BYellow='\033[1;33m'      # Yellow
BBlue='\033[1;34m'        # Blue
BPurple='\033[1;35m'      # Purple
BCyan='\033[1;36m'        # Cyan
BWhite='\033[1;37m'       # White

print_msg() {
    local msg=$1
    echo -e "${Blue}${msg}${ColorOff}"
}

print_error_msg() {
    local msg=$1
    echo -e "${Yellow}${msg}${ColorOff}"
}

print_command_not_found() {
    local command=$1
    print_error_msg "❌ \"${command}\" is not installed."
}

check_command() {
  local tool=$1
  if [ -x "$(command -v ${tool})" ]; then
    return 0
  fi
  return 1
}

run_command() {
    local command_name=$1
    local command=$*
    echo
    echo -e "🚀 ${BWhite}Running ${command_name}...${ColorOff}"
    $command
}

check_all_tools_installed() {
    print_msg "⌛ Checking all linters and formatters are installed."
    for tool in ${TOOLS[@]}; do
        if ! check_command $tool; then
            print_command_not_found $tool
            exit 1
        fi
    done

    print_msg "✅ Done."
}

 
exit_on_error() {
    exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        exit $exit_code
    fi
}

# Call exit code handler on EXIT.
trap exit_on_error EXIT

# Exit when any command fails.
set -e

check_all_tools_installed
######################################
# precommit main script.
######################################
readonly top_dir=$(git rev-parse --show-toplevel)

run_command pylint -rn -sn --rcfile=${top_dir}/.pylintrc $TARGET_FILES
run_command isort --profile=google "$TARGET_FILES"
run_command black --line-length 88 $TARGET_FILES
