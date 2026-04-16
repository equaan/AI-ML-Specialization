<!-- Agent Reasoning Trace Explorer -->
<!DOCTYPE html>

<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Detailed Trace Explorer | MediAgent</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    "surface-tint": "#49607e",
                    "on-surface": "#191c1e",
                    "on-secondary-fixed-variant": "#003ea8",
                    "surface-container-high": "#e6e8ea",
                    "on-tertiary": "#ffffff",
                    "on-surface-variant": "#43474d",
                    "inverse-surface": "#2d3133",
                    "on-secondary-container": "#fefcff",
                    "primary": "#000f22",
                    "primary-container": "#0a2540",
                    "surface": "#f7f9fb",
                    "on-tertiary-container": "#009e6d",
                    "surface-container-low": "#f2f4f6",
                    "on-primary": "#ffffff",
                    "on-background": "#191c1e",
                    "on-primary-fixed-variant": "#314865",
                    "tertiary": "#001209",
                    "surface-container-lowest": "#ffffff",
                    "secondary": "#0051d5",
                    "on-error-container": "#93000a",
                    "error": "#ba1a1a",
                    "on-secondary": "#ffffff",
                    "on-primary-fixed": "#001c37",
                    "tertiary-fixed-dim": "#4edea3",
                    "secondary-container": "#316bf3",
                    "error-container": "#ffdad6",
                    "surface-container-highest": "#e0e3e5",
                    "surface-bright": "#f7f9fb",
                    "tertiary-fixed": "#6ffbbe",
                    "inverse-on-surface": "#eff1f3",
                    "on-secondary-fixed": "#00174b",
                    "on-primary-container": "#768dad",
                    "secondary-fixed": "#dbe1ff",
                    "background": "#f7f9fb",
                    "surface-variant": "#e0e3e5",
                    "surface-container": "#eceef0",
                    "outline": "#74777e",
                    "on-error": "#ffffff",
                    "inverse-primary": "#b0c8eb",
                    "primary-fixed": "#d2e4ff",
                    "secondary-fixed-dim": "#b4c5ff",
                    "on-tertiary-fixed-variant": "#005236",
                    "on-tertiary-fixed": "#002113",
                    "tertiary-container": "#002a1a",
                    "surface-dim": "#d8dadc",
                    "primary-fixed-dim": "#b0c8eb",
                    "outline-variant": "#c4c6ce"
            },
            "borderRadius": {
                    "DEFAULT": "0.125rem",
                    "lg": "0.25rem",
                    "xl": "0.5rem",
                    "full": "0.75rem"
            },
            "fontFamily": {
                    "headline": ["Inter"],
                    "body": ["Inter"],
                    "label": ["Inter"],
                    "mono": ["JetBrains Mono"]
            }
          },
        }
      }
    </script>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .trace-line::before {
            content: '';
            position: absolute;
            left: 20px;
            top: 40px;
            bottom: -20px;
            width: 2px;
            background: linear-gradient(to bottom, #0051d5, #eceef0);
        }
        .trace-line-end::before {
            display: none;
        }
        .code-snippet::-webkit-scrollbar {
            width: 4px;
            height: 4px;
        }
        .code-snippet::-webkit-scrollbar-thumb {
            background: #43474d;
            border-radius: 10px;
        }
    </style>
</head>
<body class="bg-surface font-body text-on-surface selection:bg-secondary/30 selection:text-secondary">
<!-- TopAppBar -->
<header class="fixed top-0 w-full z-50 bg-slate-950/70 backdrop-blur-xl flex justify-between items-center h-16 px-6 w-full border-b border-slate-800/50">
<div class="flex items-center gap-8">
<h1 class="text-xl font-bold tracking-tighter text-slate-100">MediAgent</h1>
<div class="hidden md:flex gap-6">
<a class="text-slate-400 hover:text-slate-200 transition-colors duration-300 ease-in-out font-sans tracking-tight" href="#">Analysis</a>
<a class="text-slate-400 hover:text-slate-200 transition-colors duration-300 ease-in-out font-sans tracking-tight" href="#">Records</a>
<a class="text-slate-400 hover:text-slate-200 transition-colors duration-300 ease-in-out font-sans tracking-tight" href="#">Status</a>
<a class="text-blue-500 font-semibold transition-colors duration-300 ease-in-out font-sans tracking-tight" href="#">Trace</a>
</div>
</div>
<div class="flex items-center gap-4">
<button class="p-2 text-slate-400 hover:bg-slate-800/50 transition-colors rounded-full">
<span class="material-symbols-outlined">settings</span>
</button>
<button class="p-2 text-slate-400 hover:bg-slate-800/50 transition-colors rounded-full">
<span class="material-symbols-outlined">account_circle</span>
</button>
</div>
</header>
<div class="flex min-h-screen">
<!-- SideNavBar -->
<aside class="hidden md:flex flex-col pt-20 h-screen w-64 border-r border-slate-800/50 bg-slate-950">
<div class="px-6 mb-8">
<div class="text-blue-500 font-black font-mono text-sm uppercase tracking-widest">Clinical Ops</div>
<div class="text-slate-500 text-[10px] uppercase tracking-widest mt-1">V2.4 Active</div>
</div>
<nav class="flex-1">
<div class="space-y-1">
<a class="flex items-center gap-3 text-slate-500 hover:text-slate-300 px-4 py-3 hover:bg-slate-900 transition-all font-mono text-sm uppercase tracking-widest active:translate-x-1" href="#">
<span class="material-symbols-outlined">analytics</span>
<span>Analysis</span>
</a>
<a class="flex items-center gap-3 text-slate-500 hover:text-slate-300 px-4 py-3 hover:bg-slate-900 transition-all font-mono text-sm uppercase tracking-widest active:translate-x-1" href="#">
<span class="material-symbols-outlined">database</span>
<span>Records</span>
</a>
<a class="flex items-center gap-3 text-slate-500 hover:text-slate-300 px-4 py-3 hover:bg-slate-900 transition-all font-mono text-sm uppercase tracking-widest active:translate-x-1" href="#">
<span class="material-symbols-outlined">query_stats</span>
<span>Status</span>
</a>
<a class="flex items-center gap-3 bg-blue-600/10 text-blue-400 border-r-2 border-blue-500 px-4 py-3 hover:bg-slate-900 transition-all font-mono text-sm uppercase tracking-widest active:translate-x-1" href="#">
<span class="material-symbols-outlined">terminal</span>
<span>Trace</span>
</a>
</div>
</nav>
<div class="p-4 space-y-1">
<a class="flex items-center gap-3 text-slate-500 hover:text-slate-300 px-4 py-3 hover:bg-slate-900 transition-all font-mono text-sm uppercase tracking-widest" href="#">
<span class="material-symbols-outlined">help</span>
<span>Help</span>
</a>
<a class="flex items-center gap-3 text-slate-500 hover:text-slate-300 px-4 py-3 hover:bg-slate-900 transition-all font-mono text-sm uppercase tracking-widest" href="#">
<span class="material-symbols-outlined">logout</span>
<span>Logout</span>
</a>
</div>
</aside>
<!-- Main Content Area -->
<main class="flex-1 pt-24 pb-12 px-8 overflow-y-auto">
<div class="max-w-6xl mx-auto">
<!-- Header Stats -->
<div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
<div class="bg-surface-container-low p-6 rounded-xl border border-outline-variant/10">
<div class="text-on-surface-variant text-[10px] uppercase font-bold tracking-widest mb-1">Trace ID</div>
<div class="font-mono text-secondary text-sm">TX-7700-ALPHA-92</div>
</div>
<div class="bg-surface-container-low p-6 rounded-xl border border-outline-variant/10">
<div class="text-on-surface-variant text-[10px] uppercase font-bold tracking-widest mb-1">Total Latency</div>
<div class="font-mono text-on-surface text-lg">1.42s</div>
</div>
<div class="bg-surface-container-low p-6 rounded-xl border border-outline-variant/10">
<div class="text-on-surface-variant text-[10px] uppercase font-bold tracking-widest mb-1">Total Tokens</div>
<div class="font-mono text-on-surface text-lg">4,281</div>
</div>
<div class="bg-surface-container-low p-6 rounded-xl border border-outline-variant/10">
<div class="text-on-surface-variant text-[10px] uppercase font-bold tracking-widest mb-1">Status</div>
<div class="flex items-center gap-2 mt-1">
<span class="w-2 h-2 rounded-full bg-on-tertiary-container animate-pulse"></span>
<span class="text-on-tertiary-container font-bold text-xs uppercase tracking-tighter">Completed</span>
</div>
</div>
</div>
<!-- Timeline Explorer -->
<div class="space-y-0">
<!-- Entry Node -->
<div class="relative pl-12 pb-16 trace-line">
<div class="absolute left-0 top-0 w-10 h-10 rounded-full bg-primary flex items-center justify-center z-10 border-4 border-surface">
<span class="material-symbols-outlined text-white text-lg">play_arrow</span>
</div>
<div class="flex flex-col md:flex-row md:items-start gap-8">
<div class="w-full md:w-1/3">
<h3 class="text-display-lg font-extrabold tracking-tighter text-primary">Execution Start</h3>
<p class="text-on-surface-variant text-sm mt-2 leading-relaxed">Triggered by clinical radiological upload. Payload validated against FHIR schema.</p>
</div>
<div class="flex-1 bg-surface-container-highest/30 rounded-xl p-4 overflow-hidden border border-outline-variant/15">
<div class="flex justify-between items-center mb-3">
<span class="font-mono text-[10px] text-on-surface-variant uppercase">Input Payload</span>
<span class="px-2 py-0.5 bg-surface-container text-on-surface-variant text-[9px] font-mono rounded">JSON</span>
</div>
<pre class="font-mono text-xs text-on-surface-variant code-snippet overflow-x-auto"><code>{
  "request_id": "MED-902",
  "source": "Imaging_Suite_4",
  "priority": "STAT",
  "modality": "CT_SCAN"
}</code></pre>
</div>
</div>
</div>
<!-- Vision Agent Node -->
<div class="relative pl-12 pb-16 trace-line">
<div class="absolute left-0 top-0 w-10 h-10 rounded-full bg-secondary flex items-center justify-center z-10 border-4 border-surface shadow-lg shadow-secondary/20">
<span class="material-symbols-outlined text-white text-lg">visibility</span>
</div>
<div class="flex flex-col md:flex-row md:items-start gap-8">
<div class="w-full md:w-1/3">
<div class="flex items-center gap-2 mb-1">
<span class="text-[10px] font-mono bg-secondary-container text-on-secondary-container px-1.5 py-0.5 rounded">LLaVA-v1.6</span>
<span class="font-mono text-[10px] text-on-surface-variant">322ms</span>
</div>
<h3 class="text-xl font-bold tracking-tight text-primary">Vision Agent</h3>
<p class="text-on-surface-variant text-sm mt-2 leading-relaxed">Multimodal feature extraction from axial CT slices. Identifies focal opacities in the right lower lobe.</p>
<div class="mt-4 flex flex-wrap gap-2">
<span class="px-2 py-1 bg-surface-container-high rounded-full text-[10px] font-bold text-on-surface-variant uppercase tracking-wider">Visual_Scan</span>
<span class="px-2 py-1 bg-surface-container-high rounded-full text-[10px] font-bold text-on-surface-variant uppercase tracking-wider">OCR_Labels</span>
</div>
</div>
<div class="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-4">
<div class="bg-primary-container rounded-xl p-4 border border-blue-500/10">
<div class="text-[9px] font-mono text-on-primary-container mb-2 uppercase tracking-widest">Inference Details</div>
<div class="space-y-2">
<div class="flex justify-between text-[11px] font-mono">
<span class="text-on-primary-container">Confidence</span>
<span class="text-tertiary-fixed-dim">0.982</span>
</div>
<div class="flex justify-between text-[11px] font-mono">
<span class="text-on-primary-container">Tokens</span>
<span class="text-on-secondary-container">1,024</span>
</div>
</div>
</div>
<div class="bg-surface-container-highest/30 rounded-xl p-4 border border-outline-variant/15">
<div class="flex justify-between items-center mb-2">
<span class="font-mono text-[10px] text-on-surface-variant uppercase">Extracted_Features</span>
</div>
<pre class="font-mono text-[10px] text-on-surface-variant code-snippet overflow-x-auto"><code>{
  "finding": "Nodule",
  "coord": [112, 45],
  "diameter": "8.2mm",
  "density": "Solid"
}</code></pre>
</div>
</div>
</div>
</div>
<!-- RAG Agent Node -->
<div class="relative pl-12 pb-16 trace-line">
<div class="absolute left-0 top-0 w-10 h-10 rounded-full bg-on-tertiary-container flex items-center justify-center z-10 border-4 border-surface shadow-lg shadow-on-tertiary-container/20">
<span class="material-symbols-outlined text-white text-lg">database</span>
</div>
<div class="flex flex-col md:flex-row md:items-start gap-8">
<div class="w-full md:w-1/3">
<div class="flex items-center gap-2 mb-1">
<span class="text-[10px] font-mono bg-tertiary-fixed text-on-tertiary-fixed px-1.5 py-0.5 rounded">PubMed + Chroma</span>
<span class="font-mono text-[10px] text-on-surface-variant">518ms</span>
</div>
<h3 class="text-xl font-bold tracking-tight text-primary">RAG Agent</h3>
<p class="text-on-surface-variant text-sm mt-2 leading-relaxed">Vector search against 4.2M clinical papers. Retrieving Fleischner Society guidelines for small pulmonary nodules.</p>
</div>
<div class="flex-1 bg-tertiary-container text-tertiary-fixed rounded-xl p-5 border border-on-tertiary-container/20 overflow-hidden">
<div class="flex items-center gap-3 mb-4">
<div class="p-1.5 bg-on-tertiary-container/10 rounded">
<span class="material-symbols-outlined text-sm">link</span>
</div>
<span class="text-[10px] font-mono uppercase tracking-widest">Retrieved Contexts (2)</span>
</div>
<div class="space-y-4">
<div class="border-l-2 border-tertiary-fixed/30 pl-4 py-1">
<div class="text-[10px] font-mono text-tertiary-fixed/60 mb-1">PMID: 28240470</div>
<p class="text-xs italic leading-snug">"Guidelines for Management of Incidental Pulmonary Nodules... recommend follow-up CT at 6-12 months for low-risk patients."</p>
</div>
<div class="border-l-2 border-tertiary-fixed/30 pl-4 py-1">
<div class="text-[10px] font-mono text-tertiary-fixed/60 mb-1">CHROMA_SIMILARITY: 0.892</div>
<p class="text-xs italic leading-snug">"Case studies of 8mm solid nodules indicate low malignancy probability but necessitate careful observation."</p>
</div>
</div>
</div>
</div>
</div>
<!-- Report Agent Node -->
<div class="relative pl-12 pb-16 trace-line">
<div class="absolute left-0 top-0 w-10 h-10 rounded-full bg-primary-container flex items-center justify-center z-10 border-4 border-surface shadow-lg">
<span class="material-symbols-outlined text-white text-lg" data-weight="fill">description</span>
</div>
<div class="flex flex-col md:flex-row md:items-start gap-8">
<div class="w-full md:w-1/3">
<div class="flex items-center gap-2 mb-1">
<span class="text-[10px] font-mono bg-on-primary-fixed-variant text-on-primary-fixed px-1.5 py-0.5 rounded">LLaMA-3-70B</span>
<span class="font-mono text-[10px] text-on-surface-variant">580ms</span>
</div>
<h3 class="text-xl font-bold tracking-tight text-primary">Report Agent</h3>
<p class="text-on-surface-variant text-sm mt-2 leading-relaxed">Synthesizing visual findings and clinical literature into a structured medical report draft.</p>
<div class="mt-4 p-3 bg-secondary/5 border-l-2 border-secondary rounded-r-lg">
<div class="text-[9px] uppercase font-bold text-secondary mb-1">Final Decision Logic</div>
<p class="text-[11px] text-on-surface italic">"Nodule observed &gt; Literature recommendation = High confidence follow-up schedule."</p>
</div>
</div>
<div class="flex-1 bg-surface-container-lowest rounded-xl p-1 shadow-sm border border-outline-variant/20">
<div class="p-4 border-b border-surface-container">
<span class="font-mono text-[10px] text-on-surface-variant uppercase">Structured_Output.md</span>
</div>
<div class="p-4 font-mono text-xs text-on-surface leading-relaxed max-h-48 overflow-y-auto code-snippet">
<div class="text-secondary"># Clinical Impression</div>
<div class="mt-2 text-on-surface-variant">1. Solid pulmonary nodule, right lower lobe, measuring 8.2mm.</div>
<div class="mt-1 text-on-surface-variant">2. No hilar or mediastinal lymphadenopathy.</div>
<div class="mt-2 text-secondary"># Recommendation</div>
<div class="mt-1 text-on-surface-variant">Follow-up CT scan in 6-12 months per Fleischner Society criteria for solid nodules in low-risk patients.</div>
</div>
</div>
</div>
</div>
<!-- Termination Node -->
<div class="relative pl-12 pb-0 trace-line trace-line-end">
<div class="absolute left-0 top-0 w-10 h-10 rounded-full bg-on-tertiary-container flex items-center justify-center z-10 border-4 border-surface">
<span class="material-symbols-outlined text-white text-lg">check_circle</span>
</div>
<div class="flex flex-col md:flex-row md:items-center gap-8">
<div class="w-full md:w-1/3">
<h3 class="text-lg font-bold tracking-tight text-primary">Trace Complete</h3>
<p class="text-on-surface-variant text-xs mt-1">Memory cleared. Artifacts archived.</p>
</div>
<div class="flex gap-4">
<button class="px-5 py-2 bg-secondary text-on-secondary rounded-full text-xs font-bold uppercase tracking-widest hover:bg-secondary-container transition-colors">
                                    Export Logs
                                </button>
<button class="px-5 py-2 bg-surface-container-high text-on-surface-variant rounded-full text-xs font-bold uppercase tracking-widest hover:bg-surface-container-highest transition-colors">
                                    Replay Step
                                </button>
</div>
</div>
</div>
</div>
</div>
</main>
</div>
<!-- Contextual FAB (Only visible on trace detail) -->
<div class="fixed bottom-8 right-8 flex flex-col gap-3">
<button class="w-14 h-14 bg-primary text-white rounded-full shadow-2xl flex items-center justify-center hover:scale-105 transition-transform active:scale-95 group">
<span class="material-symbols-outlined text-2xl group-hover:rotate-45 transition-transform">bolt</span>
</button>
</div>
</body></html>

<!-- Knowledge Context & Evidence View -->
<!DOCTYPE html>

<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>PrecisionSentinel AI | Knowledge Context &amp; Evidence Viewer</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&amp;family=JetBrains+Mono:wght@400;500;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    "surface-variant": "#e0e3e5",
                    "tertiary-fixed-dim": "#4edea3",
                    "surface-container-lowest": "#ffffff",
                    "on-primary-fixed": "#001c37",
                    "outline-variant": "#c4c6ce",
                    "surface-tint": "#49607e",
                    "surface": "#f7f9fb",
                    "tertiary-container": "#002a1a",
                    "surface-dim": "#d8dadc",
                    "on-secondary-container": "#fefcff",
                    "on-surface": "#191c1e",
                    "error-container": "#ffdad6",
                    "surface-container-high": "#e6e8ea",
                    "on-primary-fixed-variant": "#314865",
                    "error": "#ba1a1a",
                    "inverse-on-surface": "#eff1f3",
                    "on-tertiary-container": "#009e6d",
                    "on-error-container": "#93000a",
                    "secondary": "#0051d5",
                    "inverse-primary": "#b0c8eb",
                    "surface-container": "#eceef0",
                    "on-secondary-fixed-variant": "#003ea8",
                    "on-secondary": "#ffffff",
                    "background": "#f7f9fb",
                    "on-secondary-fixed": "#00174b",
                    "surface-bright": "#f7f9fb",
                    "secondary-fixed": "#dbe1ff",
                    "on-surface-variant": "#43474d",
                    "on-primary-container": "#768dad",
                    "on-background": "#191c1e",
                    "outline": "#74777e",
                    "on-tertiary-fixed-variant": "#005236",
                    "surface-container-low": "#f2f4f6",
                    "secondary-fixed-dim": "#b4c5ff",
                    "on-error": "#ffffff",
                    "primary-container": "#0a2540",
                    "tertiary-fixed": "#6ffbbe",
                    "primary": "#000f22",
                    "primary-fixed": "#d2e4ff",
                    "secondary-container": "#316bf3",
                    "on-tertiary-fixed": "#002113",
                    "tertiary": "#001209",
                    "on-tertiary": "#ffffff",
                    "surface-container-highest": "#e0e3e5",
                    "primary-fixed-dim": "#b0c8eb",
                    "on-primary": "#ffffff",
                    "inverse-surface": "#2d3133"
            },
            "borderRadius": {
                    "DEFAULT": "0.125rem",
                    "lg": "0.25rem",
                    "xl": "0.5rem",
                    "full": "0.75rem"
            },
            "fontFamily": {
                    "headline": ["Inter"],
                    "body": ["Inter"],
                    "label": ["Inter"],
                    "mono": ["JetBrains Mono"]
            }
          },
        },
      }
    </script>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .mono-text { font-family: 'JetBrains Mono', monospace; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #0a254033; border-radius: 10px; }
    </style>
</head>
<body class="bg-surface text-on-surface font-body overflow-hidden">
<!-- Top Navigation Anchor -->
<nav class="flex justify-between items-center px-6 py-3 w-full bg-[#000f22] dark:bg-[#000f22] sticky top-0 z-50">
<div class="flex items-center gap-8">
<span class="text-xl font-bold tracking-tighter text-white font-headline">PrecisionSentinel AI</span>
<div class="hidden md:flex gap-6 items-center">
<a class="text-slate-400 font-medium hover:text-white transition-colors text-sm" href="#">Evidence Feed</a>
<a class="text-white border-b-2 border-[#0051d5] pb-1 font-medium transition-colors text-sm" href="#">Clinical Insights</a>
<a class="text-slate-400 font-medium hover:text-white transition-colors text-sm" href="#">Library</a>
</div>
</div>
<div class="flex items-center gap-4">
<div class="flex items-center bg-white/5 rounded-full px-3 py-1.5 border border-white/10">
<span class="material-symbols-outlined text-slate-400 text-lg mr-2">search</span>
<input class="bg-transparent border-none focus:ring-0 text-white text-xs w-48" placeholder="Search knowledge base..." type="text"/>
</div>
<span class="material-symbols-outlined text-slate-400 cursor-pointer hover:text-white">science</span>
<span class="material-symbols-outlined text-slate-400 cursor-pointer hover:text-white">account_circle</span>
</div>
</nav>
<!-- Main Modal Overlay Container -->
<div class="flex h-[calc(100vh-56px)] overflow-hidden">
<!-- SIDE PANEL: Retrieved Fragments -->
<aside class="w-96 bg-[#000f22] border-r border-white/5 flex flex-col">
<div class="p-6">
<h2 class="font-mono text-[10px] uppercase tracking-widest text-[#0051d5] mb-1">RAG Context Engine</h2>
<h3 class="text-white text-lg font-bold tracking-tight">Retrieved Fragments</h3>
<p class="text-slate-500 text-xs mt-1">Found 12 relevant segments from PubMed/MedQA</p>
</div>
<div class="flex-1 overflow-y-auto px-4 space-y-3 pb-8">
<!-- Fragment Item 1 (Active) -->
<div class="bg-[#0051d5] text-white p-4 rounded-xl cursor-pointer group transition-all duration-200">
<div class="flex justify-between items-start mb-2">
<span class="bg-white/20 text-[10px] px-2 py-0.5 rounded font-bold uppercase tracking-wider">PubMed</span>
<span class="mono-text text-[11px] font-bold">SIM 0.942</span>
</div>
<p class="text-sm leading-relaxed line-clamp-3 font-medium">Radiographic evidence of ground-glass opacities in bilateral lower lobes suggests typical viral pneumonia morphology...</p>
<div class="mt-3 flex items-center gap-2">
<span class="material-symbols-outlined text-xs">history</span>
<span class="text-[10px] opacity-70">Extracted 2m ago</span>
</div>
</div>
<!-- Fragment Item 2 -->
<div class="bg-white/5 hover:bg-white/10 text-slate-300 p-4 rounded-xl cursor-pointer transition-all duration-200">
<div class="flex justify-between items-start mb-2">
<span class="bg-white/5 text-[10px] px-2 py-0.5 rounded font-bold uppercase tracking-wider">MedQA</span>
<span class="mono-text text-[11px] font-bold text-[#0051d5]">SIM 0.887</span>
</div>
<p class="text-sm leading-relaxed line-clamp-3 text-slate-400">Clinical presentation of sub-acute respiratory distress in elderly populations often correlates with atypical...</p>
</div>
<!-- Fragment Item 3 -->
<div class="bg-white/5 hover:bg-white/10 text-slate-300 p-4 rounded-xl cursor-pointer transition-all duration-200">
<div class="flex justify-between items-start mb-2">
<span class="bg-white/5 text-[10px] px-2 py-0.5 rounded font-bold uppercase tracking-wider">PubMed</span>
<span class="mono-text text-[11px] font-bold text-[#0051d5]">SIM 0.814</span>
</div>
<p class="text-sm leading-relaxed line-clamp-3 text-slate-400">Differential diagnosis involving bacterial pathogens must be excluded through sputum culture and PCT testing...</p>
</div>
<!-- Fragment Item 4 -->
<div class="bg-white/5 hover:bg-white/10 text-slate-300 p-4 rounded-xl cursor-pointer transition-all duration-200">
<div class="flex justify-between items-start mb-2">
<span class="bg-white/5 text-[10px] px-2 py-0.5 rounded font-bold uppercase tracking-wider">Internal</span>
<span class="mono-text text-[11px] font-bold text-[#0051d5]">SIM 0.792</span>
</div>
<p class="text-sm leading-relaxed line-clamp-3 text-slate-400">Patient history indicates recurring asthma-like symptoms previously treated with inhaled corticosteroids without...</p>
</div>
</div>
</aside>
<!-- MAIN CONTENT: Evidence Viewer -->
<main class="flex-1 bg-surface flex flex-col relative overflow-y-auto">
<!-- Metadata Header -->
<header class="p-8 bg-white/50 backdrop-blur-md sticky top-0 z-10 border-b border-surface-container-high">
<div class="flex justify-between items-start gap-12">
<div class="space-y-4">
<div class="flex gap-2">
<span class="bg-secondary-container text-on-secondary-container px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider">Primary Evidence</span>
<span class="bg-surface-container-highest text-on-surface-variant px-3 py-1 rounded-full text-[10px] font-medium uppercase tracking-wider">ID: 8829-PX</span>
</div>
<h1 class="text-3xl font-bold tracking-tight text-primary leading-tight">Comparative Analysis of Radiographic Biomarkers in Viral vs. Bacterial Pneumonia: A Meta-Analysis</h1>
<div class="flex flex-wrap items-center gap-x-6 gap-y-2 text-on-surface-variant text-sm">
<div class="flex items-center gap-1">
<span class="material-symbols-outlined text-lg">person</span>
<span class="font-medium">Dr. Elena Rodriguez, et al.</span>
</div>
<div class="flex items-center gap-1">
<span class="material-symbols-outlined text-lg">calendar_today</span>
<span>Published: Oct 2023</span>
</div>
<div class="flex items-center gap-1 text-secondary font-bold">
<span class="material-symbols-outlined text-lg">link</span>
<span class="mono-text">PMID: 3749201</span>
</div>
</div>
</div>
<!-- Action Buttons Cluster -->
<div class="flex flex-col gap-2 shrink-0">
<button class="bg-secondary text-white px-6 py-2.5 rounded-full text-sm font-bold flex items-center justify-center gap-2 hover:opacity-90 transition-all shadow-lg shadow-secondary/20">
<span class="material-symbols-outlined text-lg">picture_as_pdf</span>
                            Open original PDF
                        </button>
<div class="flex gap-2">
<button class="flex-1 bg-surface-container-low text-primary px-4 py-2 rounded-full text-xs font-bold flex items-center justify-center gap-2 hover:bg-surface-container-high transition-all">
<span class="material-symbols-outlined text-base">content_copy</span>
                                Copy Citation
                            </button>
<button class="bg-surface-container-low text-error px-4 py-2 rounded-full text-xs font-bold flex items-center justify-center gap-2 hover:bg-error-container transition-all">
<span class="material-symbols-outlined text-base">flag</span>
</button>
</div>
</div>
</div>
</header>
<!-- Content Body -->
<div class="p-8 max-w-4xl space-y-12 pb-32">
<!-- Abstract Section -->
<section class="space-y-4">
<h4 class="font-mono text-xs uppercase tracking-widest text-on-surface-variant">Selected Segment Abstract</h4>
<div class="text-lg leading-relaxed text-on-surface font-light">
                        The current study demonstrates that <span class="bg-secondary/10 border-b-2 border-secondary font-medium">ground-glass opacities (GGOs)</span> with a peripheral distribution are highly indicative of viral etiology, particularly in the lower lobes. Our deep learning model analyzed 12,000 CT scans, revealing that a GGO-to-infiltrate ratio of &gt;1.4 correlates with viral pneumonia with a 92% sensitivity (CI: 89-94%). Conversely, lobar consolidation remains the hallmark for bacterial infection. 
                    </div>
<div class="text-lg leading-relaxed text-on-surface font-light">
                        Furthermore, the presence of subpleural sparing was observed in only 12% of viral cases, suggesting that focal pleuritis may be a secondary indicator for bacterial co-infection. These findings are critical for rapid triage in emergency settings where PCR testing turnaround exceeds 4 hours.
                    </div>
</section>
<!-- Context Mapping: Bento Grid Style -->
<section class="space-y-6">
<h4 class="font-mono text-xs uppercase tracking-widest text-[#0051d5]">Context Mapping &amp; AI Inference</h4>
<div class="grid grid-cols-12 gap-4">
<!-- Supporting Card -->
<div class="col-span-7 bg-white p-6 rounded-2xl border border-surface-container-high hover:border-secondary/20 transition-all">
<div class="flex items-center gap-3 mb-4">
<div class="w-10 h-10 rounded-full bg-tertiary-fixed flex items-center justify-center text-on-tertiary-fixed">
<span class="material-symbols-outlined">check_circle</span>
</div>
<div>
<h5 class="font-bold text-primary">Diagnosis Alignment</h5>
<p class="text-xs text-on-surface-variant">Inference Confidence: High</p>
</div>
</div>
<p class="text-sm text-on-surface-variant leading-relaxed">
                                This fragment <strong class="text-primary font-bold">supports the current Pneumonia diagnosis</strong>. The patient's CT findings (Peripheral GGOs in lower lobes) match the morphological patterns described in this meta-analysis for viral etiology.
                            </p>
</div>
<!-- Data Point Card -->
<div class="col-span-5 bg-primary p-6 rounded-2xl text-white">
<h5 class="mono-text text-[10px] uppercase tracking-widest opacity-60 mb-2">Clinical Correlation</h5>
<div class="text-2xl font-bold tracking-tighter mb-4">92.4% Match</div>
<p class="text-xs text-slate-400 leading-relaxed">
                                Similarity to patient's clinical phenotype based on radiographic markers and symptomatic presentation.
                            </p>
</div>
<!-- Technical Spec Card -->
<div class="col-span-12 bg-surface-container-low p-6 rounded-2xl flex items-center justify-between">
<div class="flex gap-8">
<div>
<div class="text-[10px] text-on-surface-variant uppercase font-mono tracking-widest mb-1">Embedding Model</div>
<div class="text-sm font-bold text-primary">BioBERT-v4.2</div>
</div>
<div>
<div class="text-[10px] text-on-surface-variant uppercase font-mono tracking-widest mb-1">Source Rank</div>
<div class="text-sm font-bold text-primary">Rank #1 of 1,240</div>
</div>
<div>
<div class="text-[10px] text-on-surface-variant uppercase font-mono tracking-widest mb-1">Trust Score</div>
<div class="text-sm font-bold text-[#009e6d]">98% Verified</div>
</div>
</div>
<span class="material-symbols-outlined text-on-surface-variant">verified_user</span>
</div>
</div>
</section>
</div>
<!-- Context Footer -->
<footer class="absolute bottom-0 left-0 w-full bg-white/80 backdrop-blur-md px-8 py-4 flex justify-between items-center border-t border-surface-container-high">
<div class="flex items-center gap-3">
<div class="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
<span class="material-symbols-outlined text-white text-sm" style="font-variation-settings: 'FILL' 1;">psychology</span>
</div>
<span class="text-xs font-medium text-on-surface-variant">AI has highlighted segments most relevant to Patient ID: <span class="mono-text text-primary font-bold">#PA-2024-0012</span></span>
</div>
<div class="flex gap-4">
<button class="text-secondary font-bold text-xs uppercase tracking-wider hover:underline">View Inference Chain</button>
<button class="text-on-surface-variant font-bold text-xs uppercase tracking-wider hover:text-primary">Download Summary</button>
</div>
</footer>
</main>
</div>
<!-- Background Decoration for Precision Aesthetic -->
<div class="fixed inset-0 pointer-events-none z-[-1] opacity-20">
<div class="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] bg-secondary/10 blur-[120px] rounded-full"></div>
<div class="absolute bottom-[-10%] left-[-5%] w-[30%] h-[30%] bg-primary/10 blur-[100px] rounded-full"></div>
</div>
</body></html>

<!-- Lab Report Data Extraction Detail -->
<!DOCTYPE html>

<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>MediAgent | Lab Report Extraction</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&amp;family=JetBrains+Mono:wght@400;500;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    "surface-tint": "#49607e",
                    "on-surface": "#191c1e",
                    "on-secondary-fixed-variant": "#003ea8",
                    "surface-container-high": "#e6e8ea",
                    "on-tertiary": "#ffffff",
                    "on-surface-variant": "#43474d",
                    "inverse-surface": "#2d3133",
                    "on-secondary-container": "#fefcff",
                    "primary": "#000f22",
                    "primary-container": "#0a2540",
                    "surface": "#f7f9fb",
                    "on-tertiary-container": "#009e6d",
                    "surface-container-low": "#f2f4f6",
                    "on-primary": "#ffffff",
                    "on-background": "#191c1e",
                    "on-primary-fixed-variant": "#314865",
                    "tertiary": "#001209",
                    "surface-container-lowest": "#ffffff",
                    "secondary": "#0051d5",
                    "on-error-container": "#93000a",
                    "error": "#ba1a1a",
                    "on-secondary": "#ffffff",
                    "on-primary-fixed": "#001c37",
                    "tertiary-fixed-dim": "#4edea3",
                    "secondary-container": "#316bf3",
                    "error-container": "#ffdad6",
                    "surface-container-highest": "#e0e3e5",
                    "surface-bright": "#f7f9fb",
                    "tertiary-fixed": "#6ffbbe",
                    "inverse-on-surface": "#eff1f3",
                    "on-secondary-fixed": "#00174b",
                    "on-primary-container": "#768dad",
                    "secondary-fixed": "#dbe1ff",
                    "background": "#f7f9fb",
                    "surface-variant": "#e0e3e5",
                    "surface-container": "#eceef0",
                    "outline": "#74777e",
                    "on-error": "#ffffff",
                    "inverse-primary": "#b0c8eb",
                    "primary-fixed": "#d2e4ff",
                    "secondary-fixed-dim": "#b4c5ff",
                    "on-tertiary-fixed-variant": "#005236",
                    "on-tertiary-fixed": "#002113",
                    "tertiary-container": "#002a1a",
                    "surface-dim": "#d8dadc",
                    "primary-fixed-dim": "#b0c8eb",
                    "outline-variant": "#c4c6ce"
            },
            "borderRadius": {
                    "DEFAULT": "0.125rem",
                    "lg": "0.25rem",
                    "xl": "0.5rem",
                    "full": "0.75rem"
            },
            "fontFamily": {
                    "headline": ["Inter"],
                    "body": ["Inter"],
                    "label": ["Inter"],
                    "mono": ["JetBrains Mono"]
            }
          },
        },
      }
    </script>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        body { font-family: 'Inter', sans-serif; }
        .mono-text { font-family: 'JetBrains Mono', monospace; }
    </style>
</head>
<body class="bg-surface text-on-surface min-h-screen flex flex-col">
<!-- TopAppBar -->
<header class="fixed top-0 w-full z-50 bg-slate-950/70 backdrop-blur-xl flex justify-between items-center h-16 px-6 w-full border-b border-slate-800/50">
<div class="flex items-center gap-8">
<h1 class="text-xl font-bold tracking-tighter text-slate-100">MediAgent</h1>
<nav class="hidden md:flex gap-6">
<a class="text-blue-500 font-semibold text-sm" href="#">Analysis</a>
<a class="text-slate-400 hover:text-slate-200 text-sm transition-colors duration-300" href="#">Records</a>
<a class="text-slate-400 hover:text-slate-200 text-sm transition-colors duration-300" href="#">Status</a>
<a class="text-slate-400 hover:text-slate-200 text-sm transition-colors duration-300" href="#">Trace</a>
</nav>
</div>
<div class="flex items-center gap-4">
<button class="p-2 text-slate-400 hover:bg-slate-800/50 rounded-full transition-colors duration-300">
<span class="material-symbols-outlined">settings</span>
</button>
<button class="p-2 text-slate-400 hover:bg-slate-800/50 rounded-full transition-colors duration-300">
<span class="material-symbols-outlined">account_circle</span>
</button>
</div>
</header>
<div class="flex flex-1 pt-16">
<!-- SideNavBar -->
<aside class="hidden lg:flex flex-col h-[calc(100vh-4rem)] w-64 bg-slate-950 border-r border-slate-800/50 sticky top-16">
<div class="p-6">
<div class="text-blue-500 font-black tracking-widest uppercase text-xs">Clinical Ops</div>
<div class="text-slate-500 text-[10px] mono-text mt-1">V2.4 Active</div>
</div>
<div class="flex-1 px-2 space-y-1">
<a class="flex items-center gap-3 bg-blue-600/10 text-blue-400 border-r-2 border-blue-500 px-4 py-3 active:translate-x-1 transition-all" href="#">
<span class="material-symbols-outlined text-sm">analytics</span>
<span class="font-mono text-sm uppercase tracking-widest">Analysis</span>
</a>
<a class="flex items-center gap-3 text-slate-500 hover:text-slate-300 hover:bg-slate-900 px-4 py-3 active:translate-x-1 transition-all" href="#">
<span class="material-symbols-outlined text-sm">database</span>
<span class="font-mono text-sm uppercase tracking-widest">Records</span>
</a>
<a class="flex items-center gap-3 text-slate-500 hover:text-slate-300 hover:bg-slate-900 px-4 py-3 active:translate-x-1 transition-all" href="#">
<span class="material-symbols-outlined text-sm">query_stats</span>
<span class="font-mono text-sm uppercase tracking-widest">Status</span>
</a>
<a class="flex items-center gap-3 text-slate-500 hover:text-slate-300 hover:bg-slate-900 px-4 py-3 active:translate-x-1 transition-all" href="#">
<span class="material-symbols-outlined text-sm">terminal</span>
<span class="font-mono text-sm uppercase tracking-widest">Trace</span>
</a>
</div>
<div class="p-4 border-t border-slate-900 space-y-1">
<a class="flex items-center gap-3 text-slate-500 hover:text-slate-300 px-4 py-2 text-sm uppercase tracking-widest font-mono" href="#">
<span class="material-symbols-outlined text-sm">help</span>
<span>Help</span>
</a>
<a class="flex items-center gap-3 text-slate-500 hover:text-slate-300 px-4 py-2 text-sm uppercase tracking-widest font-mono" href="#">
<span class="material-symbols-outlined text-sm">logout</span>
<span>Logout</span>
</a>
</div>
</aside>
<!-- Main Content Canvas -->
<main class="flex-1 flex overflow-hidden h-[calc(100vh-4rem)]">
<!-- Left Panel: PDF Preview -->
<section class="w-1/2 flex flex-col bg-surface-container-low overflow-hidden">
<div class="h-12 flex items-center justify-between px-6 bg-surface-bright/50 border-b border-outline-variant/10">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-primary text-sm">picture_as_pdf</span>
<span class="text-xs font-semibold uppercase tracking-widest text-primary">lab_report_0924.pdf</span>
</div>
<div class="flex gap-4">
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary text-lg">zoom_in</button>
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary text-lg">zoom_out</button>
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary text-lg">print</button>
</div>
</div>
<div class="flex-1 overflow-auto p-12 flex justify-center items-start">
<div class="relative bg-white shadow-2xl w-full max-w-2xl aspect-[1/1.414] p-12 overflow-hidden ring-1 ring-black/5">
<!-- Mock PDF Content -->
<div class="space-y-8 opacity-40 select-none">
<div class="flex justify-between items-start border-b border-black pb-4">
<div>
<h2 class="text-2xl font-bold uppercase">Clinical Labs Inc.</h2>
<p class="text-[10px]">123 Medical Plaza, San Francisco, CA</p>
</div>
<div class="text-right text-[10px] space-y-1">
<p>Patient ID: 882910</p>
<p>DOB: 12-MAY-1985</p>
<p>Sex: Male</p>
</div>
</div>
<div class="grid grid-cols-4 font-bold text-[10px] border-b-2 border-black/20 pb-2">
<span>TEST</span>
<span>RESULT</span>
<span>UNITS</span>
<span>REFERENCE RANGE</span>
</div>
<div class="grid grid-cols-4 text-[10px] space-y-4 pt-2">
<span class="col-span-1">Hemoglobin</span><span class="col-span-1">14.2</span><span class="col-span-1">g/dL</span><span class="col-span-1">13.5 - 17.5</span>
<span class="col-span-1">Hematocrit</span><span class="col-span-1">42.1</span><span class="col-span-1">%</span><span class="col-span-1">41.0 - 50.0</span>
<span class="col-span-1">White Cell Count</span><span class="col-span-1">7.4</span><span class="col-span-1">10^9/L</span><span class="col-span-1">4.5 - 11.0</span>
<span class="col-span-1">Platelets</span><span class="col-span-1">210</span><span class="col-span-1">10^9/L</span><span class="col-span-1">150 - 450</span>
</div>
</div>
<!-- Active Bounding Boxes (AI Overlays) -->
<div class="absolute inset-0 pointer-events-none p-12">
<!-- Header Highlight -->
<div class="absolute top-[138px] left-[48px] w-[200px] h-6 bg-secondary/10 border border-secondary/40 rounded-sm"></div>
<!-- Result Highlight -->
<div class="absolute top-[232px] left-[200px] w-24 h-5 bg-secondary/10 border-2 border-secondary rounded-sm flex items-center justify-end px-1">
<div class="absolute -top-4 -right-1 bg-secondary text-[8px] text-white px-1 font-bold">99.8%</div>
</div>
<!-- Range Highlight -->
<div class="absolute top-[232px] left-[450px] w-32 h-5 bg-tertiary-fixed-dim/20 border border-tertiary-fixed-dim rounded-sm"></div>
</div>
</div>
</div>
</section>
<!-- Right Panel: Verified Entities -->
<section class="w-1/2 flex flex-col bg-surface border-l border-outline-variant/15 overflow-hidden">
<div class="h-16 flex items-center justify-between px-8 bg-surface-container-low/50">
<div>
<h3 class="text-sm font-bold tracking-tight text-primary uppercase">Verified Entities</h3>
<p class="text-[10px] mono-text text-on-surface-variant">EXTRACTION ENGINE SIGMA-9</p>
</div>
<button class="bg-secondary text-white rounded-full px-6 py-2 text-xs font-bold hover:bg-on-secondary-fixed-variant transition-colors">
                        APPROVE ALL
                    </button>
</div>
<div class="flex-1 overflow-auto px-8 py-6 space-y-8">
<!-- Patient Group -->
<div class="space-y-4">
<div class="flex items-center gap-2 border-b border-outline-variant/5 pb-2">
<span class="material-symbols-outlined text-[16px] text-on-surface-variant">person</span>
<span class="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">Demographics</span>
</div>
<div class="grid grid-cols-2 gap-4">
<div class="bg-surface-container-low p-4 rounded-lg group hover:bg-surface-container-high transition-colors">
<div class="flex justify-between items-center mb-1">
<label class="text-[10px] font-bold text-on-surface-variant uppercase tracking-tighter">Patient Name</label>
<span class="bg-on-tertiary-container/10 text-on-tertiary-container px-1.5 py-0.5 rounded-full text-[8px] mono-text font-bold">99.2%</span>
</div>
<div class="flex items-center justify-between">
<span class="text-sm font-bold text-primary">JONATHAN DOE</span>
<button class="material-symbols-outlined text-on-surface-variant group-hover:text-secondary text-sm">edit</button>
</div>
</div>
<div class="bg-surface-container-low p-4 rounded-lg group hover:bg-surface-container-high transition-colors">
<div class="flex justify-between items-center mb-1">
<label class="text-[10px] font-bold text-on-surface-variant uppercase tracking-tighter">Collection Date</label>
<span class="bg-on-tertiary-container/10 text-on-tertiary-container px-1.5 py-0.5 rounded-full text-[8px] mono-text font-bold">100%</span>
</div>
<div class="flex items-center justify-between">
<span class="text-sm font-bold text-primary mono-text">2024-09-24</span>
<button class="material-symbols-outlined text-on-surface-variant group-hover:text-secondary text-sm">edit</button>
</div>
</div>
</div>
</div>
<!-- Lab Values Group -->
<div class="space-y-4">
<div class="flex items-center gap-2 border-b border-outline-variant/5 pb-2">
<span class="material-symbols-outlined text-[16px] text-on-surface-variant">biotech</span>
<span class="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">Clinical Measurements</span>
</div>
<!-- Table Style Entry -->
<div class="space-y-2">
<!-- Header -->
<div class="grid grid-cols-12 px-4 py-2 text-[9px] font-black uppercase text-on-surface-variant/60 tracking-widest">
<div class="col-span-5">Analyte</div>
<div class="col-span-2 text-right">Value</div>
<div class="col-span-2 text-right">Unit</div>
<div class="col-span-3 text-right">Ref Range</div>
</div>
<!-- Row 1 -->
<div class="grid grid-cols-12 items-center px-4 py-4 bg-surface-container-low rounded-xl ring-1 ring-transparent hover:ring-secondary/50 transition-all cursor-pointer">
<div class="col-span-5">
<div class="flex items-center gap-2">
<div class="w-1.5 h-1.5 rounded-full bg-secondary"></div>
<span class="text-xs font-bold text-primary">Hemoglobin</span>
</div>
</div>
<div class="col-span-2 text-right">
<span class="mono-text text-sm font-bold text-primary">14.2</span>
</div>
<div class="col-span-2 text-right">
<span class="mono-text text-[10px] text-on-surface-variant">g/dL</span>
</div>
<div class="col-span-3 text-right flex flex-col items-end">
<span class="mono-text text-[10px] text-on-surface-variant">13.5 - 17.5</span>
<span class="bg-on-tertiary-container/10 text-on-tertiary-container px-1.5 py-0.5 rounded-full text-[7px] mono-text font-black mt-1">99.8% CONF</span>
</div>
</div>
<!-- Row 2 (Anomaly Example) -->
<div class="grid grid-cols-12 items-center px-4 py-4 bg-surface-container-low rounded-xl ring-1 ring-transparent hover:ring-secondary/50 transition-all cursor-pointer">
<div class="col-span-5">
<div class="flex items-center gap-2">
<div class="w-1.5 h-1.5 rounded-full bg-error"></div>
<span class="text-xs font-bold text-primary">Glucose, Fasting</span>
</div>
</div>
<div class="col-span-2 text-right">
<span class="mono-text text-sm font-bold text-error">126</span>
</div>
<div class="col-span-2 text-right">
<span class="mono-text text-[10px] text-on-surface-variant">mg/dL</span>
</div>
<div class="col-span-3 text-right flex flex-col items-end">
<span class="mono-text text-[10px] text-on-surface-variant">70 - 99</span>
<span class="bg-error-container text-on-error-container px-1.5 py-0.5 rounded-full text-[7px] mono-text font-black mt-1">CRITICAL HI</span>
</div>
</div>
<!-- Row 3 -->
<div class="grid grid-cols-12 items-center px-4 py-4 bg-surface-container-low rounded-xl ring-1 ring-transparent hover:ring-secondary/50 transition-all cursor-pointer">
<div class="col-span-5">
<div class="flex items-center gap-2">
<div class="w-1.5 h-1.5 rounded-full bg-on-tertiary-container"></div>
<span class="text-xs font-bold text-primary">Potassium</span>
</div>
</div>
<div class="col-span-2 text-right">
<span class="mono-text text-sm font-bold text-primary">4.1</span>
</div>
<div class="col-span-2 text-right">
<span class="mono-text text-[10px] text-on-surface-variant">mmol/L</span>
</div>
<div class="col-span-3 text-right flex flex-col items-end">
<span class="mono-text text-[10px] text-on-surface-variant">3.5 - 5.1</span>
<span class="bg-on-tertiary-container/10 text-on-tertiary-container px-1.5 py-0.5 rounded-full text-[7px] mono-text font-black mt-1">98.4% CONF</span>
</div>
</div>
</div>
</div>
<!-- AI Insights / Flags -->
<div class="bg-primary p-6 rounded-xl relative overflow-hidden">
<div class="absolute -right-4 -top-4 w-32 h-32 bg-secondary opacity-20 blur-3xl rounded-full"></div>
<div class="relative z-10">
<div class="flex items-center gap-2 mb-3">
<span class="material-symbols-outlined text-secondary text-lg">psychology</span>
<span class="text-[10px] font-bold text-on-primary uppercase tracking-[0.2em]">Clinical Sentinel Analysis</span>
</div>
<p class="text-sm text-on-primary/80 leading-relaxed font-light">
                                Fasting glucose level of <span class="text-white font-bold underline decoration-secondary">126 mg/dL</span> detected. This meets the clinical threshold for a diagnostic follow-up regarding type 2 diabetes. Automatic referral generated in EHR.
                            </p>
</div>
</div>
</div>
<!-- Footer Actions -->
<div class="p-6 bg-surface-container-lowest border-t border-outline-variant/10 flex justify-between items-center">
<button class="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant hover:text-primary transition-colors flex items-center gap-2">
<span class="material-symbols-outlined text-sm">history</span>
                        Audit Log
                    </button>
<div class="flex gap-4">
<button class="bg-surface-container-high text-primary px-6 py-3 rounded-full text-xs font-bold hover:bg-surface-variant transition-all">
                            FLAG FOR REVIEW
                        </button>
<button class="bg-primary text-white px-8 py-3 rounded-full text-xs font-bold shadow-lg shadow-primary/20 hover:scale-[1.02] transition-all">
                            COMMIT TO EHR
                        </button>
</div>
</div>
</section>
</main>
</div>
<!-- Floating Assistant Button -->
<div class="fixed bottom-8 right-8 z-50">
<button class="w-14 h-14 bg-primary text-white rounded-full flex items-center justify-center shadow-2xl ring-4 ring-secondary/20 hover:scale-110 transition-transform group">
<span class="material-symbols-outlined group-hover:rotate-12 transition-transform" style="font-variation-settings: 'FILL' 1;">bolt</span>
</button>
</div>
</body></html>

<!-- MediAgent - New Analysis -->
<!DOCTYPE html>

<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    "on-tertiary-container": "#009e6d",
                    "on-tertiary": "#ffffff",
                    "surface-bright": "#f7f9fb",
                    "on-tertiary-fixed": "#002113",
                    "secondary-fixed-dim": "#b4c5ff",
                    "inverse-primary": "#b0c8eb",
                    "on-primary-fixed-variant": "#314865",
                    "primary": "#000f22",
                    "error": "#ba1a1a",
                    "primary-fixed": "#d2e4ff",
                    "tertiary-container": "#002a1a",
                    "on-secondary-fixed": "#00174b",
                    "surface-container": "#eceef0",
                    "on-background": "#191c1e",
                    "on-surface-variant": "#43474d",
                    "secondary-container": "#316bf3",
                    "error-container": "#ffdad6",
                    "primary-container": "#0a2540",
                    "inverse-surface": "#2d3133",
                    "surface": "#f7f9fb",
                    "surface-variant": "#e0e3e5",
                    "on-error": "#ffffff",
                    "tertiary-fixed-dim": "#4edea3",
                    "surface-container-lowest": "#ffffff",
                    "surface-tint": "#49607e",
                    "primary-fixed-dim": "#b0c8eb",
                    "on-tertiary-fixed-variant": "#005236",
                    "tertiary-fixed": "#6ffbbe",
                    "surface-container-high": "#e6e8ea",
                    "tertiary": "#001209",
                    "surface-container-highest": "#e0e3e5",
                    "secondary": "#0051d5",
                    "surface-container-low": "#f2f4f6",
                    "on-secondary": "#ffffff",
                    "outline": "#74777e",
                    "background": "#f7f9fb",
                    "on-error-container": "#93000a",
                    "surface-dim": "#d8dadc",
                    "on-surface": "#191c1e",
                    "on-primary-fixed": "#001c37",
                    "secondary-fixed": "#dbe1ff",
                    "on-secondary-fixed-variant": "#003ea8",
                    "on-primary": "#ffffff",
                    "outline-variant": "#c4c6ce",
                    "inverse-on-surface": "#eff1f3",
                    "on-primary-container": "#768dad",
                    "on-secondary-container": "#fefcff"
            },
            "borderRadius": {
                    "DEFAULT": "0.125rem",
                    "lg": "0.25rem",
                    "xl": "0.5rem",
                    "full": "0.75rem"
            },
            "fontFamily": {
                    "headline": ["Inter"],
                    "body": ["Inter"],
                    "label": ["Inter"],
                    "mono": ["JetBrains Mono"]
            }
          },
        },
      }
    </script>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #e0e3e5;
            border-radius: 10px;
        }
    </style>
</head>
<body class="bg-surface text-on-surface font-body overflow-hidden">
<!-- Top Navigation -->
<nav class="fixed top-0 w-full z-50 bg-slate-950/70 backdrop-blur-xl flex justify-between items-center px-8 h-16 w-full">
<div class="flex items-center gap-8">
<span class="text-xl font-bold tracking-tighter text-slate-50 font-headline">Sentinel AI</span>
<div class="hidden md:flex gap-6">
<a class="text-blue-500 border-b-2 border-blue-500 pb-1 font-['Inter'] tracking-tight transition-colors duration-200" href="#">Status</a>
<a class="text-slate-400 hover:text-slate-200 font-['Inter'] tracking-tight transition-colors duration-200" href="#">Protocols</a>
<a class="text-slate-400 hover:text-slate-200 font-['Inter'] tracking-tight transition-colors duration-200" href="#">Archive</a>
</div>
</div>
<div class="flex items-center gap-4">
<div class="relative hidden lg:block">
<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">search</span>
<input class="bg-slate-900 border-none text-slate-200 text-xs py-2 pl-10 pr-4 rounded-lg w-64 focus:ring-1 focus:ring-blue-500 font-mono" placeholder="Search Patient ID..." type="text"/>
</div>
<button class="text-slate-400 hover:text-slate-200 transition-colors">
<span class="material-symbols-outlined">notifications</span>
</button>
<button class="text-slate-400 hover:text-slate-200 transition-colors">
<span class="material-symbols-outlined">settings</span>
</button>
<div class="w-8 h-8 rounded-full overflow-hidden border border-slate-700">
<img alt="Chief Medical Officer Profile" data-alt="Close-up portrait of a professional doctor in medical attire, high-end clinical aesthetic with soft studio lighting" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCSTgJpEu5Hw8G5J9z_tEUPXph9d_XqSjufQlLt9TzsMCcCm-DimjC_mHG7Br82gGtX5RtlKaozQxjqKkOYiUus2DYpzG2qOehhgjXziaXrHRCcNwsd7FCogCZx6l08gbk2OYX_h2gUXZKVJRzFszKlV-5LSSpgmhHA3n9JRosvX5IkpdsC6O-uP4ezhSZCOxjdbdORoaRsdK1qrcz3ycBkEzDaqIiO8GmPKKOnz5-xqb23s5iu7x78b33iGkqneMmDLEnef5mV16Q"/>
</div>
</div>
</nav>
<!-- Side Navigation (Mobile Hidden) -->
<aside class="hidden lg:flex flex-col py-6 h-screen w-64 fixed left-0 top-16 bg-slate-950 border-r border-slate-800/50 z-40">
<div class="px-6 mb-8">
<div class="flex items-center gap-3 mb-2">
<div class="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
<span class="text-blue-500 font-bold font-mono text-xs tracking-widest uppercase">Precision Sentinel</span>
</div>
<p class="text-[10px] text-slate-500 font-mono uppercase tracking-[0.2em]">Clinical Node 04</p>
</div>
<nav class="flex-1 space-y-1 px-3">
<a class="flex items-center gap-4 px-4 py-3 bg-slate-900 text-blue-400 border-r-4 border-blue-500 font-mono text-xs tracking-widest uppercase transition-all duration-300" href="#">
<span class="material-symbols-outlined">dashboard</span>
<span>Dashboard</span>
</a>
<a class="flex items-center gap-4 px-4 py-3 text-slate-500 hover:bg-slate-900/50 hover:text-slate-300 font-mono text-xs tracking-widest uppercase transition-all duration-300" href="#">
<span class="material-symbols-outlined">biotech</span>
<span>Live Analysis</span>
</a>
<a class="flex items-center gap-4 px-4 py-3 text-slate-500 hover:bg-slate-900/50 hover:text-slate-300 font-mono text-xs tracking-widest uppercase transition-all duration-300" href="#">
<span class="material-symbols-outlined">assignment_ind</span>
<span>Patient Records</span>
</a>
<a class="flex items-center gap-4 px-4 py-3 text-slate-500 hover:bg-slate-900/50 hover:text-slate-300 font-mono text-xs tracking-widest uppercase transition-all duration-300" href="#">
<span class="material-symbols-outlined">psychology</span>
<span>Neural Insights</span>
</a>
<a class="flex items-center gap-4 px-4 py-3 text-slate-500 hover:bg-slate-900/50 hover:text-slate-300 font-mono text-xs tracking-widest uppercase transition-all duration-300" href="#">
<span class="material-symbols-outlined">query_stats</span>
<span>Lab Reports</span>
</a>
</nav>
<div class="px-6 pt-6 border-t border-slate-900">
<button class="w-full bg-secondary text-white rounded-full py-3 text-xs font-bold tracking-widest uppercase transition-all hover:scale-[0.98] active:scale-95 duration-200">
                New Analysis
            </button>
</div>
<div class="mt-auto px-3 pb-20 lg:pb-6 space-y-1">
<a class="flex items-center gap-4 px-4 py-3 text-slate-500 hover:text-slate-300 font-mono text-xs tracking-widest uppercase" href="#">
<span class="material-symbols-outlined">help_outline</span>
<span>Support</span>
</a>
<a class="flex items-center gap-4 px-4 py-3 text-slate-500 hover:text-slate-300 font-mono text-xs tracking-widest uppercase" href="#">
<span class="material-symbols-outlined">logout</span>
<span>Sign Out</span>
</a>
</div>
</aside>
<!-- Main Content Split Layout -->
<main class="pt-16 lg:pl-64 flex h-screen overflow-hidden">
<!-- Left Panel: Input (45%) -->
<section class="w-full lg:w-[45%] h-full bg-surface p-8 overflow-y-auto custom-scrollbar flex flex-col">
<header class="mb-10">
<h1 class="text-4xl font-extrabold tracking-tighter text-primary mb-2">Input MediAgent</h1>
<p class="text-on-surface-variant text-sm font-medium">Initiate deep neural diagnostic sequence by uploading clinical assets.</p>
</header>
<div class="space-y-8 flex-1">
<!-- Upload Zones Bento -->
<div class="grid grid-cols-2 gap-4">
<div class="bg-surface-container-low p-6 rounded-xl border border-transparent hover:border-secondary/20 transition-all cursor-pointer group">
<div class="w-10 h-10 bg-primary-container rounded-lg flex items-center justify-center mb-4 text-on-primary-container group-hover:bg-secondary group-hover:text-white transition-colors">
<span class="material-symbols-outlined">radiology</span>
</div>
<p class="text-primary font-bold text-sm mb-1">Medical Images</p>
<p class="text-on-surface-variant text-[10px] uppercase font-mono tracking-widest">DICOM, JPG, PNG</p>
</div>
<div class="bg-surface-container-low p-6 rounded-xl border border-transparent hover:border-secondary/20 transition-all cursor-pointer group">
<div class="w-10 h-10 bg-primary-container rounded-lg flex items-center justify-center mb-4 text-on-primary-container group-hover:bg-secondary group-hover:text-white transition-colors">
<span class="material-symbols-outlined">picture_as_pdf</span>
</div>
<p class="text-primary font-bold text-sm mb-1">Lab Reports</p>
<p class="text-on-surface-variant text-[10px] uppercase font-mono tracking-widest">PDF, HL7 Data</p>
</div>
</div>
<!-- Text Input -->
<div class="space-y-3">
<label class="text-xs font-bold uppercase tracking-widest text-on-surface-variant font-mono">Symptom Description</label>
<textarea class="w-full h-40 bg-surface-container-highest border-none rounded-lg p-4 text-sm font-body text-primary focus:ring-0 focus:bg-surface-container-lowest focus:border-b-2 focus:border-secondary transition-all resize-none" placeholder="Provide clinical observations, patient history, and primary complaints..."></textarea>
</div>
<!-- Voice Recorder Card -->
<div class="bg-primary-container text-white p-6 rounded-xl flex items-center justify-between">
<div class="flex items-center gap-4">
<div class="relative">
<div class="w-12 h-12 bg-secondary rounded-full flex items-center justify-center shadow-lg shadow-secondary/20">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">mic</span>
</div>
<div class="absolute inset-0 rounded-full border-2 border-secondary animate-ping opacity-25"></div>
</div>
<div>
<p class="text-sm font-bold">Record Symptoms</p>
<p class="text-[10px] font-mono text-on-primary-container uppercase tracking-widest">Active Voice Transcription</p>
</div>
</div>
<div class="flex items-end gap-1 h-8">
<div class="w-1 h-3 bg-secondary rounded-full"></div>
<div class="w-1 h-6 bg-secondary rounded-full"></div>
<div class="w-1 h-4 bg-secondary rounded-full"></div>
<div class="w-1 h-7 bg-secondary rounded-full"></div>
<div class="w-1 h-5 bg-secondary rounded-full"></div>
<div class="w-1 h-2 bg-secondary rounded-full"></div>
<div class="w-1 h-6 bg-secondary rounded-full"></div>
<div class="w-1 h-4 bg-secondary rounded-full"></div>
</div>
</div>
</div>
<div class="pt-10">
<button class="w-full bg-primary text-white py-5 rounded-full font-bold flex items-center justify-center gap-3 hover:bg-slate-900 transition-all hover:gap-5">
                    Run Clinical Analysis
                    <span class="material-symbols-outlined">arrow_forward</span>
</button>
</div>
</section>
<!-- Right Panel: Status & Feed (55%) -->
<section class="hidden lg:flex w-[55%] h-full bg-surface-container-low border-l border-outline-variant/10 flex-col">
<!-- System Status Grid -->
<div class="p-8">
<div class="flex flex-wrap gap-3">
<div class="bg-surface-container-lowest px-4 py-2 rounded-full flex items-center gap-2 border border-outline-variant/20 shadow-sm">
<div class="w-1.5 h-1.5 bg-on-tertiary-container rounded-full"></div>
<span class="text-[10px] font-mono font-bold tracking-tighter">LLaVA 13B</span>
<span class="text-[9px] text-on-tertiary-container font-mono">READY</span>
</div>
<div class="bg-surface-container-lowest px-4 py-2 rounded-full flex items-center gap-2 border border-outline-variant/20 shadow-sm">
<div class="w-1.5 h-1.5 bg-on-tertiary-container rounded-full"></div>
<span class="text-[10px] font-mono font-bold tracking-tighter">LLAMA 3.1</span>
<span class="text-[9px] text-on-tertiary-container font-mono">STABLE</span>
</div>
<div class="bg-surface-container-lowest px-4 py-2 rounded-full flex items-center gap-2 border border-outline-variant/20 shadow-sm">
<div class="w-1.5 h-1.5 bg-amber-500 rounded-full"></div>
<span class="text-[10px] font-mono font-bold tracking-tighter">CHROMADB</span>
<span class="text-[9px] text-amber-500 font-mono">INDEXING</span>
</div>
<div class="bg-surface-container-lowest px-4 py-2 rounded-full flex items-center gap-2 border border-outline-variant/20 shadow-sm">
<div class="w-1.5 h-1.5 bg-on-tertiary-container rounded-full"></div>
<span class="text-[10px] font-mono font-bold tracking-tighter">PUBMED API</span>
<span class="text-[9px] text-on-tertiary-container font-mono">SYNCED</span>
</div>
</div>
</div>
<!-- Empty State Area -->
<div class="flex-1 flex flex-col items-center justify-center p-12 text-center">
<div class="w-32 h-32 mb-8 relative">
<div class="absolute inset-0 bg-secondary/5 rounded-full blur-2xl"></div>
<div class="relative w-full h-full bg-surface-container-lowest rounded-2xl flex items-center justify-center border border-outline-variant/15 rotate-3 hover:rotate-0 transition-transform duration-500">
<span class="material-symbols-outlined text-5xl text-primary-container" style="font-variation-settings: 'wght' 200;">assignment</span>
<div class="absolute -bottom-4 -right-4 w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-lg border border-outline-variant/10">
<span class="material-symbols-outlined text-on-tertiary-container animate-pulse">favorite</span>
</div>
</div>
</div>
<h3 class="text-xl font-bold text-primary mb-2">Awaiting Diagnostic Data</h3>
<p class="text-on-surface-variant text-sm max-w-xs leading-relaxed">System is idle. Please provide patient inputs on the left panel to generate a cross-referenced clinical insight report.</p>
</div>
<!-- Recent Analysis Feed -->
<div class="p-8 bg-surface-container-lowest/50 border-t border-outline-variant/15">
<div class="flex justify-between items-center mb-6">
<h4 class="text-xs font-bold uppercase tracking-widest text-on-surface-variant font-mono">Recent Clinical Cycles</h4>
<button class="text-[10px] font-bold text-secondary uppercase tracking-widest hover:underline">View All</button>
</div>
<div class="space-y-4">
<div class="flex items-center gap-4 group cursor-pointer">
<div class="w-10 h-10 rounded-lg bg-surface-container-high flex items-center justify-center group-hover:bg-primary-container group-hover:text-white transition-colors">
<span class="material-symbols-outlined text-sm">description</span>
</div>
<div class="flex-1">
<div class="flex justify-between">
<span class="text-xs font-bold text-primary">Node-8291: Thoracic Scan</span>
<span class="text-[9px] font-mono text-on-surface-variant uppercase">14:20 PM</span>
</div>
<p class="text-[10px] text-on-surface-variant font-mono mt-0.5">COMPLETED · 0.4s LATENCY</p>
</div>
</div>
<div class="flex items-center gap-4 group cursor-pointer">
<div class="w-10 h-10 rounded-lg bg-surface-container-high flex items-center justify-center group-hover:bg-primary-container group-hover:text-white transition-colors">
<span class="material-symbols-outlined text-sm">analytics</span>
</div>
<div class="flex-1">
<div class="flex justify-between">
<span class="text-xs font-bold text-primary">Node-8288: Blood Chemistry</span>
<span class="text-[9px] font-mono text-on-surface-variant uppercase">09:15 AM</span>
</div>
<p class="text-[10px] text-on-tertiary-container font-mono mt-0.5">SUCCESS · HIGH CONFIDENCE</p>
</div>
</div>
</div>
</div>
</section>
</main>
<!-- Bottom Nav Bar (Mobile Only) -->
<nav class="md:hidden fixed bottom-0 w-full h-16 bg-white border-t border-slate-100 flex items-center justify-around px-4 z-50">
<button class="flex flex-col items-center gap-1 text-secondary">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">dashboard</span>
<span class="text-[10px] font-bold uppercase tracking-tighter">Input</span>
</button>
<button class="flex flex-col items-center gap-1 text-slate-400">
<span class="material-symbols-outlined">biotech</span>
<span class="text-[10px] font-bold uppercase tracking-tighter">Analysis</span>
</button>
<button class="flex flex-col items-center gap-1 text-slate-400">
<span class="material-symbols-outlined">assignment_ind</span>
<span class="text-[10px] font-bold uppercase tracking-tighter">Records</span>
</button>
<button class="flex flex-col items-center gap-1 text-slate-400">
<span class="material-symbols-outlined">psychology</span>
<span class="text-[10px] font-bold uppercase tracking-tighter">Insights</span>
</button>
</nav>
</body></html>

<!-- MediAgent - System Health Dashboard -->
<!DOCTYPE html>

<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    "on-tertiary-container": "#009e6d",
                    "on-tertiary": "#ffffff",
                    "surface-bright": "#f7f9fb",
                    "on-tertiary-fixed": "#002113",
                    "secondary-fixed-dim": "#b4c5ff",
                    "inverse-primary": "#b0c8eb",
                    "on-primary-fixed-variant": "#314865",
                    "primary": "#000f22",
                    "error": "#ba1a1a",
                    "primary-fixed": "#d2e4ff",
                    "tertiary-container": "#002a1a",
                    "on-secondary-fixed": "#00174b",
                    "surface-container": "#eceef0",
                    "on-background": "#191c1e",
                    "on-surface-variant": "#43474d",
                    "secondary-container": "#316bf3",
                    "error-container": "#ffdad6",
                    "primary-container": "#0a2540",
                    "inverse-surface": "#2d3133",
                    "surface": "#f7f9fb",
                    "surface-variant": "#e0e3e5",
                    "on-error": "#ffffff",
                    "tertiary-fixed-dim": "#4edea3",
                    "surface-container-lowest": "#ffffff",
                    "surface-tint": "#49607e",
                    "primary-fixed-dim": "#b0c8eb",
                    "on-tertiary-fixed-variant": "#005236",
                    "tertiary-fixed": "#6ffbbe",
                    "surface-container-high": "#e6e8ea",
                    "tertiary": "#001209",
                    "surface-container-highest": "#e0e3e5",
                    "secondary": "#0051d5",
                    "surface-container-low": "#f2f4f6",
                    "on-secondary": "#ffffff",
                    "outline": "#74777e",
                    "background": "#f7f9fb",
                    "on-error-container": "#93000a",
                    "surface-dim": "#d8dadc",
                    "on-surface": "#191c1e",
                    "on-primary-fixed": "#001c37",
                    "secondary-fixed": "#dbe1ff",
                    "on-secondary-fixed-variant": "#003ea8",
                    "on-primary": "#ffffff",
                    "outline-variant": "#c4c6ce",
                    "inverse-on-surface": "#eff1f3",
                    "on-primary-container": "#768dad",
                    "on-secondary-container": "#fefcff"
            },
            "borderRadius": {
                    "DEFAULT": "0.125rem",
                    "lg": "0.25rem",
                    "xl": "0.5rem",
                    "full": "0.75rem"
            },
            "fontFamily": {
                    "headline": ["Inter"],
                    "body": ["Inter"],
                    "label": ["Inter"],
                    "mono": ["JetBrains Mono"]
            }
          },
        }
      }
    </script>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        body { font-family: 'Inter', sans-serif; }
        .mono-text { font-family: 'JetBrains Mono', monospace; }
    </style>
</head>
<body class="bg-surface text-on-background">
<!-- TopNavBar -->
<nav class="fixed top-0 w-full z-50 bg-slate-950/70 backdrop-blur-xl flex justify-between items-center px-8 h-16 w-full">
<div class="flex items-center gap-8">
<span class="text-xl font-bold tracking-tighter text-slate-50">Sentinel AI</span>
<div class="hidden md:flex gap-6">
<a class="text-blue-500 border-b-2 border-blue-500 pb-1 font-['Inter'] tracking-tight transition-colors duration-200" href="#">Status</a>
<a class="text-slate-400 hover:text-slate-200 font-['Inter'] tracking-tight transition-colors duration-200" href="#">Protocols</a>
<a class="text-slate-400 hover:text-slate-200 font-['Inter'] tracking-tight transition-colors duration-200" href="#">Archive</a>
</div>
</div>
<div class="flex items-center gap-4">
<button class="text-slate-400 hover:text-slate-200 transition-colors duration-200">
<span class="material-symbols-outlined">notifications</span>
</button>
<button class="text-slate-400 hover:text-slate-200 transition-colors duration-200">
<span class="material-symbols-outlined">settings</span>
</button>
<div class="w-8 h-8 rounded-full overflow-hidden bg-slate-800">
<img alt="Chief Medical Officer Profile" data-alt="Close-up portrait of a professional male doctor in a white clinical coat, minimalist lighting, serious and focused expression" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCsFNSBgKp3Xg9dwc46NE5hxHQBRlZkSpMSZ-tARmPMpXA4phc3OTQanbPBoGFM8ivWAbUH0j2nhm-_8_TFYxAk11nSljgxSWYNdMinkDLZbBDruqvNqCnzp2sKuMEZ3GXniZuXsKATj0bJCdT4Ux60WtyI4Mhg-Q2Y5bB-MHvtYdH12TAMzixvOiINNpSg6kFXS_aCfL5P8Yfw_XRxNl1kVFtTdyBDli8Rh6Ac-k_mlejvW5dz-hRQ7GKFpu53shJd2sTUwcwus00"/>
</div>
</div>
</nav>
<!-- SideNavBar -->
<aside class="h-screen w-64 fixed left-0 border-r border-slate-800/50 bg-slate-950 flex flex-col py-6 z-40 hidden md:flex">
<div class="px-6 mb-10">
<div class="flex items-center gap-3">
<div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">shield_with_heart</span>
</div>
<div>
<h2 class="text-blue-500 font-bold font-['JetBrains_Mono'] text-xs tracking-widest uppercase">Precision Sentinel</h2>
<p class="text-slate-500 text-[10px] tracking-widest uppercase">Clinical Node 04</p>
</div>
</div>
</div>
<nav class="flex-1 space-y-1">
<a class="flex items-center px-6 py-3 text-slate-500 hover:bg-slate-900/50 hover:text-slate-300 duration-300 ease-in-out font-['JetBrains_Mono'] text-xs tracking-widest uppercase" href="#">
<span class="material-symbols-outlined mr-3">dashboard</span> Dashboard
            </a>
<a class="flex items-center px-6 py-3 bg-slate-900 text-blue-400 border-r-4 border-blue-500 duration-300 ease-in-out font-['JetBrains_Mono'] text-xs tracking-widest uppercase" href="#">
<span class="material-symbols-outlined mr-3">biotech</span> Live Analysis
            </a>
<a class="flex items-center px-6 py-3 text-slate-500 hover:bg-slate-900/50 hover:text-slate-300 duration-300 ease-in-out font-['JetBrains_Mono'] text-xs tracking-widest uppercase" href="#">
<span class="material-symbols-outlined mr-3">assignment_ind</span> Patient Records
            </a>
<a class="flex items-center px-6 py-3 text-slate-500 hover:bg-slate-900/50 hover:text-slate-300 duration-300 ease-in-out font-['JetBrains_Mono'] text-xs tracking-widest uppercase" href="#">
<span class="material-symbols-outlined mr-3">psychology</span> Neural Insights
            </a>
<a class="flex items-center px-6 py-3 text-slate-500 hover:bg-slate-900/50 hover:text-slate-300 duration-300 ease-in-out font-['JetBrains_Mono'] text-xs tracking-widest uppercase" href="#">
<span class="material-symbols-outlined mr-3">query_stats</span> Lab Reports
            </a>
</nav>
<div class="px-6 mb-4">
<button class="w-full py-3 bg-secondary text-on-secondary rounded-full font-bold text-xs tracking-widest uppercase shadow-lg shadow-blue-900/20">
                New Analysis
            </button>
</div>
<div class="px-2 mt-auto border-t border-slate-800/50 pt-4">
<a class="flex items-center px-4 py-2 text-slate-500 hover:text-slate-300 font-['JetBrains_Mono'] text-xs tracking-widest uppercase" href="#">
<span class="material-symbols-outlined mr-3">help_outline</span> Support
            </a>
<a class="flex items-center px-4 py-2 text-slate-500 hover:text-slate-300 font-['JetBrains_Mono'] text-xs tracking-widest uppercase" href="#">
<span class="material-symbols-outlined mr-3">logout</span> Sign Out
            </a>
</div>
</aside>
<!-- Main Content -->
<main class="md:ml-64 pt-24 px-8 pb-12">
<header class="mb-12">
<h1 class="text-4xl font-bold tracking-tighter text-primary mb-2">System Status</h1>
<p class="text-on-surface-variant font-medium">MediAgent Clinical Diagnostics Cluster — Operational</p>
</header>
<!-- Model Status Grid (2x2) -->
<section class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
<!-- LLaVA Card -->
<div class="bg-surface-container-low rounded-xl p-8 transition-colors duration-300 hover:bg-surface-container-high relative overflow-hidden">
<div class="flex justify-between items-start mb-6">
<div>
<span class="mono-text text-[10px] uppercase tracking-widest text-secondary font-bold">Vision LLM</span>
<h3 class="text-2xl font-bold tracking-tight text-primary">LLaVA-v1.6-34b</h3>
</div>
<span class="bg-tertiary-container text-on-tertiary-container px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider flex items-center">
<span class="w-1.5 h-1.5 rounded-full bg-on-tertiary-container mr-2"></span> Operational
                    </span>
</div>
<div class="grid grid-cols-2 gap-4 mono-text text-sm">
<div class="p-4 bg-surface-container-lowest rounded-lg">
<p class="text-on-surface-variant text-[10px] uppercase mb-1">RAM Usage</p>
<p class="text-primary font-medium">21.4 / 32.0 GB</p>
<div class="w-full bg-surface-variant h-1 rounded-full mt-2 overflow-hidden">
<div class="bg-secondary h-full" style="width: 67%"></div>
</div>
</div>
<div class="p-4 bg-surface-container-lowest rounded-lg">
<p class="text-on-surface-variant text-[10px] uppercase mb-1">Inference Latency</p>
<p class="text-primary font-medium">1.2s avg</p>
</div>
</div>
</div>
<!-- LLaMA Card -->
<div class="bg-surface-container-low rounded-xl p-8 transition-colors duration-300 hover:bg-surface-container-high relative overflow-hidden">
<div class="flex justify-between items-start mb-6">
<div>
<span class="mono-text text-[10px] uppercase tracking-widest text-secondary font-bold">Reasoning Engine</span>
<h3 class="text-2xl font-bold tracking-tight text-primary">LLaMA-3-70b-Med</h3>
</div>
<span class="bg-tertiary-container text-on-tertiary-container px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider flex items-center">
<span class="w-1.5 h-1.5 rounded-full bg-on-tertiary-container mr-2"></span> Operational
                    </span>
</div>
<div class="grid grid-cols-2 gap-4 mono-text text-sm">
<div class="p-4 bg-surface-container-lowest rounded-lg">
<p class="text-on-surface-variant text-[10px] uppercase mb-1">VRAM Usage</p>
<p class="text-primary font-medium">48.2 / 80.0 GB</p>
<div class="w-full bg-surface-variant h-1 rounded-full mt-2 overflow-hidden">
<div class="bg-secondary h-full" style="width: 60%"></div>
</div>
</div>
<div class="p-4 bg-surface-container-lowest rounded-lg">
<p class="text-on-surface-variant text-[10px] uppercase mb-1">Throughput</p>
<p class="text-primary font-medium">42 tokens/s</p>
</div>
</div>
</div>
<!-- Whisper Card -->
<div class="bg-surface-container-low rounded-xl p-8 transition-colors duration-300 hover:bg-surface-container-high relative overflow-hidden">
<div class="flex justify-between items-start mb-6">
<div>
<span class="mono-text text-[10px] uppercase tracking-widest text-secondary font-bold">Transcription</span>
<h3 class="text-2xl font-bold tracking-tight text-primary">Whisper-v3-Large</h3>
</div>
<span class="bg-tertiary-container text-on-tertiary-container px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider flex items-center">
<span class="w-1.5 h-1.5 rounded-full bg-on-tertiary-container mr-2"></span> Operational
                    </span>
</div>
<div class="grid grid-cols-2 gap-4 mono-text text-sm">
<div class="p-4 bg-surface-container-lowest rounded-lg">
<p class="text-on-surface-variant text-[10px] uppercase mb-1">RAM Usage</p>
<p class="text-primary font-medium">4.8 / 8.0 GB</p>
<div class="w-full bg-surface-variant h-1 rounded-full mt-2 overflow-hidden">
<div class="bg-secondary h-full" style="width: 60%"></div>
</div>
</div>
<div class="p-4 bg-surface-container-lowest rounded-lg">
<p class="text-on-surface-variant text-[10px] uppercase mb-1">Accuracy Meta</p>
<p class="text-primary font-medium">98.4% WER</p>
</div>
</div>
</div>
<!-- Embedding Card -->
<div class="bg-surface-container-low rounded-xl p-8 transition-colors duration-300 hover:bg-surface-container-high relative overflow-hidden">
<div class="flex justify-between items-start mb-6">
<div>
<span class="mono-text text-[10px] uppercase tracking-widest text-secondary font-bold">Vectorization</span>
<h3 class="text-2xl font-bold tracking-tight text-primary">Bio-BERT-Embeddings</h3>
</div>
<span class="bg-secondary-container text-on-secondary-container px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider flex items-center">
<span class="w-1.5 h-1.5 rounded-full bg-white mr-2"></span> Heavy Load
                    </span>
</div>
<div class="grid grid-cols-2 gap-4 mono-text text-sm">
<div class="p-4 bg-surface-container-lowest rounded-lg">
<p class="text-on-surface-variant text-[10px] uppercase mb-1">RAM Usage</p>
<p class="text-primary font-medium">2.1 / 4.0 GB</p>
<div class="w-full bg-surface-variant h-1 rounded-full mt-2 overflow-hidden">
<div class="bg-secondary h-full" style="width: 52%"></div>
</div>
</div>
<div class="p-4 bg-surface-container-lowest rounded-lg">
<p class="text-on-surface-variant text-[10px] uppercase mb-1">Queue Size</p>
<p class="text-secondary font-medium">1,242 docs</p>
</div>
</div>
</div>
</section>
<!-- Asymmetric Mid Section -->
<div class="flex flex-col lg:flex-row gap-8 mb-12">
<!-- ChromaDB Section -->
<section class="lg:w-2/3 bg-surface-container-low rounded-xl p-8">
<div class="flex items-center justify-between mb-8">
<div class="flex items-center gap-4">
<div class="w-12 h-12 bg-primary-container flex items-center justify-center rounded-lg">
<span class="material-symbols-outlined text-secondary" style="font-variation-settings: 'FILL' 1;">database</span>
</div>
<div>
<h2 class="text-xl font-bold tracking-tight">ChromaDB Vector Store</h2>
<p class="text-on-surface-variant text-sm">Cluster ID: CHR-9921-MED</p>
</div>
</div>
<div class="text-right">
<p class="mono-text text-2xl font-bold text-primary">12.4M</p>
<p class="text-[10px] uppercase tracking-widest text-on-surface-variant font-bold">Total Embeddings</p>
</div>
</div>
<div class="space-y-6">
<div class="flex items-center gap-6">
<div class="flex-1">
<div class="flex justify-between mb-2">
<span class="mono-text text-[10px] uppercase font-bold">Clinical Case Records</span>
<span class="mono-text text-[10px]">8.2M Docs</span>
</div>
<div class="w-full h-2 bg-surface-container-highest rounded-full overflow-hidden">
<div class="bg-secondary h-full" style="width: 66%"></div>
</div>
</div>
<div class="flex-1">
<div class="flex justify-between mb-2">
<span class="mono-text text-[10px] uppercase font-bold">Research Papers</span>
<span class="mono-text text-[10px]">4.2M Docs</span>
</div>
<div class="w-full h-2 bg-surface-container-highest rounded-full overflow-hidden">
<div class="bg-on-tertiary-container h-full" style="width: 34%"></div>
</div>
</div>
</div>
<div class="bg-surface-container-lowest p-6 rounded-lg grid grid-cols-3 gap-8">
<div>
<p class="text-[10px] uppercase text-on-surface-variant mb-1 font-bold">Index Size</p>
<p class="mono-text text-lg font-medium">84.2 GB</p>
</div>
<div>
<p class="text-[10px] uppercase text-on-surface-variant mb-1 font-bold">Query Latency</p>
<p class="mono-text text-lg font-medium text-on-tertiary-container">14ms</p>
</div>
<div>
<p class="text-[10px] uppercase text-on-surface-variant mb-1 font-bold">Health Score</p>
<p class="mono-text text-lg font-medium">99.9%</p>
</div>
</div>
</div>
</section>
<!-- PubMed API Section -->
<section class="lg:w-1/3 bg-slate-950 text-white rounded-xl p-8 flex flex-col justify-between">
<div>
<div class="flex items-center gap-3 mb-6">
<span class="material-symbols-outlined text-blue-500">api</span>
<h2 class="text-xl font-bold tracking-tight">PubMed API Status</h2>
</div>
<div class="space-y-6">
<div>
<p class="mono-text text-[10px] uppercase tracking-widest text-slate-500 mb-2">Current Rate Limit</p>
<div class="flex items-end justify-between mb-2">
<p class="text-3xl font-bold">8,421<span class="text-sm font-normal text-slate-400">/10k</span></p>
<p class="text-blue-400 mono-text text-xs">84% Capacity</p>
</div>
<div class="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
<div class="bg-blue-600 h-full" style="width: 84%"></div>
</div>
</div>
<div class="grid grid-cols-2 gap-4">
<div class="p-4 border border-slate-800 rounded-lg">
<p class="text-[10px] uppercase text-slate-500 mb-1">Status</p>
<p class="text-sm font-bold text-emerald-400">Stable</p>
</div>
<div class="p-4 border border-slate-800 rounded-lg">
<p class="text-[10px] uppercase text-slate-500 mb-1">Latency</p>
<p class="text-sm font-bold">245ms</p>
</div>
</div>
</div>
</div>
<div class="mt-8 pt-6 border-t border-slate-800">
<button class="w-full py-2 border border-slate-700 text-slate-400 rounded-full text-[10px] uppercase tracking-widest font-bold hover:bg-slate-900 transition-colors">
                        View API Documentation
                    </button>
</div>
</section>
</div>
<!-- Recent Errors Log (Collapsible) -->
<section class="bg-surface-container-low rounded-xl overflow-hidden">
<details class="group" open="">
<summary class="flex items-center justify-between p-6 cursor-pointer hover:bg-surface-container-high transition-colors list-none">
<div class="flex items-center gap-4">
<span class="material-symbols-outlined text-error" style="font-variation-settings: 'FILL' 1;">warning</span>
<h2 class="text-xl font-bold tracking-tight">Recent System Logs &amp; Faults</h2>
</div>
<span class="material-symbols-outlined transform group-open:rotate-180 transition-transform duration-300">expand_more</span>
</summary>
<div class="px-6 pb-6 border-t border-outline-variant/10">
<table class="w-full text-left mono-text text-[11px]">
<thead>
<tr class="text-on-surface-variant uppercase tracking-widest border-b border-outline-variant/20">
<th class="py-4 px-2">Timestamp</th>
<th class="py-4 px-2">Origin</th>
<th class="py-4 px-2">Severity</th>
<th class="py-4 px-2">Event Description</th>
<th class="py-4 px-2">Action</th>
</tr>
</thead>
<tbody class="divide-y divide-outline-variant/10">
<tr class="hover:bg-surface-container-highest transition-colors">
<td class="py-3 px-2 text-on-surface-variant">2024-05-24 14:22:01</td>
<td class="py-3 px-2 font-bold">LLaMA-3-Node-01</td>
<td class="py-3 px-2">
<span class="bg-error-container text-on-error-container px-2 py-0.5 rounded text-[9px] font-bold">CRITICAL</span>
</td>
<td class="py-3 px-2">OOM (Out of Memory) Exception during large context retrieval [ID: ERR-902]</td>
<td class="py-3 px-2 text-secondary cursor-pointer hover:underline">Reboot Node</td>
</tr>
<tr class="hover:bg-surface-container-highest transition-colors">
<td class="py-3 px-2 text-on-surface-variant">2024-05-24 13:58:44</td>
<td class="py-3 px-2 font-bold">PubMed-Bridge</td>
<td class="py-3 px-2">
<span class="bg-surface-variant text-on-surface-variant px-2 py-0.5 rounded text-[9px] font-bold">WARNING</span>
</td>
<td class="py-3 px-2">Latency threshold exceeded (500ms+) for query sequence "GLP-1 mechanism"</td>
<td class="py-3 px-2 text-secondary cursor-pointer hover:underline">Inspect</td>
</tr>
<tr class="hover:bg-surface-container-highest transition-colors">
<td class="py-3 px-2 text-on-surface-variant">2024-05-24 12:44:12</td>
<td class="py-3 px-2 font-bold">ChromaDB-V-02</td>
<td class="py-3 px-2">
<span class="bg-surface-variant text-on-surface-variant px-2 py-0.5 rounded text-[9px] font-bold">INFO</span>
</td>
<td class="py-3 px-2">Index optimization routine completed successfully. 4.2k nodes merged.</td>
<td class="py-3 px-2 text-secondary cursor-pointer hover:underline">View Log</td>
</tr>
</tbody>
</table>
</div>
</details>
</section>
</main>
<!-- Bottom Navigation for Mobile -->
<nav class="md:hidden fixed bottom-0 left-0 w-full bg-slate-950 px-6 py-3 flex justify-around items-center border-t border-slate-800 z-50">
<button class="text-blue-500 flex flex-col items-center gap-1">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">dashboard</span>
<span class="text-[9px] font-bold uppercase tracking-widest">Dash</span>
</button>
<button class="text-slate-500 flex flex-col items-center gap-1">
<span class="material-symbols-outlined">biotech</span>
<span class="text-[9px] font-bold uppercase tracking-widest">Live</span>
</button>
<button class="text-slate-500 flex flex-col items-center gap-1">
<span class="material-symbols-outlined">psychology</span>
<span class="text-[9px] font-bold uppercase tracking-widest">AI</span>
</button>
<button class="text-slate-500 flex flex-col items-center gap-1">
<span class="material-symbols-outlined">person</span>
<span class="text-[9px] font-bold uppercase tracking-widest">User</span>
</button>
</nav>
</body></html>

<!-- MediAgent - Clinical Analysis Results -->
<!DOCTYPE html>

<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>MediAgent — Analysis Results</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=JetBrains+Mono:wght@400;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                        "on-tertiary-container": "#009e6d",
                        "on-tertiary": "#ffffff",
                        "surface-bright": "#f7f9fb",
                        "on-tertiary-fixed": "#002113",
                        "secondary-fixed-dim": "#b4c5ff",
                        "inverse-primary": "#b0c8eb",
                        "on-primary-fixed-variant": "#314865",
                        "primary": "#000f22",
                        "error": "#ba1a1a",
                        "primary-fixed": "#d2e4ff",
                        "tertiary-container": "#002a1a",
                        "on-secondary-fixed": "#00174b",
                        "surface-container": "#eceef0",
                        "on-background": "#191c1e",
                        "on-surface-variant": "#43474d",
                        "secondary-container": "#316bf3",
                        "error-container": "#ffdad6",
                        "primary-container": "#0a2540",
                        "inverse-surface": "#2d3133",
                        "surface": "#f7f9fb",
                        "surface-variant": "#e0e3e5",
                        "on-error": "#ffffff",
                        "tertiary-fixed-dim": "#4edea3",
                        "surface-container-lowest": "#ffffff",
                        "surface-tint": "#49607e",
                        "primary-fixed-dim": "#b0c8eb",
                        "on-tertiary-fixed-variant": "#005236",
                        "tertiary-fixed": "#6ffbbe",
                        "surface-container-high": "#e6e8ea",
                        "tertiary": "#001209",
                        "surface-container-highest": "#e0e3e5",
                        "secondary": "#0051d5",
                        "surface-container-low": "#f2f4f6",
                        "on-secondary": "#ffffff",
                        "outline": "#74777e",
                        "background": "#f7f9fb",
                        "on-error-container": "#93000a",
                        "surface-dim": "#d8dadc",
                        "on-surface": "#191c1e",
                        "on-primary-fixed": "#001c37",
                        "secondary-fixed": "#dbe1ff",
                        "on-secondary-fixed-variant": "#003ea8",
                        "on-primary": "#ffffff",
                        "outline-variant": "#c4c6ce",
                        "inverse-on-surface": "#eff1f3",
                        "on-primary-container": "#768dad",
                        "on-secondary-container": "#fefcff"
                    },
                    "borderRadius": {
                        "DEFAULT": "0.125rem",
                        "lg": "0.25rem",
                        "xl": "0.5rem",
                        "full": "0.75rem"
                    },
                    "fontFamily": {
                        "headline": ["Inter"],
                        "body": ["Inter"],
                        "label": ["Inter"],
                        "mono": ["JetBrains Mono"]
                    }
                },
            },
        }
    </script>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .radial-progress {
            --value: 87;
            --size: 3rem;
            --thickness: 4px;
            display: inline-grid;
            place-content: center;
            width: var(--size);
            height: var(--size);
            border-radius: 50%;
            background: radial-gradient(closest-side, white 80%, transparent 0),
                        conic-gradient(#009e6d calc(var(--value) * 1%), #eceef0 0);
        }
    </style>
</head>
<body class="bg-background text-on-surface font-body antialiased">
<!-- TopNavBar from Shared Components -->
<header class="fixed top-0 w-full z-50 bg-slate-950/70 backdrop-blur-xl flex justify-between items-center px-8 h-16 w-full">
<div class="flex items-center gap-8">
<span class="text-xl font-bold tracking-tighter text-slate-50">Sentinel AI</span>
<nav class="hidden md:flex gap-6">
<a class="text-slate-400 hover:text-slate-200 transition-colors duration-200 text-sm font-medium" href="#">Status</a>
<a class="text-slate-400 hover:text-slate-200 transition-colors duration-200 text-sm font-medium" href="#">Protocols</a>
<a class="text-slate-400 hover:text-slate-200 transition-colors duration-200 text-sm font-medium" href="#">Archive</a>
</nav>
</div>
<div class="flex items-center gap-4">
<div class="bg-amber-500/10 border border-amber-500/20 px-3 py-1 rounded-full flex items-center gap-2">
<span class="w-2 h-2 bg-amber-500 rounded-full animate-pulse"></span>
<span class="text-[10px] font-bold tracking-widest text-amber-500 uppercase">URGENT - Amber</span>
</div>
<div class="flex gap-3 text-slate-400">
<span class="material-symbols-outlined cursor-pointer hover:text-white transition-colors">notifications</span>
<span class="material-symbols-outlined cursor-pointer hover:text-white transition-colors">settings</span>
</div>
</div>
</header>
<!-- SideNavBar from Shared Components -->
<aside class="h-screen w-64 fixed left-0 border-r border-slate-800/50 bg-slate-950 flex flex-col py-6 hidden lg:flex">
<div class="px-6 mb-8">
<div class="flex items-center gap-3">
<div class="w-8 h-8 rounded bg-blue-600 flex items-center justify-center">
<span class="material-symbols-outlined text-white text-sm" style="font-variation-settings: 'FILL' 1;">security</span>
</div>
<div>
<h2 class="text-blue-500 font-bold text-sm tracking-tight">Precision Sentinel</h2>
<p class="text-[10px] text-slate-500 font-mono uppercase tracking-widest">Clinical Node 04</p>
</div>
</div>
</div>
<nav class="flex-1 flex flex-col gap-1">
<a class="flex items-center gap-4 px-6 py-3 text-slate-500 hover:bg-slate-900/50 hover:text-slate-300 transition-all duration-300" href="#">
<span class="material-symbols-outlined text-xl">dashboard</span>
<span class="font-mono text-xs tracking-widest uppercase">Dashboard</span>
</a>
<a class="flex items-center gap-4 px-6 py-3 bg-slate-900 text-blue-400 border-r-4 border-blue-500 transition-all duration-300" href="#">
<span class="material-symbols-outlined text-xl" style="font-variation-settings: 'FILL' 1;">biotech</span>
<span class="font-mono text-xs tracking-widest uppercase">Live Analysis</span>
</a>
<a class="flex items-center gap-4 px-6 py-3 text-slate-500 hover:bg-slate-900/50 hover:text-slate-300 transition-all duration-300" href="#">
<span class="material-symbols-outlined text-xl">assignment_ind</span>
<span class="font-mono text-xs tracking-widest uppercase">Patient Records</span>
</a>
<a class="flex items-center gap-4 px-6 py-3 text-slate-500 hover:bg-slate-900/50 hover:text-slate-300 transition-all duration-300" href="#">
<span class="material-symbols-outlined text-xl">psychology</span>
<span class="font-mono text-xs tracking-widest uppercase">Neural Insights</span>
</a>
</nav>
<div class="px-6 mt-auto flex flex-col gap-4">
<button class="bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-full text-xs font-bold uppercase tracking-widest transition-transform active:scale-95">
                New Analysis
            </button>
<div class="flex flex-col gap-1 border-t border-slate-800/50 pt-4">
<a class="flex items-center gap-4 py-2 text-slate-500 hover:text-slate-300 text-xs font-mono uppercase tracking-widest transition-colors" href="#">
<span class="material-symbols-outlined text-lg">help_outline</span>
                    Support
                </a>
<a class="flex items-center gap-4 py-2 text-slate-500 hover:text-slate-300 text-xs font-mono uppercase tracking-widest transition-colors" href="#">
<span class="material-symbols-outlined text-lg">logout</span>
                    Sign Out
                </a>
</div>
</div>
</aside>
<!-- Main Content Canvas -->
<main class="lg:ml-64 pt-24 pb-32 px-8 min-h-screen">
<div class="max-w-6xl mx-auto space-y-10">
<!-- Section 1: Red Flags Alert Banner -->
<section class="bg-error-container/30 border-l-4 border-error p-6 rounded-r-xl">
<div class="flex items-start gap-4">
<span class="material-symbols-outlined text-error text-3xl" style="font-variation-settings: 'FILL' 1;">warning</span>
<div class="space-y-2">
<h3 class="text-on-error-container font-bold headline-lg tracking-tight">Critical Red Flags Detected</h3>
<ul class="grid md:grid-cols-2 gap-x-12 gap-y-2">
<li class="flex items-center gap-2 text-on-error-container text-sm">
<span class="w-1.5 h-1.5 bg-error rounded-full"></span>
                                New onset tachycardia (&gt;110 bpm) consistent with systemic inflammatory response.
                            </li>
<li class="flex items-center gap-2 text-on-error-container text-sm">
<span class="w-1.5 h-1.5 bg-error rounded-full"></span>
                                Oxygen saturation drop to 89% on ambient air.
                            </li>
<li class="flex items-center gap-2 text-on-error-container text-sm">
<span class="w-1.5 h-1.5 bg-error rounded-full"></span>
                                Radiological evidence of consolidation in the right middle lobe.
                            </li>
</ul>
</div>
</div>
</section>
<div class="grid lg:grid-cols-12 gap-10 items-start">
<!-- Left Column: Summary & Diagnosis (70%) -->
<div class="lg:col-span-8 space-y-10">
<!-- Section 2: Clinical Summary -->
<section class="bg-surface-container-low p-8 rounded-xl">
<div class="flex justify-between items-center mb-6">
<h3 class="text-sm font-bold uppercase tracking-widest text-on-surface-variant">Clinical Summary</h3>
<span class="font-mono text-[10px] text-on-surface-variant">ID: 992-PX-402</span>
</div>
<p class="text-on-surface text-lg leading-relaxed font-medium">
                            Patient presents with a 3-day history of productive cough, pleuritic chest pain, and intermittent high-grade fevers. Clinical presentation and acute phase reactants suggest an infectious pulmonary process. Neural analysis identifies high-probability bacterial etiology requiring immediate intervention.
                        </p>
</section>
<!-- Section 3: Differential Diagnosis -->
<section class="space-y-6">
<h3 class="text-sm font-bold uppercase tracking-widest text-on-surface-variant">Differential Diagnosis</h3>
<div class="space-y-4">
<!-- Diagnosis Card 01 -->
<div class="bg-surface-container-low hover:bg-surface-container-high transition-colors rounded-xl overflow-hidden group">
<div class="p-6 flex items-center justify-between">
<div class="flex items-center gap-6">
<div class="font-mono text-2xl font-bold text-outline-variant">01</div>
<div class="radial-progress" style="--value: 87;">
<span class="text-[10px] font-bold text-on-tertiary-container">87%</span>
</div>
<div>
<h4 class="text-xl font-bold tracking-tight text-primary">Bacterial Pneumonia</h4>
<span class="font-mono text-[10px] bg-surface-container-highest px-2 py-0.5 rounded text-on-surface-variant">ICD-10: J15.9</span>
</div>
</div>
<button class="flex items-center gap-2 text-secondary font-bold text-xs uppercase tracking-widest">
                                        View Evidence
                                        <span class="material-symbols-outlined group-hover:translate-y-0.5 transition-transform">expand_more</span>
</button>
</div>
<div class="bg-white/50 px-16 py-6 space-y-4">
<div class="grid grid-cols-2 gap-4">
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-on-tertiary-container text-lg">check_circle</span>
<span class="text-sm text-on-surface">Leukocytosis (14.2k)</span>
</div>
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-on-tertiary-container text-lg">check_circle</span>
<span class="text-sm text-on-surface">Right Lobar Infiltrate</span>
</div>
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-error text-lg">cancel</span>
<span class="text-sm text-on-surface">Absence of typical viral prodrome</span>
</div>
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-on-tertiary-container text-lg">check_circle</span>
<span class="text-sm text-on-surface">Procalcitonin &gt;0.5 ng/mL</span>
</div>
</div>
</div>
</div>
<!-- Diagnosis Card 02 -->
<div class="bg-surface-container-low hover:bg-surface-container-high transition-colors rounded-xl overflow-hidden opacity-80">
<div class="p-6 flex items-center justify-between">
<div class="flex items-center gap-6">
<div class="font-mono text-2xl font-bold text-outline-variant">02</div>
<div class="radial-progress" style="--value: 12; --size: 3rem;">
<span class="text-[10px] font-bold text-on-surface-variant">12%</span>
</div>
<div>
<h4 class="text-xl font-bold tracking-tight text-primary">Pulmonary Embolism</h4>
<span class="font-mono text-[10px] bg-surface-container-highest px-2 py-0.5 rounded text-on-surface-variant">ICD-10: I26.99</span>
</div>
</div>
<button class="flex items-center gap-2 text-on-surface-variant font-bold text-xs uppercase tracking-widest">
                                        View Evidence
                                        <span class="material-symbols-outlined">expand_more</span>
</button>
</div>
</div>
</div>
</section>
</div>
<!-- Right Column: Next Steps & Trace (30%) -->
<div class="lg:col-span-4 space-y-10">
<!-- Section 4: Recommended Next Steps -->
<section class="bg-primary p-8 rounded-xl text-white">
<h3 class="text-[10px] font-bold uppercase tracking-widest text-primary-fixed-dim mb-6">Recommended Actions</h3>
<div class="space-y-4">
<div class="p-4 rounded-lg bg-white/5 border border-white/10 space-y-3">
<div class="flex justify-between items-start">
<span class="bg-secondary px-2 py-0.5 rounded-full text-[10px] font-bold uppercase">Imaging</span>
<span class="material-symbols-outlined text-on-primary-container">arrow_forward</span>
</div>
<h5 class="font-bold">Urgent CT Angiography</h5>
<p class="text-xs text-on-primary-container">Rule out vascular complications or secondary abscess formation.</p>
</div>
<div class="p-4 rounded-lg bg-white/5 border border-white/10 space-y-3">
<div class="flex justify-between items-start">
<span class="bg-on-tertiary-container px-2 py-0.5 rounded-full text-[10px] font-bold uppercase text-white">Lab Test</span>
<span class="material-symbols-outlined text-on-primary-container">arrow_forward</span>
</div>
<h5 class="font-bold">Blood Cultures x2</h5>
<p class="text-xs text-on-primary-container">Required prior to initiating broad-spectrum antibiotic regimen.</p>
</div>
</div>
</section>
<!-- Section 7: Agent Trace Viewer -->
<section class="space-y-6">
<h3 class="text-sm font-bold uppercase tracking-widest text-on-surface-variant">Neural Agent Trace</h3>
<div class="relative pl-8 space-y-8 before:absolute before:left-3 before:top-2 before:bottom-2 before:w-px before:bg-outline-variant/30">
<!-- Node 1 -->
<div class="relative">
<div class="absolute -left-[29px] top-0 w-4 h-4 bg-secondary rounded-full border-4 border-background"></div>
<div class="space-y-1">
<h6 class="text-xs font-bold text-primary">Vision Agent</h6>
<p class="text-[11px] text-on-surface-variant">Analyzed Chest X-Ray DICOM. Detected right lobe density.</p>
<span class="font-mono text-[9px] text-secondary">COMPLETE • 420ms</span>
</div>
</div>
<!-- Node 2 -->
<div class="relative">
<div class="absolute -left-[29px] top-0 w-4 h-4 bg-secondary rounded-full border-4 border-background"></div>
<div class="space-y-1">
<h6 class="text-xs font-bold text-primary">RAG Agent</h6>
<p class="text-[11px] text-on-surface-variant">Cross-referenced lab values with NEJM guidelines.</p>
<span class="font-mono text-[9px] text-secondary">COMPLETE • 890ms</span>
</div>
</div>
<!-- Node 3 -->
<div class="relative">
<div class="absolute -left-[29px] top-0 w-4 h-4 bg-on-tertiary-container rounded-full border-4 border-background"></div>
<div class="space-y-1">
<h6 class="text-xs font-bold text-primary">Report Agent</h6>
<p class="text-[11px] text-on-surface-variant">Synthesized clinical narrative and ICD-10 mapping.</p>
<span class="font-mono text-[9px] text-on-tertiary-container">COMPLETE • 120ms</span>
</div>
</div>
</div>
</section>
</div>
</div>
</div>
</main>
<!-- Sticky Bottom Export Bar -->
<footer class="fixed bottom-0 w-full bg-white/90 backdrop-blur-md border-t border-surface-variant z-50">
<div class="max-w-6xl mx-auto px-8 h-20 flex items-center justify-between">
<div class="flex items-center gap-6">
<div class="flex gap-2">
<button class="bg-surface-container-low hover:bg-surface-container-high text-primary px-4 py-2 rounded-full text-xs font-bold flex items-center gap-2 transition-all">
<span class="material-symbols-outlined text-sm">picture_as_pdf</span>
                        PDF
                    </button>
<button class="bg-surface-container-low hover:bg-surface-container-high text-primary px-4 py-2 rounded-full text-xs font-bold flex items-center gap-2 transition-all">
<span class="material-symbols-outlined text-sm">terminal</span>
                        JSON
                    </button>
<button class="bg-surface-container-low hover:bg-surface-container-high text-primary px-4 py-2 rounded-full text-xs font-bold flex items-center gap-2 transition-all">
<span class="material-symbols-outlined text-sm">article</span>
                        MD
                    </button>
</div>
</div>
<div class="flex items-center gap-8">
<div class="hidden xl:block max-w-sm text-right">
<p class="text-[9px] leading-tight text-on-surface-variant italic">
                        DISCLAIMER: AI-generated analysis. For clinical decision support only. Results must be verified by a board-certified medical professional prior to treatment execution.
                    </p>
</div>
<button class="bg-secondary text-white px-8 py-3 rounded-full text-sm font-bold tracking-tight hover:brightness-110 shadow-lg shadow-secondary/20 transition-all active:scale-95">
                    Approve &amp; Push to EHR
                </button>
</div>
</div>
</footer>
</body></html>

<!-- Patient Records Archive -->
<!DOCTYPE html>

<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Patient Records Archive | MediAgent</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&amp;family=JetBrains+Mono:wght@400;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    "secondary": "#0051d5",
                    "surface-container": "#eceef0",
                    "primary": "#000f22",
                    "on-background": "#191c1e",
                    "surface": "#f7f9fb",
                    "tertiary-fixed-dim": "#4edea3",
                    "tertiary": "#001209",
                    "on-primary-container": "#768dad",
                    "inverse-primary": "#b0c8eb",
                    "on-secondary-container": "#fefcff",
                    "tertiary-fixed": "#6ffbbe",
                    "outline-variant": "#c4c6ce",
                    "error": "#ba1a1a",
                    "secondary-fixed-dim": "#b4c5ff",
                    "outline": "#74777e",
                    "surface-container-high": "#e6e8ea",
                    "primary-container": "#0a2540",
                    "on-error-container": "#93000a",
                    "surface-container-highest": "#e0e3e5",
                    "on-secondary-fixed": "#00174b",
                    "on-primary": "#ffffff",
                    "surface-tint": "#49607e",
                    "surface-container-low": "#f2f4f6",
                    "secondary-fixed": "#dbe1ff",
                    "on-tertiary-container": "#009e6d",
                    "on-secondary": "#ffffff",
                    "on-primary-fixed-variant": "#314865",
                    "on-surface": "#191c1e",
                    "surface-variant": "#e0e3e5",
                    "on-primary-fixed": "#001c37",
                    "inverse-surface": "#2d3133",
                    "on-tertiary": "#ffffff",
                    "on-error": "#ffffff",
                    "on-surface-variant": "#43474d",
                    "surface-dim": "#d8dadc",
                    "secondary-container": "#316bf3",
                    "background": "#f7f9fb",
                    "surface-bright": "#f7f9fb",
                    "primary-fixed-dim": "#b0c8eb",
                    "tertiary-container": "#002a1a",
                    "on-tertiary-fixed": "#002113",
                    "primary-fixed": "#d2e4ff",
                    "inverse-on-surface": "#eff1f3",
                    "error-container": "#ffdad6",
                    "on-secondary-fixed-variant": "#003ea8",
                    "surface-container-lowest": "#ffffff",
                    "on-tertiary-fixed-variant": "#005236"
            },
            "borderRadius": {
                    "DEFAULT": "0.125rem",
                    "lg": "0.25rem",
                    "xl": "0.5rem",
                    "full": "0.75rem"
            },
            "fontFamily": {
                    "headline": ["Inter"],
                    "body": ["Inter"],
                    "label": ["Inter"],
                    "mono": ["JetBrains Mono"]
            }
          },
        }
      }
    </script>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            vertical-align: middle;
        }
        body { font-family: 'Inter', sans-serif; }
        .mono-text { font-family: 'JetBrains Mono', monospace; }
        .glass-overlay {
            background: rgba(247, 249, 251, 0.7);
            backdrop-filter: blur(24px);
        }
    </style>
</head>
<body class="bg-surface text-on-surface min-h-screen flex overflow-hidden">
<!-- SideNavBar Component -->
<aside class="bg-[#000f22] dark:bg-[#000f22] flex flex-col h-screen py-8 px-4 docked left-0 w-64 shrink-0 z-20">
<div class="mb-10 px-4">
<h1 class="text-lg font-black text-white">Clinical Sentinel</h1>
<p class="font-['JetBrains_Mono'] text-[10px] uppercase tracking-[0.2em] text-slate-500 mt-1">V3.2.0-Alpha</p>
</div>
<nav class="flex-1 space-y-2">
<a class="flex items-center gap-3 px-4 py-3 text-slate-500 font-medium font-['JetBrains_Mono'] text-xs uppercase tracking-widest hover:bg-white/10 hover:text-white transition-all duration-300" href="#">
<span class="material-symbols-outlined" data-icon="analytics">analytics</span>
<span>New Analysis</span>
</a>
<a class="flex items-center gap-3 px-4 py-3 text-[#0051d5] font-bold border-r-4 border-[#0051d5] bg-white/5 font-['JetBrains_Mono'] text-xs uppercase tracking-widest transition-all duration-300" href="#">
<span class="material-symbols-outlined" data-icon="folder_shared">folder_shared</span>
<span>Patient Records</span>
</a>
<a class="flex items-center gap-3 px-4 py-3 text-slate-500 font-medium font-['JetBrains_Mono'] text-xs uppercase tracking-widest hover:bg-white/10 hover:text-white transition-all duration-300" href="#">
<span class="material-symbols-outlined" data-icon="query_stats">query_stats</span>
<span>System Status</span>
</a>
</nav>
<div class="mt-auto pt-6 border-t border-white/5 space-y-2">
<button class="w-full bg-secondary text-on-secondary rounded-full py-3 px-4 mb-6 font-semibold text-sm flex items-center justify-center gap-2">
<span class="material-symbols-outlined text-sm" data-icon="add">add</span>
                Start New Case
            </button>
<a class="flex items-center gap-3 px-4 py-2 text-slate-500 font-medium font-['JetBrains_Mono'] text-xs uppercase tracking-widest hover:bg-white/10 hover:text-white transition-all duration-300" href="#">
<span class="material-symbols-outlined" data-icon="settings">settings</span>
<span>Settings</span>
</a>
<a class="flex items-center gap-3 px-4 py-2 text-slate-500 font-medium font-['JetBrains_Mono'] text-xs uppercase tracking-widest hover:bg-white/10 hover:text-white transition-all duration-300" href="#">
<span class="material-symbols-outlined" data-icon="help_outline">help_outline</span>
<span>Support</span>
</a>
</div>
</aside>
<div class="flex-1 flex flex-col min-w-0 overflow-hidden">
<!-- TopNavBar Component -->
<header class="bg-[#000f22] dark:bg-[#000f22] flex justify-between items-center w-full px-8 h-16 shrink-0 z-10">
<div class="flex items-center gap-8">
<span class="text-xl font-bold tracking-tighter text-white">MediAgent</span>
<nav class="hidden md:flex gap-6">
<a class="text-white border-b-2 border-[#0051d5] pb-1 font-['Inter'] font-semibold tracking-tight text-sm" href="#">Records</a>
<a class="text-slate-400 hover:text-white transition-colors duration-200 font-['Inter'] font-semibold tracking-tight text-sm" href="#">Dashboard</a>
<a class="text-slate-400 hover:text-white transition-colors duration-200 font-['Inter'] font-semibold tracking-tight text-sm" href="#">Network</a>
</nav>
</div>
<div class="flex items-center gap-6">
<div class="relative hidden lg:block">
<input class="bg-white/5 border-none text-white text-xs py-2 pl-4 pr-10 rounded-full w-48 focus:ring-1 focus:ring-secondary transition-all" placeholder="Quick find..." type="text"/>
<span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm" data-icon="search">search</span>
</div>
<div class="flex gap-4 text-slate-400">
<button class="hover:text-white transition-colors"><span class="material-symbols-outlined" data-icon="notifications">notifications</span></button>
<button class="hover:text-white transition-colors"><span class="material-symbols-outlined" data-icon="account_circle">account_circle</span></button>
</div>
</div>
</header>
<!-- Content Canvas -->
<main class="flex-1 overflow-y-auto p-8 lg:p-12 space-y-12">
<!-- Page Header & Filters -->
<section class="flex flex-col md:flex-row md:items-end justify-between gap-8">
<div class="space-y-2">
<h2 class="text-4xl font-extrabold tracking-tight text-primary">Patient Records Archive</h2>
<p class="text-on-surface-variant font-medium">Repository of verified AI clinical assessments and diagnostics.</p>
</div>
<div class="flex flex-wrap gap-3">
<button class="px-5 py-2 rounded-full bg-primary text-white text-sm font-semibold">All Records</button>
<button class="px-5 py-2 rounded-full bg-surface-container-high text-on-surface-variant text-sm font-semibold hover:bg-surface-container-highest transition-colors">Completed</button>
<button class="px-5 py-2 rounded-full bg-surface-container-high text-on-surface-variant text-sm font-semibold hover:bg-surface-container-highest transition-colors">Flagged</button>
<button class="w-10 h-10 rounded-full flex items-center justify-center bg-surface-container-high hover:bg-secondary hover:text-white transition-all"><span class="material-symbols-outlined text-lg" data-icon="filter_list">filter_list</span></button>
</div>
</section>
<!-- Search & Control Bar -->
<section class="bg-surface-container-low p-1 rounded-full flex items-center max-w-2xl">
<div class="flex-1 relative pl-6">
<span class="material-symbols-outlined absolute left-6 top-1/2 -translate-y-1/2 text-outline" data-icon="search">search</span>
<input class="w-full bg-transparent border-none py-4 pl-8 focus:ring-0 text-sm font-medium" placeholder="Search by Patient ID, Physician, or Clinical Code..." type="text"/>
</div>
<button class="bg-secondary text-white px-8 py-3 rounded-full text-sm font-bold shadow-lg shadow-secondary/20 mr-1">
                    EXECUTE SEARCH
                </button>
</section>
<!-- Table Section (Asymmetric Layout Approach) -->
<section class="grid grid-cols-1 gap-1">
<!-- Header row -->
<div class="grid grid-cols-12 gap-4 px-8 py-4 bg-transparent font-['JetBrains_Mono'] text-[10px] uppercase tracking-widest text-outline">
<div class="col-span-2">Patient ID</div>
<div class="col-span-2">Analysis Type</div>
<div class="col-span-2">Verification Date</div>
<div class="col-span-4">Diagnostic Summary</div>
<div class="col-span-2 text-right">Confidence Status</div>
</div>
<!-- Record Rows -->
<div class="space-y-4">
<!-- Row 1 -->
<div class="grid grid-cols-12 gap-4 items-center px-8 py-6 bg-surface-container-lowest rounded-xl hover:bg-white hover:scale-[1.005] transition-all duration-300 cursor-pointer group">
<div class="col-span-2 mono-text text-sm font-bold text-primary">#PX-9042-ALPHA</div>
<div class="col-span-2">
<span class="px-3 py-1 rounded-full bg-secondary/10 text-secondary text-[10px] font-bold uppercase tracking-wider">Vision Engine</span>
</div>
<div class="col-span-2 mono-text text-xs text-on-surface-variant">2023.10.12 / 14:22</div>
<div class="col-span-4 pr-8">
<p class="text-sm font-medium line-clamp-1">Possible early-stage malignant progression in thoracic scan. High resolution verification pending.</p>
</div>
<div class="col-span-2 flex items-center justify-end gap-3">
<span class="px-3 py-1 rounded-full bg-error-container text-on-error-container text-[10px] font-bold uppercase tracking-wider">Red Flag</span>
<button class="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"><span class="material-symbols-outlined text-sm" data-icon="chevron_right">chevron_right</span></button>
</div>
</div>
<!-- Row 2 -->
<div class="grid grid-cols-12 gap-4 items-center px-8 py-6 bg-surface-container-lowest rounded-xl hover:bg-white hover:scale-[1.005] transition-all duration-300 cursor-pointer group">
<div class="col-span-2 mono-text text-sm font-bold text-primary">#PX-8821-BETA</div>
<div class="col-span-2">
<span class="px-3 py-1 rounded-full bg-on-primary-container/10 text-on-primary-container text-[10px] font-bold uppercase tracking-wider">RAG / Clinical</span>
</div>
<div class="col-span-2 mono-text text-xs text-on-surface-variant">2023.10.12 / 11:05</div>
<div class="col-span-4 pr-8">
<p class="text-sm font-medium line-clamp-1">Comprehensive cross-referencing of laboratory vitals against historical baseline suggests stability.</p>
</div>
<div class="col-span-2 flex items-center justify-end gap-3">
<span class="px-3 py-1 rounded-full bg-[#e8f5e9] text-on-tertiary-container text-[10px] font-bold uppercase tracking-wider">High Confidence</span>
<button class="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"><span class="material-symbols-outlined text-sm" data-icon="chevron_right">chevron_right</span></button>
</div>
</div>
<!-- Row 3 -->
<div class="grid grid-cols-12 gap-4 items-center px-8 py-6 bg-surface-container-lowest rounded-xl hover:bg-white hover:scale-[1.005] transition-all duration-300 cursor-pointer group">
<div class="col-span-2 mono-text text-sm font-bold text-primary">#PX-0034-GAMMA</div>
<div class="col-span-2">
<span class="px-3 py-1 rounded-full bg-primary/5 text-primary text-[10px] font-bold uppercase tracking-wider">Full Assessment</span>
</div>
<div class="col-span-2 mono-text text-xs text-on-surface-variant">2023.10.11 / 18:40</div>
<div class="col-span-4 pr-8">
<p class="text-sm font-medium line-clamp-1">Ambiguous shadow in lumbar region; data noise level above 4%. Manual verification advised.</p>
</div>
<div class="col-span-2 flex items-center justify-end gap-3">
<span class="px-3 py-1 rounded-full bg-surface-container-highest text-on-surface-variant text-[10px] font-bold uppercase tracking-wider">Low Confidence</span>
<button class="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"><span class="material-symbols-outlined text-sm" data-icon="chevron_right">chevron_right</span></button>
</div>
</div>
<!-- Row 4 -->
<div class="grid grid-cols-12 gap-4 items-center px-8 py-6 bg-surface-container-lowest rounded-xl hover:bg-white hover:scale-[1.005] transition-all duration-300 cursor-pointer group">
<div class="col-span-2 mono-text text-sm font-bold text-primary">#PX-5112-ZETA</div>
<div class="col-span-2">
<span class="px-3 py-1 rounded-full bg-secondary/10 text-secondary text-[10px] font-bold uppercase tracking-wider">Vision Engine</span>
</div>
<div class="col-span-2 mono-text text-xs text-on-surface-variant">2023.10.11 / 16:15</div>
<div class="col-span-4 pr-8">
<p class="text-sm font-medium line-clamp-1">Fracture identification in radial distal region confirmed. Automatic splint recommendation generated.</p>
</div>
<div class="col-span-2 flex items-center justify-end gap-3">
<span class="px-3 py-1 rounded-full bg-[#e8f5e9] text-on-tertiary-container text-[10px] font-bold uppercase tracking-wider">High Confidence</span>
<button class="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"><span class="material-symbols-outlined text-sm" data-icon="chevron_right">chevron_right</span></button>
</div>
</div>
</div>
</section>
<!-- Editorial Stats Section -->
<section class="grid grid-cols-1 md:grid-cols-3 gap-8 pt-12">
<div class="space-y-4">
<p class="font-['JetBrains_Mono'] text-[10px] uppercase tracking-[0.2em] text-outline">Archival Volume</p>
<div class="text-5xl font-black text-primary tracking-tighter">14,208</div>
<p class="text-sm text-on-surface-variant leading-relaxed">Verified diagnostic records secured in the neural vault. 100% data integrity verified.</p>
</div>
<div class="space-y-4 border-l border-outline-variant/30 pl-8">
<p class="font-['JetBrains_Mono'] text-[10px] uppercase tracking-[0.2em] text-outline">Accuracy Mean</p>
<div class="text-5xl font-black text-secondary tracking-tighter">99.8<span class="text-2xl font-bold ml-1">%</span></div>
<p class="text-sm text-on-surface-variant leading-relaxed">System-wide confidence interval across all vision and RAG analysis modules.</p>
</div>
<div class="bg-primary text-white p-8 rounded-2xl relative overflow-hidden group">
<div class="relative z-10 space-y-4">
<p class="font-['JetBrains_Mono'] text-[10px] uppercase tracking-[0.2em] text-white/50">Need Assistance?</p>
<h4 class="text-xl font-bold leading-tight">Request specialized human-in-the-loop audit for flagged cases.</h4>
<button class="text-xs uppercase font-black tracking-widest text-secondary hover:text-white transition-colors">Contact Radiologist →</button>
</div>
<!-- Decorative Background Element -->
<div class="absolute -right-4 -bottom-4 w-32 h-32 bg-secondary/20 rounded-full blur-3xl group-hover:scale-150 transition-transform duration-700"></div>
</div>
</section>
</main>
</div>
<!-- Floating Global Action (Conditional Suppression applied: suppressed here as it's an archive page) -->
</body></html>

<!-- Design System -->
<!DOCTYPE html>

<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>MediAgent | Clinical Workspace Access</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    "secondary": "#0051d5",
                    "surface-container": "#eceef0",
                    "primary": "#000f22",
                    "on-background": "#191c1e",
                    "surface": "#f7f9fb",
                    "tertiary-fixed-dim": "#4edea3",
                    "tertiary": "#001209",
                    "on-primary-container": "#768dad",
                    "inverse-primary": "#b0c8eb",
                    "on-secondary-container": "#fefcff",
                    "tertiary-fixed": "#6ffbbe",
                    "outline-variant": "#c4c6ce",
                    "error": "#ba1a1a",
                    "secondary-fixed-dim": "#b4c5ff",
                    "outline": "#74777e",
                    "surface-container-high": "#e6e8ea",
                    "primary-container": "#0a2540",
                    "on-error-container": "#93000a",
                    "surface-container-highest": "#e0e3e5",
                    "on-secondary-fixed": "#00174b",
                    "on-primary": "#ffffff",
                    "surface-tint": "#49607e",
                    "surface-container-low": "#f2f4f6",
                    "secondary-fixed": "#dbe1ff",
                    "on-tertiary-container": "#009e6d",
                    "on-secondary": "#ffffff",
                    "on-primary-fixed-variant": "#314865",
                    "on-surface": "#191c1e",
                    "surface-variant": "#e0e3e5",
                    "on-primary-fixed": "#001c37",
                    "inverse-surface": "#2d3133",
                    "on-tertiary": "#ffffff",
                    "on-error": "#ffffff",
                    "on-surface-variant": "#43474d",
                    "surface-dim": "#d8dadc",
                    "secondary-container": "#316bf3",
                    "background": "#f7f9fb",
                    "surface-bright": "#f7f9fb",
                    "primary-fixed-dim": "#b0c8eb",
                    "tertiary-container": "#002a1a",
                    "on-tertiary-fixed": "#002113",
                    "primary-fixed": "#d2e4ff",
                    "inverse-on-surface": "#eff1f3",
                    "error-container": "#ffdad6",
                    "on-secondary-fixed-variant": "#003ea8",
                    "surface-container-lowest": "#ffffff",
                    "on-tertiary-fixed-variant": "#005236"
            },
            "borderRadius": {
                    "DEFAULT": "0.125rem",
                    "lg": "0.25rem",
                    "xl": "0.5rem",
                    "full": "0.75rem"
            },
            "fontFamily": {
                    "headline": ["Inter"],
                    "body": ["Inter"],
                    "label": ["Inter"],
                    "mono": ["JetBrains Mono"]
            }
          },
        },
      }
    </script>
<style>
      .material-symbols-outlined {
        font-variation-settings: 'FILL' 0, 'wght' 300, 'GRAD' 0, 'opsz' 24;
        vertical-align: middle;
      }
      .bg-pattern {
        background-color: #f7f9fb;
        background-image: radial-gradient(#0051d5 0.5px, transparent 0.5px);
        background-size: 32px 32px;
        opacity: 0.15;
      }
    </style>
</head>
<body class="bg-surface font-body text-on-surface antialiased overflow-hidden">
<!-- Background Layering -->
<div class="fixed inset-0 z-0">
<div class="absolute inset-0 bg-pattern"></div>
<div class="absolute inset-0 bg-gradient-to-tr from-primary/10 via-transparent to-secondary/5"></div>
<div class="absolute top-[-10%] right-[-5%] w-[40vw] h-[40vw] bg-secondary/5 rounded-full blur-[120px]"></div>
<div class="absolute bottom-[-10%] left-[-5%] w-[30vw] h-[30vw] bg-primary/10 rounded-full blur-[100px]"></div>
</div>
<main class="relative z-10 min-h-screen flex flex-col items-center justify-center p-6 md:p-12">
<div class="w-full max-w-[1100px] grid grid-cols-1 md:grid-cols-12 gap-0 overflow-hidden bg-surface-container-lowest/80 backdrop-blur-2xl rounded-xl shadow-2xl border border-outline-variant/10">
<!-- Left Branding Panel (Editorial / Asymmetric) -->
<div class="md:col-span-5 bg-primary p-10 md:p-16 flex flex-col justify-between text-white relative">
<!-- Branding Header -->
<div class="space-y-8">
<div class="flex items-center gap-3">
<div class="w-12 h-12 bg-secondary rounded-xl flex items-center justify-center shadow-lg shadow-secondary/20">
<span class="material-symbols-outlined text-white text-3xl" data-icon="clinical_notes">clinical_notes</span>
</div>
<h1 class="text-2xl font-black tracking-tighter text-white">MediAgent</h1>
</div>
<div class="pt-12">
<h2 class="text-4xl md:text-5xl font-extrabold tracking-tight leading-none mb-6">
                            Precision <br/>
<span class="text-secondary">Sentinel</span> AI
                        </h2>
<p class="text-on-primary-container text-lg font-light leading-relaxed max-w-xs">
                            Secure clinical intelligence designed for practitioners who demand absolute accuracy.
                        </p>
</div>
</div>
<!-- Status Metadata (Mono Style) -->
<div class="space-y-4">
<div class="inline-flex items-center gap-2 px-3 py-1 bg-white/5 rounded-full border border-white/10">
<span class="w-2 h-2 bg-tertiary-fixed-dim rounded-full"></span>
<span class="font-mono text-[10px] tracking-widest text-slate-400 uppercase">System Status: Optimal</span>
</div>
<div class="flex flex-col gap-1 font-mono text-[10px] text-slate-500">
<p>ID: NODE_SENTINEL_771</p>
<p>ENC: AES-256-GCM-HKDF</p>
</div>
</div>
<!-- Abstract Visual -->
<div class="absolute bottom-[-10%] right-[-10%] opacity-20 pointer-events-none">
<span class="material-symbols-outlined text-[240px] text-secondary" style="font-variation-settings: 'wght' 100;">neurology</span>
</div>
</div>
<!-- Right Login Form Panel -->
<div class="md:col-span-7 p-10 md:p-20 bg-surface-container-lowest">
<div class="max-w-md mx-auto h-full flex flex-col justify-center">
<div class="mb-12">
<h3 class="text-3xl font-bold tracking-tight text-primary mb-2">Clinical Workspace</h3>
<p class="text-on-surface-variant font-medium">Authentication required for protected health information access.</p>
</div>
<form class="space-y-6">
<div class="space-y-2">
<label class="font-mono text-[11px] uppercase tracking-widest text-outline font-semibold">Employee ID / Clinical Email</label>
<div class="relative group">
<span class="absolute left-4 top-1/2 -translate-y-1/2 material-symbols-outlined text-outline group-focus-within:text-secondary transition-colors" data-icon="badge">badge</span>
<input class="w-full pl-12 pr-4 py-4 bg-surface-container-highest rounded-xl border-none focus:ring-0 focus:bg-surface-container-lowest transition-all duration-300 placeholder:text-outline-variant font-mono text-sm" placeholder="EMP-4429-X" type="text"/>
<div class="absolute bottom-0 left-0 h-[2px] w-0 bg-secondary transition-all duration-500 group-focus-within:w-full"></div>
</div>
</div>
<div class="space-y-2">
<div class="flex justify-between items-center">
<label class="font-mono text-[11px] uppercase tracking-widest text-outline font-semibold">Security Credential</label>
<a class="font-mono text-[10px] uppercase tracking-widest text-secondary font-bold hover:underline" href="#">Forgot Access?</a>
</div>
<div class="relative group">
<span class="absolute left-4 top-1/2 -translate-y-1/2 material-symbols-outlined text-outline group-focus-within:text-secondary transition-colors" data-icon="lock_open">lock_open</span>
<input class="w-full pl-12 pr-4 py-4 bg-surface-container-highest rounded-xl border-none focus:ring-0 focus:bg-surface-container-lowest transition-all duration-300 placeholder:text-outline-variant" placeholder="••••••••••••" type="password"/>
<div class="absolute bottom-0 left-0 h-[2px] w-0 bg-secondary transition-all duration-500 group-focus-within:w-full"></div>
</div>
</div>
<div class="flex items-center gap-2 pt-2">
<input class="w-4 h-4 rounded-sm border-outline-variant text-secondary focus:ring-secondary/20" id="remember" type="checkbox"/>
<label class="text-sm text-on-surface-variant font-medium" for="remember">Extend session (24h Clinical Shift)</label>
</div>
<button class="w-full group relative overflow-hidden bg-secondary text-white font-bold py-5 px-6 rounded-full shadow-xl shadow-secondary/30 transition-all hover:translate-y-[-2px] active:translate-y-0 active:shadow-none" type="submit">
<span class="relative z-10 flex items-center justify-center gap-2 tracking-tight text-lg">
                                Access Clinical Workspace
                                <span class="material-symbols-outlined text-xl transition-transform group-hover:translate-x-1" data-icon="arrow_forward">arrow_forward</span>
</span>
<div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/10 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
</button>
</form>
<!-- Trust Footer -->
<div class="mt-16 pt-8 border-t border-outline-variant/10">
<div class="flex flex-wrap items-center gap-6">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-tertiary-fixed-dim text-lg" data-icon="verified_user" style="font-variation-settings: 'FILL' 1;">verified_user</span>
<span class="font-mono text-[10px] uppercase tracking-wider text-outline">End-to-End Encrypted</span>
</div>
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-on-error-container text-lg" data-icon="policy" style="font-variation-settings: 'FILL' 1;">policy</span>
<span class="font-mono text-[10px] uppercase tracking-wider text-outline">For Clinical Use Only</span>
</div>
</div>
</div>
</div>
</div>
</div>
<!-- Footer Help -->
<footer class="mt-12 text-center">
<p class="text-sm text-outline font-medium">
                Need technical support? 
                <a class="text-secondary hover:underline ml-1" href="#">Contact Hospital IT</a>
<span class="mx-2 opacity-30">|</span>
<span class="font-mono text-[11px] opacity-60">Build V3.2.0-Alpha</span>
</p>
</footer>
</main>
<!-- Visual Polish Overlay -->
<div class="fixed top-0 left-0 w-full h-1 bg-gradient-to-r from-primary via-secondary to-tertiary-fixed-dim z-50"></div>
</body></html>

<!-- Clinical Workspace Login -->
# MediAgent UI/UX Refinement Plan (Portfolio Enhancement)

## 1. Goal
Elevate the MediAgent UI from a standard "form-to-result" flow to a "Transparent Agentic Workflow" that showcases the underlying LangGraph architecture and RAG complexity.

## 2. Proposed Additional Screens/Features

### A. Agentic Trace Explorer (Deep Dive)
- **Purpose:** Visualize the "brain" of the application.
- **Key Features:** 
  - Node-by-node input/output logs.
  - Confidence scoring per agent.
  - Latency and token usage metrics.
  - Raw JSON toggle for developers.

### B. Lab Report "Data Lens" View
- **Purpose:** Bridge the gap between the PDF upload and the Clinical Summary.
- **Key Features:**
  - Side-by-side view: PDF original vs. Extracted Entities.
  - Highlighted medical terms (e.g., "Hemoglobin", "WBC").
  - Verification checkmarks (User can confirm AI-extracted values).

### C. Knowledge Context Modal
- **Purpose:** Explain the "R" in RAG.
- **Key Features:**
  - Snippets from PubMed abstracts.
  - Similarity scores (how relevant was this document?).
  - Direct links to NCBI for verification.

## 3. UI/UX Refinement Focus
- **Monospace Typography:** Increase use of JetBrains Mono for "System Logs" to reinforce the AI/ML nature.
- **Micro-interactions:** Add loading states that describe *which* agent is currently thinking.
- **Trust Indicators:** Clearer mapping between findings and citations.


<!-- MediAgent UI Refinement Plan -->
# PRD.md — MediAgent Product Requirements Document

**Version:** 1.0  
**Author:** Hussain (VIT Mumbai, CE — AI/ML Specialization)  
**Last Updated:** 2025  
**Status:** Ready for Development

---

## 1. Product Overview

### 1.1 Problem Statement

Healthcare in India and globally faces a critical gap: **diagnostic support is inaccessible at the point of first contact.** Rural hospitals are understaffed, general practitioners lack access to specialist knowledge, and patients with complex multi-modal symptoms (lab reports + imaging + history) receive delayed or missed diagnoses.

Existing tools either:
- Require expensive proprietary software (Epic, IBM Watson Health)
- Are single-modal (only images OR only text)
- Are not AI-agent driven — they're static, rule-based decision trees

### 1.2 Solution

**MediAgent** is a fully open-source, multimodal clinical decision support system powered by a 3-agent LangGraph pipeline. It accepts:
- Medical images (X-rays, skin lesions, retinal scans)
- Lab report PDFs
- Patient symptom descriptions (text or voice)

And returns:
- Ranked differential diagnoses with confidence scores
- ICD-10 coded conditions
- Red-flag alerts (urgent referral triggers)
- Evidence-backed reasoning with source citations
- Actionable next steps

### 1.3 Target Users

| User | Use Case |
|---|---|
| Medical students | Study aid, case-based learning |
| Junior doctors / interns | Second-opinion support |
| Patients (health-literate) | Understanding their own reports |
| Researchers | Benchmarking clinical NLP |
| Recruiters / evaluators | Assess AI/ML engineering capability |

### 1.4 Non-Goals

- MediAgent is **NOT a replacement for a licensed physician**
- MediAgent does **NOT store or persist patient data**
- MediAgent does **NOT provide prescription recommendations**
- MediAgent is **NOT HIPAA-certified** (educational/research use only)

---

## 2. Core Features

### Feature 1 — Multimodal Input Intake
**Priority:** P0 (Must Have)

The system must accept three simultaneous input modalities:

| Input Type | Accepted Formats | Processing |
|---|---|---|
| Medical Image | JPG, PNG, DICOM (via conversion) | LLaVA vision model |
| Lab Report | PDF, scanned PDF | PyMuPDF + OCR fallback |
| Symptoms | Text field OR voice recording | Whisper (voice) |

**Acceptance Criteria:**
- Image upload with preview before submission
- PDF text extraction with visible preview of extracted text
- Voice recording with real-time waveform and transcription display
- All three inputs optional but at least one required

---

### Feature 2 — Vision Analysis Agent
**Priority:** P0 (Must Have)

A dedicated LangGraph node that processes medical images using LLaVA 1.6.

**Inputs:** Raw image file  
**Outputs:**
```json
{
  "image_type": "chest_xray | skin_lesion | retinal_scan | lab_slide | unknown",
  "findings": ["bilateral infiltrates in lower lobes", "..."],
  "anomalies": ["opacity in right lower lobe"],
  "severity_hint": "mild | moderate | severe | normal",
  "confidence": 0.82
}
```

**Acceptance Criteria:**
- Identifies image type automatically
- Returns structured JSON (not free text)
- Gracefully handles non-medical images with a warning
- Runs locally via Ollama (no external API call)

---

### Feature 3 — RAG Knowledge Retrieval Agent
**Priority:** P0 (Must Have)

A LangGraph node that retrieves relevant medical knowledge from:
1. **ChromaDB** (pre-ingested MedQA + medical guidelines)
2. **PubMed API** (live retrieval via NCBI E-utilities)

**Inputs:** Patient symptoms + Vision Agent findings  
**Outputs:**
```json
{
  "relevant_conditions": ["Pneumonia", "COVID-19", "Pulmonary Edema"],
  "supporting_evidence": ["Source excerpt 1", "Source excerpt 2"],
  "sources": [
    {"title": "...", "pmid": "...", "url": "..."}
  ],
  "retrieval_count": 5
}
```

**Acceptance Criteria:**
- Returns top-5 relevant context chunks per query
- Cites sources with PMID links
- Falls back to ChromaDB if PubMed API is unavailable
- Embedding model: PubMedBERT

---

### Feature 4 — Clinical Report Agent
**Priority:** P0 (Must Have)

The final synthesis LangGraph node that combines Vision + RAG outputs into a structured clinical summary.

**Output Schema:**
```json
{
  "patient_summary": "35-year-old presenting with...",
  "differential_diagnosis": [
    {
      "rank": 1,
      "condition": "Community-Acquired Pneumonia",
      "icd_10_code": "J18.9",
      "confidence_score": 0.87,
      "supporting_findings": ["bilateral infiltrates", "elevated WBC"],
      "against_findings": []
    }
  ],
  "red_flags": [
    "SpO2 drop mentioned — urgent referral recommended"
  ],
  "recommended_next_steps": [
    "CBC with differential",
    "Sputum culture",
    "Pulmonologist referral"
  ],
  "estimated_urgency": "high | medium | low",
  "disclaimer": "This output is generated by an AI system for educational and research purposes only. It must not be used as a substitute for professional medical advice, diagnosis, or treatment."
}
```

**Acceptance Criteria:**
- Differential diagnosis ranked by confidence score descending
- ICD-10 code present for every condition
- Red flags highlighted separately
- Disclaimer always present, non-removable
- Response time < 30 seconds on CPU

---

### Feature 5 — Voice Input (Whisper Integration)
**Priority:** P1 (Should Have)

Allow patients/doctors to describe symptoms verbally.

**Acceptance Criteria:**
- Record via browser microphone
- Transcription via local Whisper (`base` model)
- Editable transcription before submission
- Supports English (primary) and Hindi (stretch goal)

---

### Feature 6 — Agent Trace Viewer (LangSmith)
**Priority:** P1 (Should Have)

Developer-facing trace panel showing the full LangGraph execution trace.

**Acceptance Criteria:**
- Each agent node's input/output visible
- Token usage per node
- Latency per node
- Accessible via LangSmith dashboard link embedded in UI

---

### Feature 7 — Report Export
**Priority:** P2 (Nice to Have)

Export the final clinical report as:
- PDF (formatted with PyMuPDF)
- Markdown
- JSON (raw)

---

### Feature 8 — Evaluation Dashboard
**Priority:** P2 (Nice to Have)

Internal page showing benchmark results:
- RAG retrieval accuracy on MedQA test set
- Vision Agent classification accuracy on HAM10000
- End-to-end accuracy on MedMCQA

---

## 3. System Architecture

### 3.1 Component Diagram

```
┌─────────────────────────────────────────────┐
│               React Frontend                 │
│  (Input Panel | Results Panel | Trace View) │
└─────────────────┬───────────────────────────┘
                  │ HTTP (REST)
                  ▼
┌─────────────────────────────────────────────┐
│              FastAPI Backend                 │
│  POST /api/analyze                           │
│  GET  /api/health                            │
│  GET  /api/models/status                    │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│         LangGraph Orchestrator               │
│                                             │
│  START → Vision Agent → RAG Agent           │
│              └──────────► Report Agent → END│
└─────────────────┬───────────────────────────┘
                  │
      ┌───────────┼───────────┐
      ▼           ▼           ▼
┌──────────┐ ┌────────┐ ┌──────────┐
│  Ollama  │ │Chroma  │ │ PubMed   │
│ (LLaVA + │ │  DB    │ │   API    │
│  LLaMA3) │ │        │ │  (NCBI)  │
└──────────┘ └────────┘ └──────────┘
```

### 3.2 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/analyze` | Main analysis endpoint — accepts multipart form data |
| GET | `/api/health` | System health check (Ollama status, ChromaDB status) |
| GET | `/api/models/status` | Check which models are loaded |
| POST | `/api/transcribe` | Standalone voice transcription |
| GET | `/api/export/{session_id}` | Export report as PDF/MD/JSON |

### 3.3 Data Flow

```
1. User submits form (image + PDF + symptoms/voice)
2. FastAPI receives multipart request
3. Files saved to temp directory (/tmp/mediagent/{session_id}/)
4. LangGraph Orchestrator initialized with state
5. Vision Agent processes image → returns findings JSON
6. RAG Agent retrieves context using symptoms + findings
7. Report Agent synthesizes final clinical report
8. Response returned to frontend as JSON
9. Temp files deleted
10. Frontend renders structured report
```

---

## 4. Technical Requirements

### 4.1 Backend Dependencies

```
# requirements.txt
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
langchain>=0.2.0
langchain-community>=0.2.0
langgraph>=0.1.0
langchain-ollama>=0.1.0
chromadb>=0.5.0
sentence-transformers>=3.0.0
pymupdf>=1.24.0
openai-whisper>=20231117
pytesseract>=0.3.10
pillow>=10.0.0
pydantic>=2.0.0
python-multipart>=0.0.9
httpx>=0.27.0
python-dotenv>=1.0.0
langsmith>=0.1.0
```

### 4.2 System Requirements

| Component | Minimum | Recommended |
|---|---|---|
| RAM | 8 GB | 16 GB |
| Storage | 20 GB | 50 GB |
| GPU | None (CPU mode) | NVIDIA 8GB VRAM |
| Python | 3.11+ | 3.11+ |
| Node.js | 18+ | 20+ |
| Ollama | Latest | Latest |

### 4.3 Models Required

```bash
ollama pull llama3.1:8b          # 4.7 GB — Report Agent
ollama pull llava:13b            # 8.0 GB — Vision Agent (use llava:7b for low RAM)
```

---

## 5. User Stories

### Epic 1 — Core Analysis

- **US-001:** As a medical student, I want to upload a chest X-ray and get a differential diagnosis so that I can learn about radiological findings.
- **US-002:** As a junior doctor, I want to upload a lab report PDF and describe patient symptoms to get ranked diagnoses so that I have a second-opinion reference.
- **US-003:** As a patient, I want to describe my symptoms by voice so I don't have to type long descriptions.

### Epic 2 — Results & Trust

- **US-004:** As a user, I want to see the sources and evidence behind every diagnosis so I know the AI is not hallucinating.
- **US-005:** As a developer, I want to see the full LangGraph trace so I can debug and improve the agents.
- **US-006:** As a user, I want to see red-flag warnings prominently so I know when to seek urgent care.

### Epic 3 — Export & Sharing

- **US-007:** As a user, I want to export the report as a PDF so I can share it with my doctor.

---

## 6. UI/UX Requirements

### 6.1 Pages

| Page | Route | Description |
|---|---|---|
| Home / Input | `/` | Split panel: input form + live preview |
| Results | `/results` | Structured report with tabs |
| History | `/history` | Past sessions (in-memory, no persistence) |
| System Status | `/status` | Model health, API status |

### 6.2 Design Principles

- **Medical-grade aesthetic:** Clean whites, deep blues, minimal color
- **Information hierarchy:** Red flags > Diagnoses > Evidence > Next Steps
- **Progressive disclosure:** Summary first, expandable detail cards
- **Mobile-responsive:** Doctors use phones and tablets
- **Dark mode support:** For clinical environments

### 6.3 Key UI Components

- Image drag-and-drop zone with DICOM preview
- PDF upload with extracted text preview sidebar
- Voice recorder with animated waveform
- Confidence score radial progress indicators
- Expandable diagnosis cards with ICD-10 badges
- Red flag alert banners (high contrast)
- Source citation chips with PubMed links
- LangGraph trace timeline (collapsible)

---

## 7. Milestones

| Phase | Description | Deliverable |
|---|---|---|
| Phase 0 | Repo setup, Ollama + ChromaDB scaffolding | Running `main.py` with health endpoint |
| Phase 1 | Vision Agent + RAG Agent working individually | Unit tests passing for both agents |
| Phase 2 | LangGraph orchestration wiring all 3 agents | Full pipeline `/api/analyze` returning JSON |
| Phase 3 | FastAPI complete + Whisper integration | All API endpoints live |
| Phase 4 | React frontend (Stitch) integrated | End-to-end demo working |
| Phase 5 | Evaluation, README, LangSmith tracing | Portfolio-ready with benchmarks |

---

## 8. Out of Scope (v1.0)

- EHR (Electronic Health Record) integration
- Multi-language support beyond English
- Mobile native app
- Real-time streaming responses
- Authentication / user accounts
- HIPAA compliance
- DICOM native support (use PNG conversion for now)


<!-- PRD.md -->
# CLAUDE.md — MediAgent Project Intelligence

## Project Identity

**Project Name:** MediAgent — Multimodal Clinical Decision Support Agent  
**Type:** AI/ML Specialization Portfolio Project (3rd Year — Vidyalankar Institute of Technology)  
**Domain:** Healthcare / Medical AI  
**Stack:** Python · LangGraph · LangChain · FastAPI · ChromaDB · LLaVA · BioBERT · Whisper · React  
**Goal:** A multimodal, multi-agent clinical decision support system that takes patient images, lab reports (PDFs), and symptom descriptions (text/voice) and returns structured differential diagnoses with confidence scores and red-flag alerts.

---

## Architecture Overview

```
User Input (Image + PDF + Text/Voice)
        │
        ▼
  FastAPI Gateway
        │
        ▼
  LangGraph Orchestrator  ◄──────────────────────────────────┐
        │                                                      │
   ┌────┴──────────────────────────────────────┐              │
   │              Agent Pipeline               │              │
   │                                           │              │
   │  ┌──────────────┐  ┌──────────────────┐  │              │
   │  │ Vision Agent │  │   RAG Agent      │  │              │
   │  │ (LLaVA /     │  │ (BioBERT +       │  │              │
   │  │  BioViL-T)   │  │  ChromaDB +      │  │              │
   │  │              │  │  PubMed/MedQA)   │  │              │
   │  └──────┬───────┘  └──────┬───────────┘  │              │
   │         │                 │               │              │
   │         └────────┬────────┘               │              │
   │                  │                        │              │
   │         ┌────────▼─────────┐             │              │
   │         │  Report Agent    │             │              │
   │         │ (Clinical        │             │              │
   │         │  Summarizer)     │             │              │
   │         └────────┬─────────┘             │              │
   └──────────────────┼────────────────────────┘              │
                      │                                        │
                      ▼                                        │
              Structured Output ───────────────────────────────┘
              (JSON + Markdown)
                      │
                      ▼
              React Frontend (Google Stitch)
```

---

## Repository Structure

```
mediagent/
├── CLAUDE.md               ← This file
├── PRD.md                  ← Product Requirements Document
├── TODO.md                 ← Phased task tracker
├── PROMPTS.md              ← LLM prompt templates
├── STITCH.md               ← Google Stitch frontend prompt
│
├── backend/
│   ├── main.py             ← FastAPI entry point
│   ├── config.py           ← Env vars, model paths, settings
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py ← LangGraph state machine
│   │   ├── vision_agent.py ← Image analysis (LLaVA)
│   │   ├── rag_agent.py    ← Medical knowledge retrieval
│   │   └── report_agent.py ← Final clinical summary
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── pdf_parser.py   ← Lab report PDF extraction
│   │   ├── voice_input.py  ← Whisper transcription
│   │   ├── pubmed_tool.py  ← PubMed API tool
│   │   └── image_loader.py ← Image preprocessing
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embedder.py     ← BioBERT embeddings
│   │   ├── vectorstore.py  ← ChromaDB CRUD
│   │   └── ingest.py       ← Dataset ingestion scripts
│   ├── models/
│   │   └── schemas.py      ← Pydantic models
│   └── utils/
│       ├── logger.py
│       └── helpers.py
│
├── frontend/               ← React app (Google Stitch generated)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   └── package.json
│
├── data/
│   ├── raw/                ← Raw datasets (gitignored)
│   └── processed/          ← Chunked + embedded docs
│
├── scripts/
│   ├── ingest_pubmed.py
│   ├── ingest_medqa.py
│   └── setup_chromadb.py
│
├── tests/
│   ├── test_vision_agent.py
│   ├── test_rag_agent.py
│   └── test_api.py
│
├── .env.example
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## Tech Stack & Model Choices

| Layer | Technology | Why |
|---|---|---|
| Orchestration | LangGraph | Stateful multi-agent graph, perfect for sequential + parallel agent flows |
| LLM Backend | LLaMA 3.1 8B via Ollama | Fully open source, runs locally, no API cost |
| Vision Model | LLaVA 1.6 (13B) or BioViL-T | Multimodal image+text understanding |
| Embeddings | BioBERT / PubMedBERT | Domain-specific medical embeddings |
| Vector Store | ChromaDB | Lightweight, local, open source |
| PDF Parsing | PyMuPDF (fitz) | Fast, accurate text+table extraction |
| Voice | OpenAI Whisper (local) | Open source speech-to-text |
| API Layer | FastAPI | Async, fast, type-safe |
| Frontend | React + Tailwind (Stitch) | Clean SPA, component-driven |
| Tracing | LangSmith | Agent trace visualization |
| Containerization | Docker + Docker Compose | Reproducible dev environment |

---

## Agent Definitions

### 1. Vision Agent (`vision_agent.py`)
- **Input:** Medical image (X-ray, skin lesion, eye fundus, etc.)
- **Model:** LLaVA 1.6 via Ollama
- **Output:** Structured JSON with `{findings: [], anomalies: [], image_type: "", confidence: float}`
- **Prompt:** See `PROMPTS.md → VISION_AGENT_PROMPT`

### 2. RAG Agent (`rag_agent.py`)
- **Input:** Patient symptoms (text) + Vision Agent findings
- **Tools:** ChromaDB retriever, PubMed API search tool
- **Knowledge Base:** MedQA chunks + PubMed abstracts (ingested at setup)
- **Output:** `{relevant_conditions: [], supporting_evidence: [], sources: []}`
- **Prompt:** See `PROMPTS.md → RAG_AGENT_PROMPT`

### 3. Report Agent (`report_agent.py`)
- **Input:** Outputs from Vision Agent + RAG Agent
- **Model:** LLaMA 3.1 8B via Ollama
- **Output:** Final structured clinical report JSON
- **Schema:**
```json
{
  "patient_summary": "...",
  "differential_diagnosis": [
    {"condition": "...", "confidence": 0.85, "icd_code": "..."},
  ],
  "red_flags": ["..."],
  "recommended_next_steps": ["..."],
  "disclaimer": "For clinical review only. Not a substitute for professional diagnosis."
}
```
- **Prompt:** See `PROMPTS.md → REPORT_AGENT_PROMPT`

---

## LangGraph State Schema

```python
from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage

class MediAgentState(TypedDict):
    # Inputs
    patient_symptoms: str
    image_path: Optional[str]
    pdf_path: Optional[str]
    voice_transcript: Optional[str]

    # Agent outputs
    vision_findings: Optional[dict]
    rag_context: Optional[dict]
    final_report: Optional[dict]

    # Metadata
    messages: List[BaseMessage]
    current_agent: str
    error: Optional[str]
```

---

## Environment Variables

```env
# .env.example
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
VISION_MODEL=llava:13b
CHROMADB_PATH=./data/chromadb
PUBMED_API_KEY=your_pubmed_api_key
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=mediagent
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000
```

---

## Key Development Rules

1. **All models run locally via Ollama** — no OpenAI calls in production code.
2. **Every agent returns a typed Pydantic schema** — no raw string outputs.
3. **LangGraph state is immutable** — agents return updated state dicts, never mutate.
4. **FastAPI endpoints are async** — use `async def` everywhere.
5. **Medical disclaimer is mandatory** on every report output.
6. **No patient data is persisted** — all uploads are temp files, deleted after processing.
7. **Whisper runs locally** — `whisper.load_model("base")` unless GPU available.
8. **ChromaDB collections:**
   - `medqa_chunks` — MedQA dataset embeddings
   - `pubmed_abstracts` — PubMed abstract embeddings
   - `medical_guidelines` — WHO/CDC guidelines

---

## Datasets & Knowledge Sources (All Open Source)

| Dataset | Source | Use |
|---|---|---|
| MedQA (USMLE) | HuggingFace `bigbio/med_qa` | RAG knowledge base |
| PubMed Abstracts | NCBI E-utilities API | Live tool retrieval |
| MedMCQA | HuggingFace `medmcqa` | Evaluation |
| MIMIC-CXR (if available) | PhysioNet | X-ray vision eval |
| Skin HAM10000 | Kaggle / HuggingFace | Skin lesion testing |

---

## Running the Project

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/mediagent
cd mediagent
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Pull models via Ollama
ollama pull llama3.1:8b
ollama pull llava:13b

# 3. Ingest knowledge base
python scripts/ingest_medqa.py
python scripts/ingest_pubmed.py

# 4. Start backend
uvicorn backend.main:app --reload --port 8000

# 5. Start frontend (separate terminal)
cd frontend && npm install && npm run dev
```

---

## Common Pitfalls to Avoid

- **LLaVA hallucinations on non-medical images** — always validate `image_type` before proceeding.
- **ChromaDB cold start** — run ingestion scripts before first query.
- **Ollama RAM usage** — LLaVA 13B needs ~16GB RAM; use `llava:7b` for lower spec machines.
- **PDF parsing edge cases** — scanned PDFs won't parse with PyMuPDF; add OCR fallback with `pytesseract`.
- **LangGraph cycles** — avoid unconditional loops; always add termination conditions.

---

## Evaluation Metrics

| Agent | Metric | Target |
|---|---|---|
| Vision Agent | Precision on image classification | > 75% |
| RAG Agent | Retrieval MRR@5 on MedQA | > 0.65 |
| Full Pipeline | End-to-end answer accuracy on MedMCQA | > 60% |
| Latency | Total pipeline response time | < 30s |

---

## Resume-Worthy Talking Points

- "Designed a stateful 3-agent LangGraph pipeline with parallel vision and RAG sub-graphs"
- "Built domain-specific RAG over 200K+ PubMed abstracts using PubMedBERT embeddings"
- "Integrated LLaVA 1.6 for multimodal medical image analysis within an agentic workflow"
- "Achieved end-to-end inference with zero external API calls using Ollama local inference"
- "Implemented structured clinical output schema with ICD-10 code mapping and confidence scoring"


<!-- CLAUDE.md -->
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
