#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
: "${JAVA_HOME:?Set JAVA_HOME to a Java 8 JDK}"
: "${HR_04E_TIME_OUTPUT:?Set a new observation JSON path; existing files are never overwritten}"
test "$(git -C "$repo_root/.source" rev-parse HEAD)" = \
    f3beacf78de4f6d34edc4971ac87e38a5c6fe59d
if ! "$JAVA_HOME/bin/java" -version 2>&1 | grep -q 'version "1\.8\.'; then
    echo "JAVA_HOME must point to a Java 8 JDK" >&2
    exit 1
fi
export PATH="$JAVA_HOME/bin:$PATH"
export TZ=UTC JAVA_TOOL_OPTIONS=-Duser.timezone=UTC
java -version
mvn -version
work_dir="$(mktemp -d /tmp/hr-04e-time.XXXXXXXX)"
payara_home="$work_dir/payara41"
asadmin="$payara_home/bin/asadmin"
started=false
cleanup() {
    if [[ "$started" == true ]]; then
        "$asadmin" --port 19048 stop-domain timestamp-reload >/dev/null 2>&1 || true
    fi
    rm -rf "$work_dir"
}
trap cleanup EXIT

mkdir "$work_dir/source" "$work_dir/database" "$work_dir/probe"
cp -a "$repo_root/.source/." "$work_dir/source/"
chmod -R u+w "$work_dir/source"
export HR_04E_TIME_DATABASE="$work_dir/database"
export HR_04E_TIME_DOMAIN="$payara_home/glassfish/domains/timestamp-reload"
export LEGACY_BASE_URL=http://127.0.0.1:19080/cargo-tracker
export HR_04E_TIME_PROBE=http://127.0.0.1:19080/timestamp-probe/probe
printf 'Dedicated domain: %s\nDedicated database: %s\n' \
    "$HR_04E_TIME_DOMAIN" "$HR_04E_TIME_DATABASE"
(
    cd "$work_dir/source"
    mvn -P '!payara' -s "$repo_root/characterization/legacy-runtime/maven-settings.xml" \
        -B package -DskipTests -Dwebapp.databaseTempDir="$HR_04E_TIME_DATABASE" \
        -Dwebapp.graphTraversalUrl="$LEGACY_BASE_URL/rest/graph-traversal/shortest-path"
)
curl -fsSL \
    https://repo.maven.apache.org/maven2/fish/payara/distributions/payara/4.1.2.181/payara-4.1.2.181.zip \
    -o "$work_dir/payara.zip"
unzip -q "$work_dir/payara.zip" -d "$work_dir"
"$asadmin" create-domain --portbase 19000 --nopassword=true timestamp-reload
"$asadmin" start-domain timestamp-reload
started=true
"$asadmin" --port 19048 set \
    configs.config.server-config.network-config.network-listeners.network-listener.http-listener-1.address=127.0.0.1
"$asadmin" --port 19048 deploy "$work_dir/source/target/cargo-tracker.war"

api="$HOME/.m2/repository/javax/javaee-api/7.0/javaee-api-7.0.jar"
provider="$payara_home/glassfish/modules/org.eclipse.persistence.core.jar"
mkdir -p "$work_dir/probe/WEB-INF/classes"
javac -cp "$api:$provider" -d "$work_dir/probe/WEB-INF/classes" \
    "$repo_root/characterization/handling-registration/timestamp-reload/TimestampProbe.java"
jar cf "$work_dir/timestamp-probe.war" -C "$work_dir/probe" .
"$asadmin" --port 19048 deploy "$work_dir/timestamp-probe.war"

cd "$repo_root"
"$repo_root/.migration/harness/tools/afs-run" --ticket HR-04E-TIME --name timestamp-reload-pytest -- \
    python -m pytest -q -s -o addopts= \
    "$repo_root/characterization/handling-registration/test_timestamp_reload.py"
