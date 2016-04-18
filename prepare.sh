#!/usr/bin/env bash

set -o errexit

readonly TEMPLATE_DIR="${TRAVIS_BUILD_DIR}/template"
readonly CONTENTS_DIR="${TEMPLATE_DIR}/RSqueak.app/Contents"
readonly RESOURCES_DIR="${CONTENTS_DIR}/Resources"
readonly IMAGE_TARGET="${RESOURCES_DIR}/RSqueak.image"
readonly CHANGES_TARGET="${RESOURCES_DIR}/RSqueak.image"
readonly TARGET_FILE="${TRAVIS_BUILD_DIR}/RSqueak.tar.gz"
readonly BASE_URL="https://www.hpi.uni-potsdam.de/hirschfeld/artefacts/rsqueak"
readonly TARGET_URL="${BASE_URL}/bundle"
readonly VM_LINUX="rsqueak-linux-latest"
readonly VM_OSX="rsqueak-darwin-latest"
readonly VM_WIN="rsqueak-win32-latest.exe"
readonly VM_LINUX_TARGET="${CONTENTS_DIR}/Linux/RSqueak"
readonly VM_OSX_TARGET="${CONTENTS_DIR}/MacOS/RSqueak"
readonly VM_WIN_TARGET="${CONTENTS_DIR}/Win64/RSqueak.exe"

echo "Copying Squeak image into template..."
cp "${SMALLTALK_CI_IMAGE}" "${IMAGE_TARGET}"
cp "${SMALLTALK_CI_CHANGES}" "${CHANGES_TARGET}"
cp "${SMALLTALK_CI_BUILD}/"*.sources "${RESOURCES_DIR}/"

echo "Downloading latest VMs..."
curl -f -s --retry 3 -o "${VM_LINUX_TARGET}" "${BASE_URL}/${VM_LINUX}"
curl -f -s --retry 3 -o "${VM_OSX_TARGET}" "${BASE_URL}/${VM_OSX}"
curl -f -s --retry 3 -o "${VM_WIN_TARGET}" "${BASE_URL}/${VM_WIN}"

echo "Compressing bundle..."
pushd "${TEMPLATE_DIR}" > /dev/null
tar czvf "${TARGET_FILE}" "./RSqueak.app"
popd > /dev/null

echo "Uploading bundle..."
curl -T "${TARGET_FILE}" -u "${DEPLOY_CREDENTIALS}" "${TARGET_URL}"

echo "Done!"
