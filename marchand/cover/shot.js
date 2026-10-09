const puppeteer = require("/home/user/personalbrand/node_modules/puppeteer-core");
(async () => {
  const b = await puppeteer.launch({ executablePath: "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell",
    args: ["--no-sandbox", "--allow-file-access-from-files"] });
  const p = await b.newPage(); await p.setViewport({ width: 1080, height: 1920 });
  await p.goto("file://" + __dirname + "/cover.html", { waitUntil: "load" });
  await p.evaluate(() => document.fonts.ready.then(() => true));
  await p.screenshot({ path: __dirname + "/cover-marchand.png", clip: { x: 0, y: 0, width: 1080, height: 1920 } });
  await b.close();
})();
