import flet as ft

# ============================================================
#  Theme v2: "Ledger Light" — a clean, no-black fintech palette.
#  Light body (off-white / white cards) with a navy→teal
#  gradient "hero" header, exactly like modern banking apps
#  (dark accent band on top, airy white content below).
# ============================================================

# ---- Base surfaces (light) ----
BG = "#F4F7FB"              # App background — soft off-white blue-grey
SURFACE = "#FFFFFF"          # Cards / tiles / fields
SURFACE_ALT = "#EEF2F8"      # Muted surface (icon chips, inputs backdrop)
BORDER = "#E1E7F0"           # Hairline borders

# ---- Header / hero band (navy → teal gradient, never black) ----
NAVY = "#123A5E"
NAVY_LIGHT = "#1E5C8A"
GRADIENT_HEADER = ["#0F2E4C", "#0E7C66"]   # navy -> emerald-teal, diagonal

# ---- Brand colors ----
PRIMARY = "#0E9F6E"          # Emerald green — growth / positive
PRIMARY_DARK = "#0B7A54"
PRIMARY_LIGHT = "#4ADE80"
PRIMARY_SOFT = "#D9F7E7"

GOLD = "#D9A441"             # Savings / donations / highlights
GOLD_DARK = "#B07C22"        # Readable gold-on-white variant
GOLD_SOFT = "#FBEBC7"

DANGER = "#DC2626"           # Withdrawals / pending / errors
DANGER_SOFT = "#FDE3E3"

# ---- Text ----
TEXT_PRIMARY = "#0F2E4C"     # Deep navy — reads as ink, never black
TEXT_SECONDARY = "#5B6B82"
TEXT_MUTED = "#93A0B3"

# ---- Text/icons that sit ON TOP of the navy/teal header gradient ----
ON_HEADER = "#FFFFFF"
ON_HEADER_MUTED = "#CFEAE0"

GRADIENT_TILE = ["#FFFFFF", "#F7FAFC"]      # subtle card gradient


def base_theme() -> ft.Theme:
    return ft.Theme(
        font_family="font",
        color_scheme=ft.ColorScheme(
            primary=PRIMARY,
            secondary=GOLD,
            background=BG,
            surface=SURFACE,
            error=DANGER,
        ),
    )
