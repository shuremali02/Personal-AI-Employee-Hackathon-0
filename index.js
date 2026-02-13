/**
 * Main entry point for Personal AI Employee
 */

require('dotenv').config();
const express = require('express');

// Initialize Express app
const app = express();
const PORT = process.env.MCP_SERVER_PORT || 8080;

// Middleware
app.use(express.json());

// Basic health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'operational',
    service: 'personal-ai-employee',
    timestamp: new Date().toISOString()
  });
});

// Main initialization function
async function initializeAIEmployee() {
  console.log('🚀 Starting Personal AI Employee...');
  console.log('Loading configuration...');

  // Initialize core components
  console.log('Initializing brain (Claude Code interface)...');
  console.log('Initializing memory (Obsidian vault)...');
  console.log('Initializing senses (watchers)...');
  console.log('Initializing hands (MCP servers)...');

  console.log(`\n✅ Personal AI Employee is operational!`);
  console.log(`Listening on port ${PORT}`);
}

// Start the server
app.listen(PORT, async () => {
  await initializeAIEmployee();
});