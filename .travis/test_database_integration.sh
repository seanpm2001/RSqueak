#!/bin/bash

set -e

IMAGE="${IMAGE:-}"
IMAGE_URL="${IMAGE_URL:-"https://www.hpi.uni-potsdam.de/hirschfeld/artefacts/\
rsqueak/bundle/RSqueak.tar.gz"}"
IMAGE_DIR="${IMAGE_DIR:-}"
IMAGE_EXTRACT="${IMAGE_EXTRACT:-"./RSqueak.app/Contents/Resources"}"
IMAGE_PATH="${IMAGE_EXTRACT}/RSqueak.image"
RESULT_CMD="${RESULT_CMD:-}"
RESULT_CMD_URL="${RESULT_CMD_URL:-"https://raw.githubusercontent.com/hpi-swa/\
smalltalkCI/master/lib/junit_xml_prettfier.py"}"

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

FILETREE_PATH=$(realpath repository)

cat > "${HOME}/runSQPyteTests.st" <<EOF
    FileStream startUp: true.
    Metacello new
        baseline: 'SQPyte';
        repository: 'filetree://${FILETREE_PATH}';
        onConflict: [:ex | ex allow];
        load.
    SCISqueakTestReport runClasses: {(Smalltalk at: #SQLiteTests). (Smalltalk at: #SQPyteTests)} named: 'test'.
    Smalltalk at: #WorldState ifPresent: [:global |
        global addDeferredUIMessage: [
            Smalltalk at: #SmalltalkImage ifPresent: [:image |
                image current snapshot: false andQuit: true ]]]
EOF

if [[ -z "${IMAGE}" ]]; then
    if [[ -z "${IMAGE_DIR}" ]]; then
        IMAGE_DIR=$(mktemp -d "${TMPDIR:-/tmp}/sqpyte.XXXXXXXXX")
    fi
    TAR="${IMAGE_DIR}/rsqueak.tar.gz"

    mkdir -p "${IMAGE_DIR}"
    pushd "${IMAGE_DIR}"

    if [ ! -f "${TAR}" ]; then
        echo "==== Download image archive..."
        wget --quiet "${IMAGE_URL}" -O "${TAR}"
    fi

    echo "==== Extract archive..."
    tar -zxf "${TAR}" "${IMAGE_EXTRACT}/"
    IMAGE=$(realpath "${IMAGE_PATH}")

    popd
fi

if [[ ! -f "${IMAGE}" ]]; then
    echo "Image file not found. That's bad." && exit 1
fi

echo "==== Run tests..."
./rsqueak --silent --no-display "${IMAGE}" "${HOME}/runSQPyteTests.st"

if [[ -z "${RESULT_CMD}" ]]; then
    RESULT_CMD="/tmp/print_test_results.py"

    if [[ ! -f "${RESULT_CMD}" ]]; then
        wget --quiet "${RESULT_CMD_URL}" -O "${RESULT_CMD}"
        chmod +x "${RESULT_CMD}"
    fi
fi

"${RESULT_CMD}" "$(dirname "${IMAGE}")"
