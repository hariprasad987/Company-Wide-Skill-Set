# Task Tracker API — Stimulated Node.js Task

This stimulated task implements a small REST API with Node.js's built-in HTTP module. Data is stored in memory and resets whenever the server restarts.

## Run

```bash
cd "4 - 7 yrs/Node.js - Stimulated Task/Task Tracker API"
npm start
```

The API runs at <http://localhost:3000>.

## Try the endpoints

List tasks:

```bash
curl http://localhost:3000/api/tasks
```

Create a task:

```bash
curl -X POST http://localhost:3000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Document the project"}'
```

Complete a task:

```bash
curl -X PATCH http://localhost:3000/api/tasks/2 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'
```

Delete a task:

```bash
curl -X DELETE http://localhost:3000/api/tasks/1
```

No third-party dependencies are required.
