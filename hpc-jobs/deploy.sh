#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REMOTE_HOST="hpc"
REMOTE_USER="${1:-nsio}"
REMOTE="${REMOTE_USER}@${REMOTE_HOST}"
REMOTE_DIR="~/bachelorProject/hpc-jobs"

echo "==> Building container..."
apptainer -q build --force --ignore-subuid --ignore-fakeroot-command "$SCRIPT_DIR/container.sif" "$SCRIPT_DIR/compare-container.def"

echo "==> Uploading job files..."
scp -r "$SCRIPT_DIR"/container.sif "$SCRIPT_DIR"/*.job "$REMOTE:$REMOTE_DIR"

echo "==> Submitting job..."
ssh "$REMOTE" "cd $REMOTE_DIR && sbatch multi.job"

echo "==> Done."
