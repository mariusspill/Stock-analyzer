#!/usr/bin/env bash
# Run the test suite inside the container, so it uses the locked dependencies
# rather than whatever happens to be installed on this machine.
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose run --rm --no-deps pipeline pytest "$@"
