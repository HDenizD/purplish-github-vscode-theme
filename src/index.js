const fs = require("fs").promises;
const getTheme = require("./theme");

const lightDefaultTheme = getTheme({
  theme: "light",
  name: "Purplish GitHub Light",
});

const darkDefaultTheme = getTheme({
  theme: "dark",
  name: "Purplish GitHub Dark",
});

// Write themes

fs.mkdir("./themes", { recursive: true })
  .then(() => Promise.all([
    fs.writeFile("./themes/light-default.json", JSON.stringify(lightDefaultTheme, null, 2)),
    fs.writeFile("./themes/dark-default.json", JSON.stringify(darkDefaultTheme, null, 2)),
  ]))
  .catch(() => process.exit(1))
