# STITCH.md — MediAgent Google Stitch Frontend Prompt

> Copy the prompt below verbatim into Google Stitch to generate the MediAgent frontend.  
> After generation, export as React + Tailwind and place in `frontend/src/`.

---

## Google Stitch Prompt

```
Build a premium, full-stack medical AI web application called "MediAgent" — a Multimodal Clinical Decision Support System. This is a portfolio-grade product for an AI/ML engineering student, so the design must look production-ready, not like a student project.

---

### BRAND & VISUAL IDENTITY

Name: MediAgent
Tagline: "Multimodal Clinical Intelligence"
Logo concept: A minimalist caduceus symbol merged with a neural network node, in deep blue.

Color Palette:
- Primary: #0A2540 (deep navy — trust, clinical authority)
- Accent: #2563EB (electric blue — technology, AI)
- Success: #10B981 (emerald green — safe/normal findings)
- Warning: #F59E0B (amber — moderate concern)
- Danger: #EF4444 (red — red flags, urgent)
- Surface: #F8FAFC (near-white background)
- Card: #FFFFFF (pure white cards)
- Muted: #64748B (secondary text)
- Border: #E2E8F0 (subtle borders)

Typography:
- Headings: Inter, weight 700
- Body: Inter, weight 400
- Monospace (for ICD codes, JSON trace): JetBrains Mono

Design Language:
- Medical-grade minimalism: clean whitespace, no decorative clutter
- Glassmorphism on modal overlays only (backdrop-blur, semi-transparent)
- Subtle drop shadows on cards (shadow-sm, not dramatic)
- Pill-shaped badges for tags (ICD codes, urgency levels, confidence)
- Smooth transitions: 200ms ease-in-out on hover states
- Radial progress indicators for confidence scores
- No gradients except subtle hero section gradient

---

### PAGE 1 — HOME / INPUT PAGE (Route: /)

Layout: Full-height split layout
- Left Panel (45% width): Input & Upload Zone
- Right Panel (55% width): Live Preview & Status

#### LEFT PANEL — Input Zone

Header:
- MediAgent logo (icon + wordmark) top-left
- "New Analysis" pill button top-right (clears form)

Section 1 — Medical Image Upload:
- Large drag-and-drop zone with dashed border
- Icon: stethoscope or X-ray icon in center
- Label: "Drop medical image here"
- Subtext: "X-ray, skin photo, retinal scan • JPG, PNG"
- On hover: border turns accent blue, background tints lightly
- On upload: show image thumbnail with overlay "✓ Image loaded"
- File size shown below thumbnail
- "Remove" X button on thumbnail

Section 2 — Lab Report Upload:
- Smaller upload zone, same drag-and-drop pattern
- Icon: document/PDF icon
- Label: "Upload Lab Report PDF"
- On upload: show filename + page count + "✓ Extracted" status chip
- Click to expand extracted text preview (collapsible panel, max 150px height with scroll)

Section 3 — Symptom Description:
- Label: "Describe Symptoms"
- Large textarea (min 4 rows) with placeholder:
  "e.g. Patient presents with high fever for 3 days, productive cough, and chest pain on deep breathing..."
- Character count bottom-right (e.g. "142 / 1000")
- OR divider separator below textarea

Section 4 — Voice Input:
- Voice recorder card with microphone icon
- "Record Symptoms" button (outlined, with mic icon)
- On recording: animated red pulsing dot + waveform visualization (CSS/SVG animated bars)
- "Stop & Transcribe" button appears while recording
- After transcription: editable text box appears with transcribed text
- Status: "Transcribed via Whisper AI ✓"

Analyze Button:
- Full-width, solid navy button: "Run Clinical Analysis →"
- Disabled state with tooltip if no inputs provided
- Loading state: spinner + "Analyzing... Vision Agent running"
- Progress indicator: 3-step pill progress bar
  "1. Vision Analysis → 2. Knowledge Retrieval → 3. Report Generation"

#### RIGHT PANEL — Live Preview & Model Status

Top Section — System Status Bar:
- 4 status pills in a row:
  - "LLaVA 13B" with green dot (active) or amber dot (loading)
  - "LLaMA 3.1 8B" with status dot
  - "ChromaDB" with status dot
  - "PubMed API" with status dot
- Clicking a pill shows a tooltip with model details

Middle Section — Input Preview:
- Before upload: illustrated empty state
  "Upload an image, a lab report, or describe symptoms to begin."
  Soft illustration of a clipboard with a heartbeat line.
- After image upload: image preview fills this panel with a label overlay
- After PDF upload: extracted text preview in monospace font
- After voice: waveform replay button + transcription preview

Bottom Section — Recent Analyses (in-memory, current session only):
- "Recent" label
- List of past analyses in this session (session storage only)
- Each item: timestamp + truncated summary + "View" chip

---

### PAGE 2 — RESULTS PAGE (Route: /results or modal overlay)

Trigger: After analysis completes, results slide up from bottom OR navigate to /results

Layout: Full-width results page with sticky header

Sticky Header:
- "MediAgent" wordmark left
- "New Analysis" button right
- Urgency badge center: pill with color-coded urgency
  - IMMEDIATE: red pill
  - URGENT: amber pill
  - SEMI-URGENT: yellow pill
  - ROUTINE: green pill

#### SECTION 1 — RED FLAGS (if any)

Full-width alert banner at top of results:
- Red background (#FEE2E2), red border-left (4px solid #EF4444)
- Icon: triangle warning icon
- Title: "⚠ Red Flags Detected"
- List of red flag items as bullet points
- "Seek immediate medical attention" footer text in bold
- Only shown if red_flags array is non-empty

#### SECTION 2 — Patient Summary Card

White card with thin navy left border (4px)
- Title: "Clinical Summary"
- Body: patient_summary text from report
- Metadata row: image type badge | urgency badge | timestamp

#### SECTION 3 — Differential Diagnosis (Main Section)

Title: "Differential Diagnosis"
Subtitle: "Ranked by AI confidence score"

For each diagnosis, render a DiagnosisCard:

DiagnosisCard Design:
- White card with subtle shadow
- Left column (20%):
  - Rank number (large, muted, e.g. "01")
  - Radial progress circle (confidence score %)
  - Color: green >75%, amber 50-75%, red <50%
- Right column (80%):
  - Condition name (large bold text)
  - ICD-10 code pill badge (monospace font, navy background, white text)
    e.g. "ICD J18.9"
  - Confidence percentage text (e.g. "87% confidence")
  - Collapsible section "View Evidence →":
    - Supporting findings as green checkmark list
    - Against findings as red X list
    - Clinical rationale text in italic

Cards are collapsed by default, expand on click with smooth animation.
Top card (rank 1) is pre-expanded.

#### SECTION 4 — Recommended Next Steps

White card
Title: "Recommended Investigations & Actions"
Numbered list of next steps
Each item has a category chip:
- "Lab Test" (blue)
- "Imaging" (purple)
- "Referral" (orange)
- "Monitoring" (green)
Categorize intelligently based on text content.

#### SECTION 5 — Evidence & Sources

White card
Title: "Supporting Medical Evidence"
Subtitle: "Retrieved from PubMed and MedQA knowledge base"
For each source: citation chip with PMID, clickable external link icon
Expandable abstract preview on click.

#### SECTION 6 — Additional History Needed

Muted card (light grey background)
Title: "To improve accuracy, gather:"
Bullet list of additional_history_needed items
Each item has a clipboard icon

#### SECTION 7 — Agent Trace Viewer (Collapsible)

Collapsed by default, "View Agent Reasoning Trace ↓" toggle button

When expanded:
- Timeline visualization of 3 agent nodes
  - Vision Agent: green checkmark + duration (e.g. "8.2s")
  - RAG Agent: green checkmark + duration
  - Report Agent: green checkmark + duration
- Total pipeline duration
- "View full trace on LangSmith →" external link button
- Token usage per agent as small monospace text

#### SECTION 8 — Export Bar (Sticky Bottom)

Sticky footer bar (white, top shadow):
- "Export Report:" label
- Three buttons: "PDF" | "Markdown" | "JSON"
- "Copy Link" button (copies session URL)
- Disclaimer text (small, muted): 
  "AI-generated for educational use only. Not a substitute for professional medical advice."

---

### PAGE 3 — SYSTEM STATUS PAGE (Route: /status)

Clean dashboard showing:
- Model cards in a 2x2 grid
  - Each card: model name, version, RAM usage, status (Active/Loading/Error)
- ChromaDB status: collection names + document count
- PubMed API: last successful call + rate limit remaining
- Whisper: model size loaded
- Recent errors log (last 10, collapsible)

---

### COMPONENT SPECIFICATIONS

#### Confidence Radial Component
SVG circle with stroke-dasharray animation
- Outer ring: light grey track
- Inner fill: animated fill arc colored by score
- Center text: percentage value
- Animation: fills from 0 to final value over 800ms on mount

#### Waveform Recorder Component
- CSS animated bars (20 bars, varying heights, animated while recording)
- Bars pulse with sine-wave-like animation
- Color: accent blue while recording, muted grey when stopped
- After recording: static bars showing "recording complete" state

#### ICD-10 Badge
- Pill shape, font: JetBrains Mono
- Navy background, white text
- Hover: lighter navy
- Click: copies ICD code to clipboard with toast notification

#### Status Pill
- Small pill with colored dot
- Green: active/healthy
- Amber: loading/warning
- Red: error/offline
- Grey: unknown
- Subtle pulse animation on amber (checking) state

#### Toast Notifications
- Bottom-right position
- Slide up animation
- Auto-dismiss after 3 seconds
- Types: success (green), error (red), info (blue), warning (amber)

---

### RESPONSIVE BEHAVIOR

Desktop (>1200px): Side-by-side input/preview layout
Tablet (768-1200px): Stacked layout, full-width panels
Mobile (<768px):
- Single column
- Upload zones stack vertically
- Diagnosis cards full width
- Export bar becomes scrollable row

---

### INTERACTIONS & MICRO-ANIMATIONS

- Upload zone: scale(1.02) + border color change on hover
- Analyze button: subtle scale(0.98) on click
- Diagnosis cards: smooth height transition on expand/collapse (300ms)
- Red flag banner: fade-in from top with slight slide (200ms)
- Results page: cards stagger-fade in sequentially (each 100ms apart)
- Confidence circle: fill animation on results load
- Status pills: gentle pulse on amber/loading state

---

### TECHNICAL REQUIREMENTS FOR EXPORT

- React 18+ with functional components and hooks
- Tailwind CSS for all styling (no CSS modules, no inline styles except dynamic values)
- Lucide React for all icons
- React Router v6 for routing
- Axios for API calls (base URL: http://localhost:8000)
- All API calls go to these endpoints:
  - POST /api/analyze (multipart form data)
  - POST /api/transcribe (audio file)
  - GET /api/models/status
  - GET /api/export/{sessionId}?format=pdf|markdown|json
- Use React Context for global state (current report, session history)
- All components in src/components/
- All pages in src/pages/
- API client in src/api/client.js
- No hardcoded mock data — always fetch from backend
- Loading skeletons (not spinners) for diagnosis cards while fetching

---

Generate all pages and components described above. Export as a complete React project structure.
```

---

## Post-Stitch Integration Notes

After generating from Stitch, make these adjustments before plugging into the repo:

1. **API Client** — Update `src/api/client.js` base URL to use env variable:
   ```js
   const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
   ```

2. **Voice Recording** — Stitch may generate a basic mic button. Enhance with:
   - `MediaRecorder` API for browser-native recording
   - Send audio as `audio/webm` blob to `/api/transcribe`

3. **File Uploads** — Ensure `multipart/form-data` headers are set correctly:
   ```js
   const formData = new FormData();
   formData.append('image', imageFile);
   formData.append('pdf', pdfFile);
   formData.append('symptoms', symptomsText);
   ```

4. **CORS** — Backend must allow `http://localhost:3000` (already in `CLAUDE.md`)

5. **Tailwind Config** — Add these custom colors to `tailwind.config.js`:
   ```js
   colors: {
     navy: { 900: '#0A2540', 800: '#0D2E4E' },
     'med-blue': '#2563EB',
     'med-green': '#10B981',
   }
   ```
