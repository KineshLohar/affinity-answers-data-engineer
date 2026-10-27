const mysql = require("mysql2/promise");
const readline = require("node:readline/promises");
const { stdin: input, stdout: output } = require("node:process");

const connectionOptions = {
  host: "mysql-rfam-public.ebi.ac.uk",
  port: 4497,
  user: "rfamro",
  password: "",
  database: "Rfam",
  connectTimeout: 15000,
  // Rfam's public account is read-only. Do not use this console for writes.
};

function printRows(rows, fields) {
  if (!fields || fields.length === 0) {
    console.log("Query completed.");
    return;
  }

  if (rows.length === 0) {
    console.log("(0 rows)");
    return;
  }

  const columns = fields.map((field) => field.name);
  const values = rows.map((row) =>
    columns.map((column) => {
      const value = row[column];
      return value === null || value === undefined ? "NULL" : String(value);
    })
  );

  const widths = columns.map((column, index) =>
    Math.min(
      48,
      Math.max(
        column.length,
        ...values.map((row) => row[index].length)
      )
    )
  );

  const formatRow = (row) =>
    row
      .map((value, index) => {
        const clipped =
          value.length > widths[index]
            ? `${value.slice(0, widths[index] - 1)}…`
            : value;
        return clipped.padEnd(widths[index]);
      })
      .join(" | ");

  console.log(formatRow(columns));
  console.log(widths.map((width) => "-".repeat(width)).join("-+-"));
  for (const row of values) {
    console.log(formatRow(row));
  }
  console.log(`\n(${rows.length} row(s))`);
}

async function main() {
  console.log("Rfam SQL Terminal (Node.js)");
  console.log("Connecting to the public, read-only Rfam database...");

  let connection;
  try {
    connection = await mysql.createConnection(connectionOptions);
  } catch (error) {
    console.error(`\nConnection failed: ${error.message}`);
    console.error(
      "Check your internet connection. Some networks block outbound connections to port 4497."
    );
    process.exitCode = 1;
    return;
  }

  console.log("Connected.");
  console.log("Enter SQL statements ending with a semicolon (;).");
  console.log("Commands: help, exit, quit\n");

  const rl = readline.createInterface({ input, output });
  let statement = [];

  try {
    while (true) {
      let line;
      try {
        line = await rl.question(statement.length ? "...  " : "SQL> ");
      } catch {
        break;
      }

      const trimmed = line.trim();

      if (statement.length === 0 && ["exit", "quit"].includes(trimmed.toLowerCase())) {
        break;
      }

      if (statement.length === 0 && trimmed.toLowerCase() === "help") {
        console.log("Examples:");
        console.log("  SHOW TABLES;");
        console.log("  DESCRIBE taxonomy;");
        console.log("  SELECT * FROM taxonomy LIMIT 5;");
        console.log("Type exit or quit to disconnect.\n");
        continue;
      }

      statement.push(line);
      if (!trimmed.endsWith(";")) continue;

      const sql = statement.join("\n").trim();
      statement = [];

      if (sql === ";") continue;

      // The public account is read-only. Keep the console for inspection queries.
      const firstKeyword = sql.replace(/^(?:\s|--[^\n]*\n|\/\*[\s\S]*?\*\/)+/g, "")
        .split(/\s+/)[0]
        ?.replace(/;$/, "")
        .toUpperCase();

      if (!["SELECT", "SHOW", "DESCRIBE", "DESC", "EXPLAIN", "WITH"].includes(firstKeyword)) {
        console.log("This practice console only allows read-only query types: SELECT, SHOW, DESCRIBE, EXPLAIN, and WITH.");
        console.log("Try a read-only query instead.\n");
        continue;
      }

      try {
        const [rows, fields] = await connection.query(sql);
        printRows(rows, fields);
      } catch (error) {
        console.error(`SQL error: ${error.message}`);
      }
      console.log();
    }
  } finally {
    rl.close();
    await connection.end();
    console.log("Disconnected from Rfam.");
  }
}

main().catch((error) => {
  console.error(`Unexpected error: ${error.message}`);
  process.exitCode = 1;
});
