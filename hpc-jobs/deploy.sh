#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REMOTE_HOST="hpc"
JOB_SCRIPT="${1:-multi.job}"
REMOTE_USER="${2:-nsio}"
REMOTE="${REMOTE_USER}@${REMOTE_HOST}"
REMOTE_DIR="~/bachelorProject"

# echo "==> Building container..."
# apptainer -q build --force --ignore-subuid --ignore-fakeroot-command "$SCRIPT_DIR/container.sif" "$SCRIPT_DIR/compare-container.def"

echo "==> Uploading job files..."
rsync -r ~/bachelorProject/{Algorithms,gurobi,Utils,*.py} "$REMOTE:$REMOTE_DIR"
scp -r "$SCRIPT_DIR"/*.job "$REMOTE:$REMOTE_DIR/hpc-jobs"
# "$SCRIPT_DIR"/container.sif 

echo "==> Submitting job..."
ssh "$REMOTE" "cd $REMOTE_DIR/hpc-jobs && sbatch $JOB_SCRIPT"

echo "==> Done."
