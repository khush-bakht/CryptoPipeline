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

// API endpoint to fetch all strategies
app.get("/api/strategies", async (req, res) => {
    try {
      const result = await pool.query("SELECT * FROM public.strategies_config")
      const strategies = result.rows
  
      const strategiesWithPnl = await Promise.all(
        strategies.map(async (strategy) => {
          try {
            const tableName = `backtest.${strategy.name}` 
            const pnlResult = await pool.query(`
              SELECT pnl_sum FROM ${tableName}
              ORDER BY datetime DESC
              LIMIT 1
            `)
  
            const lastPnl = pnlResult.rows[0]?.pnl_sum ?? null
  
            return {
              ...strategy,
              pnl: lastPnl,
            }
          } catch (err) {
            console.error(`Error fetching P&L for ${strategy.name}:`, err.message)
            return {
              ...strategy,
              pnl: null, 
            }
          }
        })
      )
  
      res.json(strategiesWithPnl)
    } catch (err) {
      console.error("Error fetching strategies:", err)
      res.status(500).json({ error: "Failed to fetch strategies" })
    }
  })
  
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
      currentPnl: latestPnlResult.rows[0]?.pnl_sum || 0
    });
    
  } catch (err) {
    console.error("Error fetching strategy details:", err);
    res.status(500).json({ error: "Failed to fetch strategy details" });
  }
});

// Health check endpoint
app.get("/", (req, res) => {
  res.send("Strategies backend is running!");
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});