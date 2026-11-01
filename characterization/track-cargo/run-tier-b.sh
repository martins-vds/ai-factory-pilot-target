#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
: "${JAVA_HOME:?Set JAVA_HOME to a Java 8 JDK}"
export PATH="$JAVA_HOME/bin:$PATH"
work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT

mkdir "$work_dir/source"
cp -a "$repo_root/.source/." "$work_dir/source/"
chmod -R u+w "$work_dir/source"
test_dir="$work_dir/source/src/test/java/org/eclipse/cargotracker/domain/model/cargo"
mkdir -p "$test_dir"
cp "$repo_root/characterization/track-cargo/tier_b/TrackCargoCharacterizationTest.java" "$test_dir/"

cd "$work_dir/source"
mvn -P '!payara' -s "$repo_root/characterization/legacy-runtime/maven-settings.xml" \
  -B -DskipTests=false \
  -Dtest=TrackCargoCharacterizationTest,ItineraryTest,CargoTest,RouteSpecificationTest,HandlingEventTest,HandlingHistoryTest test
