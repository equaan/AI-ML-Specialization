```markdown
# Design System Strategy: The Precision Sentinel

This document defines the visual and structural standards for the design system. Our goal is to move beyond generic medical interfaces and create an environment of **Clinical Authority**. We are building a "Precision Sentinel"—a system that feels as reliable as a surgeon and as intelligent as a neural network.

The aesthetic is characterized by **High-End Editorial Minimalism**: a rejection of cluttered grids in favor of purposeful whitespace, tonal layering, and sophisticated typography.

---

## 1. Creative North Star: The Precision Sentinel
In the medical-AI space, trust is earned through clarity and restraint. We avoid the "tech-bro" vibrance of typical AI apps. Instead, we use a monochromatic foundation of Deep Navy with surgical strikes of Electric Blue. 

To break the "template" look:
*   **Intentional Asymmetry:** Avoid perfectly centered layouts. Shift content to a 60/40 or 70/30 split to create an editorial feel.
*   **Atmospheric Depth:** We do not use lines to separate ideas. We use "air" (whitespace) and "tone" (background shifts).
*   **Data as Art:** Use JetBrains Mono to treat medical data with the reverence of code, making it feel "computed" and "exact."

---

## 2. Color & Surface Architecture

### The Palette
We utilize a Material-inspired token system but apply it with editorial strictness.
*   **Primary (`#000f22`):** The "Deep Navy" anchor. Used for high-level navigation and authoritative headers.
*   **Secondary (`#0051d5`):** The "Electric Blue" pulse. Use this exclusively for primary actions and AI-driven insights.
*   **Tertiary (`#001209` / `#009e6d`):** The "Success Emerald" range. Used for healthy vitals and positive diagnoses.

### The "No-Line" Rule
**Explicit Instruction:** Designers are prohibited from using 1px solid borders for sectioning content. Boundaries must be defined through:
1.  **Background Color Shifts:** A `surface-container-low` component sitting on a `surface` background.
2.  **Tonal Transitions:** Moving from `surface-container-highest` to `surface-bright` to define a sidebar.

### Glass & Gradient Signature
To ensure the system feels "cutting-edge," use Glassmorphism for **overlays only** (Modals, Popovers, Floating Action Menus). 
*   **Token:** Use `surface` at 70% opacity with a `24px` backdrop-blur. 
*   **Gradients:** Main CTAs may use a subtle linear gradient from `primary` to `primary-container` (top-to-bottom) to add a "metallic" clinical polish.

---

## 3. Typography: The Human & The Machine

We pair two distinct typefaces to create a tension between care and computation.

*   **Inter (The UI & Headings):** This is our "Human" voice. 
    *   **Display Scales:** Use `display-lg` with `-0.02em` tracking for a high-end, confident header feel.
    *   **Hierarchy:** Keep a high contrast between `headline-lg` and `body-md`. Do not fear large gaps in scale; it signals authority.
*   **JetBrains Mono (The Clinical Data):** This is our "Machine" voice.
    *   **Usage:** Mandatory for patient IDs, lab results, clinical codes, and timestamps.
    *   **Psychology:** It signals to the practitioner that this data is raw, precise, and untampered by human error.

---

## 4. Elevation & Depth: Tonal Layering

Traditional drop shadows are too "software-standard." We use **Tonal Layering**.

*   **The Layering Principle:** Stack surfaces to create hierarchy.
    *   *Base:* `surface`
    *   *Content Section:* `surface-container-low`
    *   *Interactive Card:* `surface-container-lowest` (this creates a "lift" through brightness rather than shadow).
*   **Ambient Shadows:** If a floating element (like a context menu) requires a shadow, use a "Cloud Shadow": `Y: 12px, Blur: 32px, Color: On-Surface @ 6%`. It should feel like a soft glow of light, not a dark smudge.
*   **The Ghost Border:** For high-density data where separation is vital, use an `outline-variant` token at **15% opacity**. It should be barely visible—a "ghost" of a line.

---

## 5. Components

### Buttons
*   **Primary:** Pill-shaped (`rounded-full`). Background: `secondary`. Text: `on-secondary`. No shadow.
*   **Secondary:** Pill-shaped. Background: `primary-container`. Text: `primary-fixed`. 
*   **Tertiary (The Editorial Link):** No background. `label-md` uppercase with `0.05em` tracking.

### Cards & Data Containers
*   **Rule:** Forbid divider lines. 
*   **Structure:** Use vertical white space (`1.5rem` to `2.5rem`) to separate content blocks. 
*   **Surface:** Use `surface-container-low`. For hover states, shift to `surface-container-high`.

### Input Fields
*   **Style:** Subtle. Use `surface-container-highest` as the background with a `sm` (0.125rem) corner radius. 
*   **Focus:** Transition the background to `surface-container-lowest` and add a `2px` "Electric Blue" (`secondary`) underline. Do not use a full-box stroke.

### Pill-Shaped Badges
*   Used for status (Active, Pending, Critical). 
*   **Coloring:** Use the `container` and `on-container` pairs (e.g., `error-container` background with `on-error-container` text).

---

## 6. Do's and Don'ts

### Do:
*   **Embrace "Dead Space":** If a screen feels empty, resist the urge to fill it. High-end medical tools prioritize focus over density.
*   **Align to the Data:** Use JetBrains Mono for anything that could be misinterpreted (numbers 0/O, 1/l).
*   **Use Subtle Animation:** Interactions should feel like "opening a heavy door"—smooth, dampened, and deliberate.

### Don't:
*   **Don't use 100% Black:** Use `primary` (`#000f22`) for your darkest tones. It maintains the "Navy" brand identity.
*   **Don't use Rounded-MD for everything:** Use `rounded-full` for badges and buttons, but keep containers at `rounded-lg` or `rounded-xl` for a structured, architectural feel.
*   **Don't use traditional "Dividers":** If you think you need a line, try adding `32px` of space or a slight background color shift instead.