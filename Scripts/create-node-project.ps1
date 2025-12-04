# ============================================
# CREATE NEW NODE.JS PROJECT
# ============================================

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectName,

    [Parameter(Mandatory=$false)]
    [ValidateSet("javascript", "typescript", "express", "react", "vue")]
    [string]$Template = "javascript"
)

$DevTools = "D:\DevTools"
$ProjectsDir = "$DevTools\Database"
$ProjectPath = "$ProjectsDir\$ProjectName"

Write-Host "Creating Node.js Project: $ProjectName" -ForegroundColor Cyan
Write-Host "Template: $Template" -ForegroundColor Gray
Write-Host ""

# Check if project exists
if (Test-Path $ProjectPath) {
    Write-Host "ERROR: Project '$ProjectName' already exists" -ForegroundColor Red
    exit 1
}

# Create project directory
New-Item -ItemType Directory -Path $ProjectPath -Force | Out-Null
Set-Location $ProjectPath

Write-Host "Initializing npm..." -ForegroundColor Yellow
npm init -y | Out-Null

# Configure based on template
switch ($Template) {
    "javascript" {
        Write-Host "Setting up JavaScript project..." -ForegroundColor Yellow

        # Install dev dependencies
        npm install --save-dev eslint prettier nodemon

        # Create .eslintrc.json
        @"
{
  "env": {
    "node": true,
    "es2021": true
  },
  "extends": "eslint:recommended",
  "parserOptions": {
    "ecmaVersion": "latest"
  }
}
"@ | Out-File -FilePath ".eslintrc.json" -Encoding UTF8

        # Create index.js
        @"
console.log('Hello from Node.js!');
"@ | Out-File -FilePath "index.js" -Encoding UTF8
    }

    "typescript" {
        Write-Host "Setting up TypeScript project..." -ForegroundColor Yellow

        # Install dependencies
        npm install --save-dev typescript @types/node ts-node nodemon

        # Create tsconfig.json
        npx tsc --init

        # Create src/index.ts
        New-Item -ItemType Directory -Path "src" -Force | Out-Null
        @"
console.log('Hello from TypeScript!');
"@ | Out-File -FilePath "src/index.ts" -Encoding UTF8
    }

    "express" {
        Write-Host "Setting up Express.js project..." -ForegroundColor Yellow

        # Install dependencies
        npm install express
        npm install --save-dev nodemon

        # Create index.js
        @"
const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'Hello from Express!' });
});

app.listen(PORT, () => {
  console.log(\`Server running on http://localhost:\${PORT}\`);
});
"@ | Out-File -FilePath "index.js" -Encoding UTF8
    }
}

# Create .gitignore
@"
node_modules/
.env
*.log
dist/
build/
.DS_Store
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8

# Create README
@"
# $ProjectName

Created with DevTools

## Installation

\`\`\`bash
npm install
\`\`\`

## Usage

\`\`\`bash
npm start
\`\`\`
"@ | Out-File -FilePath "README.md" -Encoding UTF8

Write-Host ""
Write-Host "Project created successfully!" -ForegroundColor Green
Write-Host "Location: $ProjectPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  cd $ProjectPath" -ForegroundColor Gray
Write-Host "  npm install" -ForegroundColor Gray
Write-Host "  npm start" -ForegroundColor Gray
