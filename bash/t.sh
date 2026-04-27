#!/bin/bash

t() {
  if [[ "$1" =~ ^[0-9]+$ ]]; then
    tree -L "$1" "${@:2}"
  else
    tree "$@"
  fi
}
