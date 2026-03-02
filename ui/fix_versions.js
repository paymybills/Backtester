const fs = require('fs');
const path = require('path');
const p = path.join(__dirname, 'src', 'components', 'ui');

fs.readdirSync(p).forEach(f => {
    if (!f.endsWith('.tsx')) return;
    const filePath = path.join(p, f);
    const content = fs.readFileSync(filePath, 'utf8');
    // Match `from "package@version"` and replace with `from "package"`
    const newContent = content.replace(/from\s+["']([^"']+)@\d+\.\d+\.\d+["']/g, 'from "$1"');
    if (content !== newContent) {
        fs.writeFileSync(filePath, newContent);
        console.log(`Updated ${f}`);
    }
});
