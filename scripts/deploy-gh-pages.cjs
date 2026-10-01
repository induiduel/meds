const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const gitExe = '"C:\\Program Files\\Git\\cmd\\git.exe"';
const rootDir = path.resolve(__dirname, '..');
const distDir = path.join(rootDir, 'dist');
const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN || '';
const repoUrl = token 
  ? `https://${token}@github.com/induiduel/meds.git`
  : 'origin';

console.log('Deploying dist folder to gh-pages branch...');
process.chdir(distDir);

try {
  execSync(`${gitExe} init`);
  execSync(`${gitExe} config user.name "induiduel"`);
  execSync(`${gitExe} config user.email "nofrostlife@gmail.com"`);
  execSync(`${gitExe} add -A`);
  execSync(`${gitExe} commit -m "Deploy to GitHub Pages"`);
  execSync(`${gitExe} push -f ${repoUrl} master:gh-pages`);
  console.log('✅ Successfully deployed dist to gh-pages branch!');
} catch (e) {
  console.error('Deploy error:', e.message);
} finally {
  const gitDir = path.join(distDir, '.git');
  if (fs.existsSync(gitDir)) {
    fs.rmSync(gitDir, { recursive: true, force: true });
  }
}
