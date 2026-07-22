const http = require("node:http");

const port = Number(process.env.PORT) || 3000;
let nextId = 3;
let tasks = [
  { id: 1, title: "Design the API", completed: true },
  { id: 2, title: "Test every endpoint", completed: false },
];

function sendJson(response, statusCode, data) {
  response.writeHead(statusCode, { "Content-Type": "application/json; charset=utf-8" });
  response.end(JSON.stringify(data, null, 2));
}

function readJson(request) {
  return new Promise((resolve, reject) => {
    let body = "";

    request.on("data", (chunk) => {
      body += chunk;
      if (body.length > 1_000_000) {
        reject(new Error("Request body is too large"));
        request.destroy();
      }
    });

    request.on("end", () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch {
        reject(new Error("Request body must contain valid JSON"));
      }
    });

    request.on("error", reject);
  });
}

function taskIdFrom(pathname) {
  const match = pathname.match(/^\/api\/tasks\/(\d+)$/);
  return match ? Number(match[1]) : null;
}

const server = http.createServer(async (request, response) => {
  const url = new URL(request.url, `http://${request.headers.host || "localhost"}`);

  try {
    if (request.method === "GET" && url.pathname === "/") {
      return sendJson(response, 200, {
        name: "Task Tracker API",
        endpoints: [
          "GET /api/tasks",
          "POST /api/tasks",
          "PATCH /api/tasks/:id",
          "DELETE /api/tasks/:id",
        ],
      });
    }

    if (request.method === "GET" && url.pathname === "/api/tasks") {
      return sendJson(response, 200, { count: tasks.length, tasks });
    }

    if (request.method === "POST" && url.pathname === "/api/tasks") {
      const body = await readJson(request);
      if (typeof body.title !== "string" || body.title.trim() === "") {
        return sendJson(response, 400, { error: "title is required" });
      }

      const task = { id: nextId++, title: body.title.trim(), completed: false };
      tasks.push(task);
      return sendJson(response, 201, task);
    }

    const taskId = taskIdFrom(url.pathname);

    if (request.method === "PATCH" && taskId !== null) {
      const task = tasks.find((item) => item.id === taskId);
      if (!task) return sendJson(response, 404, { error: "task not found" });

      const body = await readJson(request);
      if (body.title !== undefined) {
        if (typeof body.title !== "string" || body.title.trim() === "") {
          return sendJson(response, 400, { error: "title must be a non-empty string" });
        }
        task.title = body.title.trim();
      }
      if (body.completed !== undefined) {
        if (typeof body.completed !== "boolean") {
          return sendJson(response, 400, { error: "completed must be a boolean" });
        }
        task.completed = body.completed;
      }
      return sendJson(response, 200, task);
    }

    if (request.method === "DELETE" && taskId !== null) {
      const taskIndex = tasks.findIndex((item) => item.id === taskId);
      if (taskIndex === -1) return sendJson(response, 404, { error: "task not found" });

      const [deletedTask] = tasks.splice(taskIndex, 1);
      return sendJson(response, 200, deletedTask);
    }

    return sendJson(response, 404, { error: "route not found" });
  } catch (error) {
    return sendJson(response, 400, { error: error.message });
  }
});

server.listen(port, "0.0.0.0", () => {
  console.log(`Task Tracker API running at http://localhost:${port}`);
});
