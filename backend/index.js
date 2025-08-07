import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import pkg from "pg";

dotenv.config();

const { Pool } = pkg;
const app = express();
const port = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Postgres connection pool
const pool = new Pool({
  user: process.env.PG_USER,
  host: process.env.PG_HOST,
  database: process.env.PG_DATABASE,
  password: process.env.PG_PASSWORD,
  port: process.env.PG_PORT,
});

// Initialize user schema and table
async function initializeUserSchema() {
  try {
    // Create user schema if it doesn't exist
    await pool.query(`CREATE SCHEMA IF NOT EXISTS "user"`);
    
    // Create users table if it doesn't exist
    await pool.query(`
      CREATE TABLE IF NOT EXISTS "user".users (
        email VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        api_key VARCHAR(255),
        api_secret VARCHAR(255),
        assigned_strategies JSONB DEFAULT '[]'::jsonb,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    
    console.log("User schema and table initialized successfully");
  } catch (err) {
    console.error("Error initializing user schema:", err);
  }
}

// Initialize on startup
initializeUserSchema();

// API endpoint to fetch all strategies
app.get("/api/strategies", async (req, res) => {
  try {
    const result = await pool.query("SELECT * FROM public.strategies_config");
    const strategies = result.rows;

    const strategiesWithPnl = await Promise.all(
      strategies.map(async (strategy) => {
        try {
          const tableName = `backtest.${strategy.name}`;
          const pnlResult = await pool.query(`
            SELECT pnl_sum FROM ${tableName}
            ORDER BY datetime DESC
            LIMIT 1
          `);

          const lastPnl = pnlResult.rows[0]?.pnl_sum ?? null;

          return {
            ...strategy,
            pnl: lastPnl,
          };
        } catch (err) {
          console.error(`Error fetching P&L for ${strategy.name}:`, err.message);
          return {
            ...strategy,
            pnl: null,
          };
        }
      })
    );

    res.json(strategiesWithPnl);
  } catch (err) {
    console.error("Error fetching strategies:", err);
    res.status(500).json({ error: "Failed to fetch strategies" });
  }
});

// API endpoint to fetch strategy details and ledger
app.get("/api/strategies/:strategyName", async (req, res) => {
  try {
    const { strategyName } = req.params;

    // Get strategy config
    const configResult = await pool.query(
      "SELECT * FROM public.strategies_config WHERE name = $1",
      [strategyName]
    );

    if (configResult.rows.length === 0) {
      return res.status(404).json({ error: "Strategy not found" });
    }

    const strategy = configResult.rows[0];

    // Get backtest data (ledger)
    const tableName = `backtest.${strategyName}`;
    const ledgerResult = await pool.query(`
      SELECT * FROM ${tableName}
      ORDER BY datetime ASC
    `);

    // Get latest PnL
    const latestPnlResult = await pool.query(`
      SELECT pnl_sum FROM ${tableName}
      ORDER BY datetime DESC
      LIMIT 1
    `);

    res.json({
      strategy,
      ledger: ledgerResult.rows,
      currentPnl: latestPnlResult.rows[0]?.pnl_sum || 0,
    });
  } catch (err) {
    console.error("Error fetching strategy details:", err);
    res.status(500).json({ error: "Failed to fetch strategy details" });
  }
});

// API endpoint to fetch strategy metrics
app.get("/api/strategy-metrics", async (req, res) => {
  try {
    const { strategy } = req.query;

    if (!strategy) {
      return res.status(400).json({ error: "Strategy name is required" });
    }

    console.log(`Fetching metrics for strategy: ${strategy}`);

    // Check if the stats schema exists
    const schemaCheck = await pool.query(`
      SELECT EXISTS (
        SELECT 1 FROM information_schema.schemata
        WHERE schema_name = 'stats'
      )
    `);

    if (!schemaCheck.rows[0].exists) {
      console.log("Stats schema does not exist");
      return res.status(404).json({ error: "Stats schema not found. Please run stats generation first." });
    }

    // Check if the strategy_stats table exists
    const tableCheck = await pool.query(`
      SELECT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'stats' AND table_name = 'strategy_stats'
      )
    `);

    if (!tableCheck.rows[0].exists) {
      console.log("Stats table does not exist");
      return res.status(404).json({ error: "Stats table not found. Please run stats generation first." });
    }

    // Fetch metrics from stats.strategy_stats table
    const metricsResult = await pool.query(`
      SELECT * FROM stats.strategy_stats
      WHERE strategy_name = $1
      ORDER BY created_at DESC
      LIMIT 1
    `, [strategy]);

    console.log(`Found ${metricsResult.rows.length} metrics records for ${strategy}`);

    if (metricsResult.rows.length === 0) {
      return res.status(404).json({ error: "No metrics found for this strategy" });
    }

    const metrics = metricsResult.rows[0];

    // Remove the strategy_name and created_at fields from the response
    delete metrics.strategy_name;
    delete metrics.created_at;

    console.log("Returning metrics:", Object.keys(metrics));
    res.json(metrics);
  } catch (err) {
    console.error("Error fetching strategy metrics:", err);
    res.status(500).json({ error: "Failed to fetch strategy metrics" });
  }
});

// USER MANAGEMENT ENDPOINTS

// Get all users
app.get("/api/users", async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT email, name, api_key, assigned_strategies, created_at, updated_at 
      FROM "user".users 
      ORDER BY created_at DESC
    `);
    res.json(result.rows);
  } catch (err) {
    console.error("Error fetching users:", err);
    res.status(500).json({ error: "Failed to fetch users" });
  }
});

// Add new user
app.post("/api/users", async (req, res) => {
  try {
    const { name, email, password, api_key, api_secret, assigned_strategies } = req.body;

    // Validate required fields
    if (!name || !email || !password) {
      return res.status(400).json({ error: "Name, email, and password are required" });
    }

    // Check if user already exists
    const existingUser = await pool.query(
      'SELECT email FROM "user".users WHERE email = $1',
      [email]
    );

    if (existingUser.rows.length > 0) {
      return res.status(409).json({ error: "User with this email already exists" });
    }

    // Insert new user
    const result = await pool.query(`
      INSERT INTO "user".users (name, email, password, api_key, api_secret, assigned_strategies)
      VALUES ($1, $2, $3, $4, $5, $6)
      RETURNING email, name, api_key, assigned_strategies, created_at
    `, [name, email, password, api_key, api_secret, JSON.stringify(assigned_strategies || [])]);

    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error("Error adding user:", err);
    res.status(500).json({ error: "Failed to add user" });
  }
});

// Delete user
app.delete("/api/users/:email", async (req, res) => {
  try {
    const { email } = req.params;

    const result = await pool.query(
      'DELETE FROM "user".users WHERE email = $1 RETURNING email',
      [email]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: "User not found" });
    }

    res.json({ message: "User deleted successfully", email: result.rows[0].email });
  } catch (err) {
    console.error("Error deleting user:", err);
    res.status(500).json({ error: "Failed to delete user" });
  }
});

// Get available strategies for assignment (grouped by symbol to prevent duplicates)
app.get("/api/strategies/available", async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT name, symbol, exchange, time_horizon 
      FROM public.strategies_config 
      ORDER BY symbol, name
    `);
    
    // Group strategies by symbol
    const strategiesBySymbol = result.rows.reduce((acc, strategy) => {
      if (!acc[strategy.symbol]) {
        acc[strategy.symbol] = [];
      }
      acc[strategy.symbol].push(strategy);
      return acc;
    }, {});

    res.json(strategiesBySymbol);
  } catch (err) {
    console.error("Error fetching available strategies:", err);
    res.status(500).json({ error: "Failed to fetch available strategies" });
  }
});

// Health check endpoint
app.get("/", (req, res) => {
  res.send("Strategies backend is running!");
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
