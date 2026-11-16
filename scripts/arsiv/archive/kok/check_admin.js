const fs = require('fs');

const content = fs.readFileSync('src/components/AdminPanelModal.tsx', 'utf8');
const lines = content.split('\n');

// Find return ( around line 1068
let retLine = 0;
for (let i = 1000; i < lines.length; i++) {
  if (lines[i].includes('return (') || lines[i].includes('return(')) {
    retLine = i;
    break;
  }
}
console.log('Return line:', retLine + 1);

let depth = 0;
let inString = false;
let stringChar = '';
let inComment = false;

for (let i = retLine; i < lines.length; i++) {
  const line = lines[i];
  for (let c = 0; c < line.length; c++) {
    const ch = line[c];
    if (inComment) {
      if (ch === '*' && line[c + 1] === '/') {
        inComment = false;
        c++;
      }
    } else if (inString) {
      if (ch === stringChar && line[c - 1] !== '\\') inString = false;
    } else {
      if (ch === '/' && line[c + 1] === '*') {
        inComment = true;
        c++;
      } else if (ch === '/' && line[c + 1] === '/') {
        break; // rest of line is comment
      } else if (ch === '"' || ch === "'" || ch === '`') {
        inString = true;
        stringChar = ch;
      } else if (ch === '{') {
        depth++;
      } else if (ch === '}') {
        depth--;
        if (depth < 0) {
          console.log('Negative brace depth at line', i + 1, 'col', c + 1);
        }
      }
    }
  }
}
console.log('Final brace depth:', depth);
