const lightColors = require("@primer/primitives/dist/json/colors/light.json");
const lightHighContrastColors = require("@primer/primitives/dist/json/colors/light_high_contrast.json");
const lightColorblindColors = require("@primer/primitives/dist/json/colors/light_colorblind.json");
const darkColors = require("@primer/primitives/dist/json/colors/dark.json");
const darkHighContrastColors = require("@primer/primitives/dist/json/colors/dark_high_contrast.json");
const darkColorblindColors = require("@primer/primitives/dist/json/colors/dark_colorblind.json");
const dimmedColors = require("@primer/primitives/dist/json/colors/dark_dimmed.json");

function getColors(theme) {

  switch(theme) {
    case "light":

      // Temp override until Primitives are updated
      lightColors.fg.default = "#1f2328";
      lightColors.fg.muted = "#656d76";

      // Purplish customizations (this fork) — same accents as the dark theme:
      // Primary (formerly green) buttons -> purple
      lightColors.btn.primary.bg = "#8345ff";
      lightColors.btn.primary.hoverBg = "#7437e8";
      // Uncommitted files (untracked + added git decorations) -> coral instead of green
      lightColors.success.fg = "#f78166";
      // Blue UI accents -> purple (same set as the dark theme)
      lightColors.accent.fg = "#8345ff";
      lightColors.accent.emphasis = "#8345ff";
      lightColors.accent.subtle = "#efe7ff";

      return lightColors;
    case "light_high_contrast":
      return lightHighContrastColors;
    case "light_colorblind":
        return lightColorblindColors;
    case "dark":

      // Temp override until Primitives are updated
      darkColors.fg.default = "#e6edf3";
      darkColors.fg.muted = "#7d8590";
      darkColors.severe.subtle = "rgba(219, 109, 40, 0.1)";
      darkColors.danger.subtle = "rgba(248, 81, 73, 0.1)";
      darkColors.done.subtle = "rgba(163, 113, 247, 0.1)";
      darkColors.sponsors.subtle = "rgba(219, 97, 162, 0.1)";

      // Purplish customizations (this fork only):
      // Primary (formerly green) buttons -> purple
      darkColors.btn.primary.bg = "#8345ff";
      darkColors.btn.primary.hoverBg = "#9a63ff";
      // Editor / right-side background -> dark purple base
      darkColors.canvas.default = "#100d17";
      // Explorer / left sidebar -> darker shade of the same purple
      darkColors.canvas.inset = "#0a0710";
      // Overlays/popups (dropdowns, Command Palette, widgets, notifications) -> same base for a uniform surface
      darkColors.canvas.overlay = "#100d17";
      darkColors.canvas.subtle = "#100d17";
      // Uncommitted files (untracked + added git decorations) -> coral instead of green
      darkColors.success.fg = "#f78166";
      // Blue UI accents -> purple (badges, progress bar, links, list focus,
      // matched-text highlight, text cursor, text selection, status focus, ...)
      darkColors.accent.fg = "#a371f7";
      darkColors.accent.emphasis = "#8345ff";
      darkColors.accent.subtle = "rgba(131, 69, 255, 0.15)";

      return darkColors;
    case "dark_high_contrast":
      return darkHighContrastColors;
    case "dark_colorblind":
      return darkColorblindColors;
    case "dark_dimmed":
      return dimmedColors;
    default:
      throw new Error(`Colors are missing for value: ${theme}`);
  }
}

module.exports = {
  getColors,
};
