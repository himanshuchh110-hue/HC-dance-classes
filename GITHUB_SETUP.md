# GitHub Setup Instructions for HC Dance Classes

## Step 1: Install Git
Download and install Git from: https://git-scm.com/download/win
- Run the installer and follow the default options
- Restart your terminal/PowerShell after installation

## Step 2: Create GitHub Account
1. Go to https://github.com
2. Click "Sign up"
3. Create a free account
4. Verify your email

## Step 3: Create a New Repository on GitHub
1. Login to GitHub
2. Click the "+" icon in the top right
3. Select "New repository"
4. Fill in:
   - Repository name: `HC-dance-classes` (or your preferred name)
   - Description: "A full-stack dance classes booking website"
   - Public or Private (your choice)
   - Do NOT initialize with README (we already have one)
5. Click "Create repository"

## Step 4: Setup Git Locally
Open PowerShell and run these commands:

### Configure Git (first time only)
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"
```

### Navigate to your project
```powershell
cd "b:\HC dance classes"
```

### Initialize git and push to GitHub
```powershell
git init
git add .
git commit -m "Initial commit: HC Dance Classes website"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/HC-dance-classes.git
git push -u origin main
```

**Replace YOUR_USERNAME with your actual GitHub username**

## Step 5: Share Your Repository
Once pushed, your repository will be available at:
```
https://github.com/YOUR_USERNAME/HC-dance-classes
```

Share this link with anyone to show them your code!

## Step 6: Deploy Live (Optional)
To make your website accessible online, use:
- **Heroku** (free tier available)
- **PythonAnywhere** (free hosting for Flask apps)
- **Replit** (free cloud development)
- **GitHub Pages** (for static sites)

## Useful Git Commands

```powershell
# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push

# Pull latest changes
git pull
```

---

Need help? Reply with your GitHub username and I can guide you through any step!
