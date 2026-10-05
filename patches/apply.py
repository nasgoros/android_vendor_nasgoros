#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 The nasgorOS Project
# SPDX-License-Identifier: Apache-2.0
"""Apply the nasgorOS adaptation patches after syncing the pinned manifest.

Preflight checks every revision and patch before changing any repository.
Already-applied patches are skipped, and unrelated local changes are retained.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    location = parser.add_mutually_exclusive_group(required=True)
    location.add_argument('--source-root', type=Path, help='Android source tree after repo sync')
    location.add_argument('--clones', type=Path, help='workspace repos/ directory for development')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true', help='preflight only; no writes')
    mode.add_argument('--verify', action='store_true', help='require every patch already applied')
    args = parser.parse_args()
    lock = json.loads((HERE.parent/'ports/crdroid/sources.lock.json').read_text())
    projects = {item['path']: item for item in lock['projects']}
    repositories = {}
    errors = []
    for item in projects.values():
        repo = ((args.clones/item['local_clone']) if args.clones else (args.source_root/item['path'])).resolve()
        repositories[item['path']] = repo
        head = git(repo, 'rev-parse', 'HEAD')
        if head.returncode or head.stdout.strip() != item['revision']:
            errors.append(f'{item["path"]}: expected pinned revision {item["revision"]}; sync the port manifest first')
    pending = []
    for item in json.loads((HERE/'series.json').read_text()):
        repo = repositories[item['path']]
        patch = HERE/item['patch']
        reverse = git(repo, 'apply', '--reverse', '--check', str(patch))
        if reverse.returncode == 0:
            print(f'Applied: {item["patch"]}')
            continue
        check = git(repo, 'apply', '--check', str(patch))
        if check.returncode:
            errors.append(f'{item["patch"]}: conflicts; local changes were not modified\n{check.stderr.strip()}')
        elif args.verify:
            errors.append(f'{item["patch"]}: patch has not been applied')
        else:
            pending.append((repo, patch))
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    if args.check or args.verify:
        print(f'Preflight passed: {len(projects)} pinned repositories, {len(pending)} pending patches')
        return 0
    completed = []
    for repo, patch in pending:
        result = git(repo, 'apply', str(patch))
        if result.returncode:
            print(result.stderr, file=sys.stderr)
            # Only undo patches applied by this invocation, never user changes.
            for previous_repo, previous_patch in reversed(completed):
                undo = git(previous_repo, 'apply', '--reverse', str(previous_patch))
                if undo.returncode:
                    print(f'Could not roll back {previous_patch}: {undo.stderr}', file=sys.stderr)
            return 1
        completed.append((repo, patch))
        print(f'Applied: {patch.relative_to(HERE)}')
    print('NasgorOS customization patches are ready.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
