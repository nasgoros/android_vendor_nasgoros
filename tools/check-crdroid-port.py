#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 The nasgorOS Project
# SPDX-License-Identifier: Apache-2.0
"""Check the port's source integration without invoking an Android compiler."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

VENDOR = Path(__file__).resolve().parent.parent
ANDROID = '{http://schemas.android.com/apk/res/android}'


def run(*args, cwd=None):
    return subprocess.check_output(args, cwd=cwd)


def check(condition, message):
    if not condition:
        raise ValueError(message)


def merged_manifest(directory):
    projects = {}

    def include(name):
        for element in ET.parse(directory/name).getroot():
            if element.tag == 'include':
                include(element.attrib['name'])
            elif element.tag == 'project':
                path = element.get('path', element.attrib['name'])
                check(path not in projects, f'Duplicate manifest path: {path}')
                projects[path] = element
            elif element.tag == 'remove-project':
                matches = [path for path, project in projects.items()
                           if project.get('name') == element.get('name')
                           and (element.get('path') is None or element.get('path') == path)]
                check(matches or element.get('optional') == 'true',
                      f'Unmatched remove-project: {element.attrib}')
                for path in matches:
                    del projects[path]
    include('default.xml')
    return projects


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--clones', required=True, type=Path)
    parser.add_argument('--manifest', required=True, type=Path)
    args = parser.parse_args()
    clones = args.clones.resolve()
    lock = json.loads((VENDOR/'ports/crdroid/sources.lock.json').read_text())['projects']
    projects = merged_manifest(args.manifest.resolve())
    repositories = {}
    for item in lock:
        entry = projects[item['path']]
        check(entry.get('name') == item['repository']
              and entry.get('revision') == item['revision']
              and entry.get('upstream') == 'refs/heads/'+item['branch'],
              f'Manifest/lock mismatch: {item["path"]}')
        repo = clones/item['local_clone']
        check(run('git', 'rev-parse', 'HEAD', cwd=repo).decode().strip() == item['revision'],
              f'Clone/lock mismatch: {item["path"]}')
        repositories[item['path']] = repo
    print(f'PASS: {len(projects)} manifest paths, {len(lock)} pinned repositories')

    # Only real resource trees: upstream test fixtures can intentionally contain invalid XML.
    xml_files = list((clones/'android_packages_apps_NasgorSettings').rglob('*.xml'))
    xml_files += list((clones/'android_packages_apps_crDroidSettings/res').rglob('*.xml'))
    xml_files += list((VENDOR/'overlay/crdroid').rglob('*.xml'))
    xml_files += list((VENDOR/'overlay/minimal').rglob('*.xml'))
    settings_resources = clones/'android_packages_apps_Settings/res'
    xml_files += list(settings_resources.glob('*/nasgor_about*.xml'))
    xml_files += [settings_resources/'xml/my_device_info.xml',
                  settings_resources/'xml/firmware_version.xml']
    for file in xml_files:
        ET.parse(file)
    print(f'PASS: {len(xml_files)} resource/manifest XML files')

    # Resolve the explicit external activities exposed by the customization screens.
    activities = set()
    roots = list(repositories.values()) + [clones/'android_packages_apps_NasgorSettings']
    for root in roots:
        if not root.name.startswith(('android_packages_apps_', 'android_packages_services_')):
            continue
        for manifest in root.rglob('AndroidManifest.xml'):
            tree = ET.parse(manifest).getroot()
            package = tree.get('package')
            if not package:
                continue
            for activity in tree.findall('./application/activity') + tree.findall('./application/activity-alias'):
                name = activity.get(ANDROID+'name', '')
                if name.startswith('.'):
                    name = package + name
                elif '.' not in name:
                    name = package + '.' + name
                activities.add((package, name))
    intents = 0
    for xml in (clones/'android_packages_apps_crDroidSettings/res/xml').glob('*.xml'):
        for intent in ET.parse(xml).iter('intent'):
            package = intent.get(ANDROID+'targetPackage')
            target = intent.get(ANDROID+'targetClass')
            if package and target:
                check((package, target) in activities, f'Unresolved activity in {xml.name}: {target}')
                intents += 1
    print(f'PASS: {intents} explicit activity intents')

    names = {}
    for root in roots:
        for pattern in ('Android.bp', 'Android.mk'):
            for file in root.rglob(pattern):
                text = file.read_text(errors='replace')
                for name in re.findall(r'\bname\s*:\s*"([^"\n]+)"', text) + re.findall(
                        r'^\s*LOCAL_(?:MODULE|PACKAGE_NAME)\s*:?=\s*([^\s#$]+)', text, re.M):
                    names.setdefault(name, set()).add(str(file))
    packages = []
    for line in (VENDOR/'config/crdroid.mk').read_text().replace('\\\n', ' ').splitlines():
        if line.startswith('PRODUCT_PACKAGES +='):
            packages.extend(line.split('+=', 1)[1].split())
    for package in packages:
        check(package in names, f'Missing product module: {package}')
        check(len(names[package]) == 1, f'Duplicate product module: {package}: {names[package]}')
    print(f'PASS: {len(packages)} selected product modules have unique definitions in port sources')

    # Reconstruct edited files from the pinned revision, then apply the exported patch.
    # This checks the committed patch artifact rather than just the modified working tree.
    series = json.loads((VENDOR/'patches/series.json').read_text())
    for item in series:
        repo = repositories[item['path']]
        patch = VENDOR/'patches'/item['patch']
        run('git', 'apply', '--reverse', '--check', str(patch), cwd=repo)
        changed = run('git', 'diff', 'HEAD', '--name-only', '-z', cwd=repo).decode().strip('\0').split('\0')
        with tempfile.TemporaryDirectory(prefix='nasgor-port-check-') as directory:
            temporary = Path(directory)
            for name in changed:
                original = subprocess.run(['git', 'show', 'HEAD:'+name], cwd=repo,
                                          capture_output=True)
                if original.returncode == 0:
                    target = temporary/name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(original.stdout)
            run('git', 'apply', '--check', str(patch), cwd=temporary)
            run('git', 'apply', str(patch), cwd=temporary)
            for name in changed:
                actual, expected = temporary/name, repo/name
                check(actual.exists() == expected.exists(), f'Patch file mismatch: {name}')
                if expected.exists():
                    check(actual.read_bytes() == expected.read_bytes(), f'Patch content mismatch: {name}')
    print(f'PASS: {len(series)} patches reconstruct the current source changes')
    print('Static integration checks only. Compilation and device validation are still required.')


if __name__ == '__main__':
    main()
