/**
 * PM2 Process Management Configuration for Personal AI Employee
 *
 * This configuration file defines how to run the various services and watchers
 * that make up the Personal AI Employee system.
 */

module.exports = {
  apps: [
    {
      name: 'mcp-servers',
      script: './.mcp/start-servers.sh',
      cwd: './',
      interpreter: '/bin/bash',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PORT: 8080
      },
      error_file: './logs/mcp-error.log',
      out_file: './logs/mcp-out.log',
      log_file: './logs/mcp-combined.log'
    },
    {
      name: 'gmail-watcher',
      script: './watchers/gmail-watcher.py',
      interpreter: 'python3',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '512M',
      env: {
        PYTHONPATH: './',
        NODE_ENV: 'production'
      },
      error_file: './logs/gmail-error.log',
      out_file: './logs/gmail-out.log',
      log_file: './logs/gmail-combined.log'
    },
    {
      name: 'whatsapp-watcher',
      script: './watchers/whatsapp-watcher.py',
      interpreter: 'python3',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '512M',
      env: {
        PYTHONPATH: './',
        NODE_ENV: 'production'
      },
      error_file: './logs/whatsapp-error.log',
      out_file: './logs/whatsapp-out.log',
      log_file: './logs/whatsapp-combined.log'
    },
    {
      name: 'finance-watcher',
      script: './watchers/finance-watcher.py',
      interpreter: 'python3',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '512M',
      env: {
        PYTHONPATH: './',
        NODE_ENV: 'production'
      },
      error_file: './logs/finance-error.log',
      out_file: './logs/finance-out.log',
      log_file: './logs/finance-combined.log'
    }
  ],

  deploy: {
    production: {
      user: 'user',
      host: 'your-server.com',
      ref: 'origin/main',
      repo: 'git@github.com:username/personal-ai-employee.git',
      path: '/var/www/personal-ai-employee',
      'post-deploy': 'npm install && pm2 reload ecosystem.config.js --env production'
    }
  }
};