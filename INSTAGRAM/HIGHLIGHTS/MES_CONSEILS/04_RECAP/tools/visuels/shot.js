// node shot.js <name> : renders <name>.html (1080x1920) to ../../../03_VISUELS_FIXES/<name>.png
const puppeteer = require("/home/user/personalbrand/node_modules/puppeteer-core");
(async () => {
  const name = process.argv[2];
  const b = await puppeteer.launch({ executablePath: "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell",
    args: ["--no-sandbox", "--allow-file-access-from-files"] });
  const p = await b.newPage(); await p.setViewport({ width: 1080, height: 1920 });
  await p.goto("file://" + __dirname + "/" + name + ".html", { waitUntil: "load" });
  await p.evaluate(() => document.fonts.ready.then(() => true));
  await p.screenshot({ path: __dirname + "/../../../03_VISUELS_FIXES/" + name + ".png", clip: { x: 0, y: 0, width: 1080, height: 1920 } });
  await b.close();
})();
