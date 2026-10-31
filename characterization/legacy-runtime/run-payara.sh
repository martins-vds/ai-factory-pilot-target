#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
: "${JAVA_HOME:?Set JAVA_HOME to a Java 8 JDK}"

if ! "$JAVA_HOME/bin/java" -version 2>&1 | grep -q 'version "1\.8\.'; then
  echo "JAVA_HOME must point to a Java 8 JDK" >&2
  exit 1
fi

export PATH="$JAVA_HOME/bin:$PATH"
work_dir="$(mktemp -d)"
payara_home="$work_dir/payara41"
server_started=false

cleanup() {
  if [[ "$server_started" == true ]]; then
    "$payara_home/bin/asadmin" stop-domain domain1 >/dev/null 2>&1 || true
  fi
  rm -rf "$work_dir"
}
trap cleanup EXIT

mkdir "$work_dir/source"
cp -a "$repo_root/.source/." "$work_dir/source/"
chmod -R u+w "$work_dir/source"

echo "Building Cargo Tracker from a scratch copy with the Payara test profile disabled."
java -version
mvn -version
(
  cd "$work_dir/source"
  mvn -P '!payara' -s "$repo_root/characterization/legacy-runtime/maven-settings.xml" -B package -DskipTests
)

curl -fsSL \
  https://repo.maven.apache.org/maven2/fish/payara/distributions/payara/4.1.2.181/payara-4.1.2.181.zip \
  -o "$work_dir/payara.zip"
unzip -q "$work_dir/payara.zip" -d "$work_dir"
echo "Using Payara Server 4.1.2.181."
"$payara_home/bin/asadmin" start-domain domain1
server_started=true
"$payara_home/bin/asadmin" deploy --force "$work_dir/source/target/cargo-tracker.war"

response_body="$work_dir/response.html"
status="$(curl -sS --max-time 60 -o "$response_body" -w '%{http_code}' \
  http://localhost:8080/cargo-tracker/)"
printf 'GET http://localhost:8080/cargo-tracker/ -> HTTP %s\n' "$status"
test "$status" = 200
grep -q 'Public Tracking Interface' "$response_body"
grep -m1 -o 'Public Tracking Interface' "$response_body"
