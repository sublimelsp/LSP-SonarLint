#!/usr/bin/env bash

function main
{
    rm -rf out LSP-SonarLint LSP-SonarLint.zip
    local base_url=https://binaries.sonarsource.com/Distribution
    declare -A artifacts=(
        ["sonarlint-language-server"]="4.6.0.2652"
        ["sonar-javascript-plugin"]="6.4.1.12828"
        ["sonar-java-plugin"]="6.7.0.23054"
        ["sonar-php-plugin"]="3.9.0.6331"
        ["sonar-python-plugin"]="3.1.0.7619"
        ["sonar-html-plugin"]="3.2.0.2082"
    )
    mkdir -p out
    touch out/.no-sublime-package
    cp -R LICENSE NOTICE src/* out/
    for name in "${!artifacts[@]}"; do
        local artifact=$name-${artifacts[$name]}.jar
        curl --silent $base_url/$name/$artifact -o out/$artifact
    done
    pushd out && zip -q -r LSP-SonarLint.zip . && popd
    mv out/LSP-SonarLint.zip .
    rm -rf out
}

main "$@"
