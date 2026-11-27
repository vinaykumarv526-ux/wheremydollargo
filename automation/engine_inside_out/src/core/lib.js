// 2D Flat Architectural Explainer Engine - Visual Library
export const W = 1080, H = 1920, FPS = 30;
export let ctx = null;
export function setCtx(c) { ctx = c; }

// Signature Palette from System Specification
export const C = {
  bg: '#F4F1EA',          // Background Cream (Real-world / daytime scenes)
  navy: '#0E1A2B',        // Blueprint Deep Navy (Internal cutaways & technical X-rays)
  navyDark: '#0F172A',    // Deep slate navy
  navyGrid: '#1E293B',    // Grid lines for navy background
  ink: '#1A1A1E',         // Technical Ink (Outlines, borders, text strokes)
  cyan: '#38BDF8',        // Technical Cyan (Flow paths, vectors, blueprints)
  cyanLight: '#BAE6FD',   // Pale cyan vector tint
  yellow: '#FFD43B',      // Attention Yellow (Keyword highlights, primary tags)
  red: '#EF4444',         // Hazard Red (Failure warnings, stress concentrations, Red X)
  green: '#10B981',       // Safety Green (Auto-correction, stability, passing checks)
  white: '#FFFFFF',
  gray: '#64748B',
  grayLight: '#E2E8F0',
  gridCream: '#E6E2D8',   // Grid lines on cream background
};

// Math Utilities
export const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
export const lerp = (a, b, t) => a + (b - a) * t;
export const seg = (t, a, b) => clamp((t - a) / ((b - a) || 1e-6));
export const eo = (t) => 1 - Math.pow(1 - t, 3);
export const eio = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
export const eob = (t) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };
export const rnd = (i) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
export const TAU = Math.PI * 2;

// Drawing Primitives
export function rr(x, y, w, h, r = 24) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); }
export function circle(x, y, r, fill, stroke = null, sw = 4) {
  ctx.beginPath(); ctx.arc(x, y, r, 0, TAU);
  if (fill) { ctx.fillStyle = fill; ctx.fill(); }
  if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = sw; ctx.stroke(); }
}
export function ell(x, y, rx, ry, fill, rot = 0, stroke = null, sw = 4) {
  ctx.beginPath(); ctx.ellipse(x, y, rx, ry, rot, 0, TAU);
  if (fill) { ctx.fillStyle = fill; ctx.fill(); }
  if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = sw; ctx.stroke(); }
}
export function line(pts, color, w = 6, dashed = false) {
  if (pts.length < 2) return;
  ctx.save();
  ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
  for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i][0], pts[i][1]);
  ctx.strokeStyle = color; ctx.lineWidth = w; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  if (dashed) ctx.setLineDash(typeof dashed === 'object' ? dashed : [12, 10]);
  ctx.stroke();
  ctx.restore();
}
export function fillAll(color) { ctx.fillStyle = color; ctx.fillRect(-300, -300, W + 600, H + 600); }

// Technical Background Grid
export function drawGrid(isNavy = false, step = 80) {
  ctx.save();
  ctx.strokeStyle = isNavy ? C.navyGrid : C.gridCream;
  ctx.lineWidth = 2;
  for (let x = -200; x <= W + 200; x += step) {
    ctx.beginPath(); ctx.moveTo(x, -200); ctx.lineTo(x, H + 200); ctx.stroke();
  }
  for (let y = -200; y <= H + 200; y += step) {
    ctx.beginPath(); ctx.moveTo(-200, y); ctx.lineTo(W + 200, y); ctx.stroke();
  }
  ctx.restore();
}

// Technical Blueprint Outer Border Frame
export function blueprintBox(x, y, w, h, title = '', code = 'SEC-04') {
  ctx.save();
  ctx.translate(x, y);
  
  // Outer blueprint container
  rr(-w / 2, -h / 2, w, h, 28);
  ctx.fillStyle = C.navy; ctx.fill();
  ctx.strokeStyle = C.cyan; ctx.lineWidth = 6; ctx.stroke();
  
  // Dashed inner caliper line
  rr(-w / 2 + 18, -h / 2 + 18, w - 36, h - 36, 16);
  ctx.strokeStyle = C.cyan; ctx.lineWidth = 2;
  ctx.setLineDash([8, 8]); ctx.stroke(); ctx.setLineDash([]);
  
  // Technical Corner Marks
  const cs = 36;
  [[-w/2, -h/2], [w/2, -h/2], [-w/2, h/2], [w/2, h/2]].forEach(([cx, cy]) => {
    ctx.strokeStyle = C.yellow; ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(cx + (cx < 0 ? 0 : -cs), cy); ctx.lineTo(cx, cy); ctx.lineTo(cx, cy + (cy < 0 ? cs : -cs));
    ctx.stroke();
  });
  
  // Blueprint Header Badge
  if (title) {
    pill(title.toUpperCase(), 0, -h / 2 - 2, 42, C.cyan, C.navy, 1);
  }
  if (code) {
    pill(code, w / 2 - 80, -h / 2 + 40, 24, C.navyGrid, C.cyanLight, 1);
  }
  ctx.restore();
}

// Dimension Caliper Line
export function caliper(x1, y1, x2, y2, label = '', color = C.cyan, bg = C.ink, fg = C.white) {
  ctx.save();
  const dx = x2 - x1, dy = y2 - y1, len = Math.hypot(dx, dy);
  const ang = Math.atan2(dy, dx);
  ctx.translate(x1, y1); ctx.rotate(ang);
  
  // Main measurement line
  ctx.strokeStyle = color; ctx.lineWidth = 3; ctx.setLineDash([10, 6]);
  ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(len, 0); ctx.stroke();
  ctx.setLineDash([]);
  
  // End ticks
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(0, -18); ctx.lineTo(0, 18);
  ctx.moveTo(len, -18); ctx.lineTo(len, 18);
  ctx.stroke();
  
  // Measurement Label Pill
  if (label) {
    pill(label, len / 2, 0, 28, bg, fg, 1);
  }
  ctx.restore();
}

// Flow Vector with Traveling Sparks
export function flowVector(pts, progress = 0, color = C.cyan, width = 8) {
  if (pts.length < 2) return;
  line(pts, color, width);
  
  // Draw traveling pulse
  const segIdx = Math.floor(progress * (pts.length - 1));
  const tSeg = (progress * (pts.length - 1)) % 1;
  const p0 = pts[Math.min(segIdx, pts.length - 2)];
  const p1 = pts[Math.min(segIdx + 1, pts.length - 1)];
  const px = lerp(p0[0], p1[0], tSeg);
  const py = lerp(p0[1], p1[1], tSeg);
  
  circle(px, py, 14, C.yellow, C.white, 3);
}

// Pill Badge
export function pill(text, x, y, size = 48, bg = C.ink, fg = C.white, sc = 1) {
  if (sc <= 0) return;
  ctx.save(); ctx.translate(x, y); ctx.scale(sc, sc);
  ctx.font = `900 ${size}px Inter`; ctx.letterSpacing = '1px';
  const pad = size * 0.9;
  const w = ctx.measureText(text).width + pad * 2, h = size * 1.6;
  rr(-w / 2, -h / 2, w, h, h / 2);
  ctx.fillStyle = bg; ctx.fill();
  ctx.lineWidth = 4; ctx.strokeStyle = C.ink; ctx.stroke();
  ctx.fillStyle = fg; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(text, 0, size * 0.04);
  ctx.letterSpacing = '0px';
  ctx.restore();
}

// Schematic Pointer Tag
export function tag(label, x, y, tx, ty, size = 48, sc = 1, bg = C.ink, fg = C.white) {
  if (sc <= 0) return;
  ctx.save();
  ctx.globalAlpha = clamp(sc);
  line([[x, y], [tx, ty]], C.ink, 6, [10, 8]);
  circle(tx, ty, 8, C.yellow, C.ink, 4);
  ctx.restore();
  pill(label, x, y, size, bg, fg, sc);
}

// Hazard Red Warning X
export function redX(x, y, s = 1, a = 1) {
  if (a <= 0) return;
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.globalAlpha = a;
  ctx.lineCap = 'round';
  for (const [w, c] of [[84, C.ink], [60, C.red]]) {
    ctx.strokeStyle = c; ctx.lineWidth = w;
    ctx.beginPath();
    ctx.moveTo(-180, -180); ctx.lineTo(180, 180);
    ctx.moveTo(180, -180); ctx.lineTo(-180, 180);
    ctx.stroke();
  }
  ctx.restore();
}

// Safety Green Passing Checkmark
export function greenCheck(x, y, s = 1, a = 1) {
  if (a <= 0) return;
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.globalAlpha = a;
  circle(0, 0, 140, C.green, C.ink, 14);
  ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  ctx.strokeStyle = C.white; ctx.lineWidth = 26;
  ctx.beginPath();
  ctx.moveTo(-60, 5); ctx.lineTo(-15, 55); ctx.lineTo(75, -45);
  ctx.stroke();
  ctx.restore();
}

// Core Efficiency Metric Graphic
export function metricDisplay(x, y, value, unit, label, sc = 1, isNavy = true) {
  if (sc <= 0) return;
  ctx.save(); ctx.translate(x, y); ctx.scale(sc, sc);
  
  const w = 680, h = 380;
  rr(-w / 2, -h / 2, w, h, 28);
  ctx.fillStyle = isNavy ? C.navy : C.white; ctx.fill();
  ctx.lineWidth = 8; ctx.strokeStyle = isNavy ? C.cyan : C.ink; ctx.stroke();
  
  // Dashed inner frame
  rr(-w / 2 + 16, -h / 2 + 16, w - 32, h - 32, 18);
  ctx.lineWidth = 2; ctx.strokeStyle = isNavy ? C.cyanLight : C.gray;
  ctx.setLineDash([8, 6]); ctx.stroke(); ctx.setLineDash([]);
  
  // Label on top
  pill(label.toUpperCase(), 0, -h / 2 + 45, 34, isNavy ? C.navyGrid : C.grayLight, isNavy ? C.cyan : C.ink, 1);
  
  // Big Value
  ctx.font = '900 135px Inter'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillStyle = C.yellow;
  ctx.fillText(value, 0, 15);
  
  // Unit Subtext
  ctx.font = '900 48px Inter'; ctx.fillStyle = isNavy ? C.white : C.ink;
  ctx.fillText(unit, 0, 120);
  
  ctx.restore();
}

// Outlined bold text for punchy callouts
export function bigText(text, x, y, size, fill = C.white, rot = 0, sc = 1) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc);
  ctx.font = `900 ${size}px Inter`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.lineJoin = 'round';
  ctx.lineWidth = size * 0.22; ctx.strokeStyle = C.ink; ctx.strokeText(text, 0, 0); ctx.fillStyle = fill; ctx.fillText(text, 0, 0);
  ctx.restore();
}
