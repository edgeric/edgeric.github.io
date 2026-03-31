#!/usr/bin/env bash
set -euo pipefail

# One-command Sphinx build + deploy for EdgeRIC docs.
# Defaults can be overridden via flags or environment variables.

USER_NAME="${DEPLOY_USER:-edgeric}"
HOST_NAME="${DEPLOY_HOST:-edgeric.ucsd.edu}"
REMOTE_DIR="${DEPLOY_REMOTE_DIR:-~/htdocs/}"
JUMP_HOST="${DEPLOY_JUMP_HOST:-}"
IDENTITY_FILE="${DEPLOY_IDENTITY_FILE:-}"
DRY_RUN=false
BUILD=true

usage() {
  cat <<'EOF'
Usage: ./deploy_site.sh [options]

Shorthand:
  ./deploy_site.sh user@target-host
  (equivalent to: ./deploy_site.sh --target user@target-host)

Options:
  --user USER           SSH user (default: edgeric)
  --host HOST           Target host (default: edgeric.ucsd.edu)
  --target USER@HOST    Target user and host in one flag
  --remote-dir PATH     Remote destination dir (default: ~/htdocs/)
  --jump-host HOST      SSH jump host (example: edgeric@mywebsite.eng.ucsd.edu)
  --identity FILE       SSH private key file (example: ~/.ssh/id_ed25519)
  --no-build            Skip 'make html' and only sync existing _build/html
  --dry-run             Preview upload without changing remote files
  -h, --help            Show this help

Environment variable equivalents:
  DEPLOY_USER, DEPLOY_HOST, DEPLOY_REMOTE_DIR, DEPLOY_JUMP_HOST, DEPLOY_IDENTITY_FILE
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --user)
      USER_NAME="$2"
      shift 2
      ;;
    --host)
      HOST_NAME="$2"
      shift 2
      ;;
    --target)
      if [[ "$2" == *"@"* ]]; then
        USER_NAME="${2%@*}"
        HOST_NAME="${2#*@}"
      else
        echo "Invalid --target value: $2 (expected user@host)" >&2
        exit 1
      fi
      shift 2
      ;;
    --remote-dir)
      REMOTE_DIR="$2"
      shift 2
      ;;
    --jump-host)
      JUMP_HOST="$2"
      shift 2
      ;;
    --identity)
      IDENTITY_FILE="$2"
      shift 2
      ;;
    --no-build)
      BUILD=false
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *@*)
      if [[ "$1" == *"@"* ]]; then
        USER_NAME="${1%@*}"
        HOST_NAME="${1#*@}"
        shift
      fi
      ;;
    *)
      echo "Unknown option or argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [[ "$BUILD" == true ]]; then
  echo "[1/2] Building docs with make html..."
  make html
fi

if [[ ! -d "_build/html" ]]; then
  echo "Error: _build/html not found. Run without --no-build or build docs first." >&2
  exit 1
fi

RSYNC_OPTS=( -avz --delete )
if [[ "$DRY_RUN" == true ]]; then
  RSYNC_OPTS+=( -n )
fi

SSH_CMD="ssh"
if [[ -n "$IDENTITY_FILE" ]]; then
  SSH_CMD+=" -i $IDENTITY_FILE"
fi
if [[ -n "$JUMP_HOST" ]]; then
  SSH_CMD+=" -J $JUMP_HOST"
fi

echo "[2/2] Syncing _build/html to ${USER_NAME}@${HOST_NAME}:${REMOTE_DIR} ..."
rsync "${RSYNC_OPTS[@]}" -e "$SSH_CMD" "_build/html/" "${USER_NAME}@${HOST_NAME}:${REMOTE_DIR}"

echo "Deploy completed."
if [[ "$DRY_RUN" == true ]]; then
  echo "Dry run mode was enabled; no remote files were changed."
fi
