const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const gitExe = '"C:\\Program Files\\Git\\cmd\\git.exe"';
const rootDir = path.resolve(__dirname, '..');
const distDir = path.join(rootDir, 'dist');
const parentRemote = execSync(`${gitExe} remote get-url origin`, { cwd: rootDir }).toString().trim();
const repoUrl = process.env.GITHUB_TOKEN
  ? `https://${process.env.GITHUB_TOKEN}@github.com/induiduel/meds.git`
  : parentRemote;

console.log('Deploying dist folder to gh-pages branch...');
process.chdir(distDir);

try {
  fs.writeFileSync(path.join(distDir, '.nojekyll'), '');
  if (fs.existsSync(path.join(distDir, 'index.html'))) {
    fs.copyFileSync(path.join(distDir, 'index.html'), path.join(distDir, '404.html'));
  }
  execSync(`${gitExe} init`);
  execSync(`${gitExe} config user.name "induiduel"`);
  execSync(`${gitExe} config user.email "nofrostlife@gmail.com"`);
  execSync(`${gitExe} add -A`);
  execSync(`${gitExe} commit -m "Deploy to GitHub Pages"`);
  execSync(`${gitExe} push -f ${repoUrl} HEAD:gh-pages`);
  console.log('✅ Successfully deployed dist to gh-pages branch!');
} catch (e) {
  console.error('Deploy error:', e.message);
} finally {
  const gitDir = path.join(distDir, '.git');
  if (fs.existsSync(gitDir)) {
    fs.rmSync(gitDir, { recursive: true, force: true });
  }
}
