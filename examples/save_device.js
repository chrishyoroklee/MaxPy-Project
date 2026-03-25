const maxApi = require("max-api");
const fs = require("fs");
const path = require("path");
const os = require("os");

maxApi.addHandler("save_amxd", (b64) => {
  try {
    const buf = Buffer.from(b64, "base64");
    const savePath = path.join(
      os.homedir(),
      "Desktop",
      "generated_device.amxd"
    );
    fs.writeFileSync(savePath, buf);
    maxApi.outlet("saved", savePath);
  } catch (e) {
    maxApi.outlet("error", String(e));
  }
});
