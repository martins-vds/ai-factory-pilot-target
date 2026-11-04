import java.io.IOException;
import java.lang.reflect.Method;
import java.time.Instant;
import java.util.Date;
import java.util.List;
import javax.json.Json;
import javax.json.JsonArrayBuilder;
import javax.json.JsonObjectBuilder;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.eclipse.persistence.sessions.Record;
import org.eclipse.persistence.sessions.Session;
import org.eclipse.persistence.sessions.factories.SessionManager;

/**
 * Experiment-only observer of the unmodified source session in a private domain.
 * SQL reads bypass entity caches; POST clears identity maps, never database rows.
 */
@WebServlet("/probe")
public class TimestampProbe extends HttpServlet {
    private static final String EVENTS =
        "SELECT E.ID, E.TYPE, CAST(E.COMPLETIONTIME AS VARCHAR(40)) AS COMPLETION, "
        + "CAST(E.REGISTRATION AS VARCHAR(40)) AS REGISTRATION "
        + "FROM HANDLINGEVENT E JOIN CARGO C ON E.CARGO_ID=C.ID "
        + "WHERE C.TRACKING_ID='DEF789' ORDER BY E.ID";
    private static final String COLUMNS =
        "SELECT C.COLUMNNAME, CAST(C.COLUMNDATATYPE AS VARCHAR(100)) AS SQLTYPE "
        + "FROM SYS.SYSCOLUMNS C JOIN SYS.SYSTABLES T ON C.REFERENCEID=T.TABLEID "
        + "WHERE T.TABLENAME='HANDLINGEVENT' "
        + "AND C.COLUMNNAME IN ('COMPLETIONTIME','REGISTRATION') ORDER BY C.COLUMNNAME";

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws IOException {
        observe(request, response, false);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws IOException {
        observe(request, response, true);
    }

    private void observe(HttpServletRequest request, HttpServletResponse response, boolean clear)
            throws IOException {
        if (!"127.0.0.1".equals(request.getRemoteAddr())) {
            response.sendError(403);
            return;
        }
        try {
            Session source = null;
            Class<?> eventClass = null;
            for (SessionManager manager : SessionManager.getAllManagers()) {
                for (Session session : manager.getSessions().values()) {
                    for (Class<?> entity : session.getDescriptors().keySet()) {
                        if (entity.getName().equals(
                                "org.eclipse.cargotracker.domain.model.handling.HandlingEvent")) {
                            if (source != null && source != session) {
                                throw new IllegalStateException("multiple source sessions");
                            }
                            source = session;
                            eventClass = entity;
                        }
                    }
                }
            }
            if (source == null) {
                throw new IllegalStateException("no source HandlingEvent session");
            }
            if (clear) {
                source.getIdentityMapAccessor().initializeAllIdentityMaps();
            }
            JsonObjectBuilder result = Json.createObjectBuilder()
                .add("observed_utc", Instant.now().toString())
                .add("session", source.getName())
                .add("operation", clear ? "initializeAllIdentityMaps" : "read-only");
            JsonArrayBuilder rows = Json.createArrayBuilder();
            JsonArrayBuilder cached = Json.createArrayBuilder();
            boolean empty = true;
            List<?> records = source.executeSQL(EVENTS);
            for (Object value : records) {
                Record record = (Record) value;
                long id = ((Number) record.get("ID")).longValue();
                rows.add(Json.createObjectBuilder()
                    .add("id", id).add("type", record.get("TYPE").toString())
                    .add("completion", record.get("COMPLETION").toString())
                    .add("registration", record.get("REGISTRATION").toString()));
                Object event = source.getIdentityMapAccessor().getFromIdentityMap(id, eventClass);
                if (event != null) {
                    empty = false;
                    cached.add(Json.createObjectBuilder().add("id", id)
                        .add("completion", timestamp(event, "getCompletionTime"))
                        .add("registration", timestamp(event, "getRegistrationTime")));
                }
            }
            JsonArrayBuilder columns = Json.createArrayBuilder();
            for (Object value : source.executeSQL(COLUMNS)) {
                Record record = (Record) value;
                columns.add(Json.createObjectBuilder()
                    .add("name", record.get("COLUMNNAME").toString())
                    .add("sql_type", record.get("SQLTYPE").toString()));
            }
            result.add("rows", rows).add("cached", cached).add("columns", columns)
                .add("cache_empty", empty);
            response.setContentType("application/json");
            response.getWriter().println(result.build());
        } catch (ReflectiveOperationException | RuntimeException exception) {
            throw new IOException("timestamp observer failed", exception);
        }
    }

    private String timestamp(Object event, String getter) throws ReflectiveOperationException {
        Method method = event.getClass().getMethod(getter);
        return Instant.ofEpochMilli(((Date) method.invoke(event)).getTime()).toString();
    }
}
