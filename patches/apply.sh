#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Compatibility entry point; all preflight and application logic lives in apply.py.
exec python3 "$(dirname "$0")/apply.py" "$@"
