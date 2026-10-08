/** ATS primary identity. Semantic success/error/warning colors remain independent. */
export const bluePalette = {
  primary: "#1d4ed8",
  hover: "#1e40af",
  active: "#1e3a8a",
  focus: "#2563eb",
  soft: "#eff6ff",
  selected: "#dbeafe",
  border: "#93c5fd",
  onPrimary: "#ffffff",
} as const;

export const atsBlueTheme = {
  token: {
    colorPrimary: bluePalette.primary,
    colorPrimaryHover: bluePalette.hover,
    colorPrimaryActive: bluePalette.active,
    colorPrimaryBg: bluePalette.soft,
    colorPrimaryBgHover: bluePalette.selected,
    colorPrimaryBorder: bluePalette.border,
    colorLink: bluePalette.primary,
    colorLinkHover: bluePalette.hover,
    colorLinkActive: bluePalette.active,
    colorTextLightSolid: bluePalette.onPrimary,
    colorText: "#1d2129",
    colorTextSecondary: "#4e5969",
    colorBorder: "#e5e6eb",
    borderRadius: 4,
    fontSize: 14,
  },
};
