const lightColors = require("@primer/primitives/dist/json/colors/light.json");
const lightHighContrastColors = require("@primer/primitives/dist/json/colors/light_high_contrast.json");
const lightColorblindColors = require("@primer/primitives/dist/json/colors/light_colorblind.json");
const darkColors = require("@primer/primitives/dist/json/colors/dark.json");
const darkHighContrastColors = require("@primer/primitives/dist/json/colors/dark_high_contrast.json");
const darkColorblindColors = require("@primer/primitives/dist/json/colors/dark_colorblind.json");
const dimmedColors = require("@primer/primitives/dist/json/colors/dark_dimmed.json");

// A pristine copy of the dark primitives for the extra "Dark Purple" variant,
// cloned before getColors() mutates the shared dark object.
const darkPurpleColors = JSON.parse(JSON.stringify(darkColors));

// Shared "purplish" overrides for the dark-based themes (Dark and Dark Purple).
// `bg` provides the per-variant background ramp.
function applyDarkPurplish(c, bg) {
  // Temp override until Primitives are updated
  c.fg.default = "#e6edf3";
  c.fg.muted = "#7d8590";
  c.severe.subtle = "rgba(219, 109, 40, 0.1)";
  c.danger.subtle = "rgba(248, 81, 73, 0.1)";
  c.done.subtle = "rgba(163, 113, 247, 0.1)";
  c.sponsors.subtle = "rgba(219, 97, 162, 0.1)";

  // Purplish customizations (this fork)
  c.btn.primary.bg = "#8345ff";        // purple primary buttons
  c.btn.primary.hoverBg = "#9a63ff";
  c.success.fg = "#f78166";            // coral uncommitted-file decorations
  c.accent.fg = "#a371f7";             // purple UI accent (links, cursor, matched text, ...)
  c.accent.emphasis = "#8345ff";       // purple badges / progress / status focus
  c.accent.subtle = "rgba(131, 69, 255, 0.15)";

  // Background ramp (varies per variant)
  c.canvas.default = bg.default;
  c.canvas.inset = bg.inset;
  c.canvas.overlay = bg.overlay;
  c.canvas.subtle = bg.subtle;

  return c;
}

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
      // Purplish GitHub Dark — neutral near-black backgrounds
      return applyDarkPurplish(darkColors, {
        default: "#0d0d0d", inset: "#080808", overlay: "#0d0d0d", subtle: "#0d0d0d",
      });
    case "dark_purple":
      // Purplish GitHub Dark Purple — dark aubergine backgrounds
      return applyDarkPurplish(darkPurpleColors, {
        default: "#100d17", inset: "#0a0710", overlay: "#100d17", subtle: "#100d17",
      });
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
