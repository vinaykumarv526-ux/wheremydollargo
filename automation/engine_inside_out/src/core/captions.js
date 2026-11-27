// 2D Flat Architectural Explainer Engine - Caption System
// 1 to 3 words on screen, Inter 900 bold, white with thick dark ink outline,
// exactly ONE yellow (#FFD43B) highlighted keyword per chunk, bottom safe zone (y: 1420).
import { ctx, C, clamp, lerp, seg, eob } from './lib.js';
import { T, lineWords } from './timing.js';

export const CAP = { y: 1420, size: 92, maxW: 960 };
let caps = [];

function autoChunks(text) {
  const ws = text.toUpperCase().split(/\s+/).filter(Boolean), out = [];
  for (let i = 0; i < ws.length;) {
    const n = ws.length - i === 4 ? 2 : Math.min(3, ws.length - i);
    out.push(ws.slice(i, i + n));
    i += n;
  }
  return out.map((c) => {
    const k = c.reduce((b, w, j) => (w.replace(/[^A-Z]/g, '').length > c[b].replace(/[^A-Z]/g, '').length ? j : b), 0);
    return c.map((w, j) => (j === k ? '*' + w : w)).join(' ');
  });
}

export function buildCaptions(script) {
  caps = [];
  script.lines.forEach((ln, i) => {
    const chunks = (ln.caps ? ln.caps.split('|') : autoChunks(ln.text)).map((s) => s.trim()).filter(Boolean);
    const ws = lineWords(i);
    if (!ws.length) return;
    const counts = chunks.map((c) => c.split(/\s+/).length), N = counts.reduce((a, b) => a + b, 0);
    const nm = (w) => String(w).toLowerCase().replace(/[^a-z0-9']+/g, '');
    let acc = 0, from = 0;
    
    chunks.forEach((c, j) => {
      const first = nm(c.split(/\s+/)[0]);
      let idx = j === 0 ? 0 : ws.findIndex((w, k) => k > from && first && (nm(w.w) === first || (first.length > 2 && nm(w.w).startsWith(first))));
      if (idx < 0) idx = Math.max(from + (j ? 1 : 0), Math.min(ws.length - 1, Math.round(acc * ws.length / N)));
      acc += counts[j]; from = idx;
      
      caps.push({
        line: i,
        s: ws[idx].s - 0.05,
        words: c.split(/\s+/).map((w) => ({
          txt: w.replace(/\*/g, ''),
          hi: w.includes('*')
        }))
      });
    });
  });

  caps.forEach((c, k) => {
    const next = caps[k + 1];
    const lineEnd = T.lines[c.line] ? T.lines[c.line].end : c.s + 2.0;
    c.e = next ? (next.s - lineEnd > 0.7 && next.line !== c.line ? lineEnd + 0.35 : next.s) : T.dur;
  });

  return caps;
}

export const captionList = () => caps;

export function drawCaption(t) {
  const c = caps.find((c) => t >= c.s && t < c.e);
  if (!c) return;
  const lt = t - c.s, size = CAP.size;
  ctx.save();
  ctx.font = `900 ${size}px Inter`;
  ctx.letterSpacing = '-1px';
  const sp = size * 0.28;
  c.words.forEach((w) => (w.w = ctx.measureText(w.txt).width));
  const width = (ws) => ws.reduce((a, w) => a + w.w, 0) + sp * (ws.length - 1);
  
  let lines = [c.words];
  if (width(c.words) > CAP.maxW && c.words.length > 1) {
    let best = null;
    for (let i = 1; i < c.words.length; i++) {
      const a = c.words.slice(0, i), b = c.words.slice(i), m = Math.max(width(a), width(b));
      if (!best || m < best.m) best = { m, l: [a, b] };
    }
    lines = best.l;
  }
  
  const fit = Math.min(1, CAP.maxW / Math.max(...lines.map(width)));
  const sc = (lt < 0.18 ? lerp(0.75, 1, eob(seg(lt, 0, 0.18))) : 1) * fit;
  
  ctx.translate(540, CAP.y);
  ctx.scale(sc, sc);
  ctx.textBaseline = 'middle';
  ctx.textAlign = 'left';
  ctx.lineJoin = 'round';
  
  const lh = size * 1.05, y0 = -(lines.length - 1) * lh / 2;
  lines.forEach((ln, li) => {
    let x = -width(ln) / 2;
    const y = y0 + li * lh;
    for (const w of ln) {
      // Thick technical ink outline
      ctx.lineWidth = 24;
      ctx.strokeStyle = C.ink;
      ctx.strokeText(w.txt, x, y + 8);
      ctx.strokeText(w.txt, x, y);
      
      // Keyword in attention yellow, others in pure white
      ctx.fillStyle = w.hi ? C.yellow : C.white;
      ctx.fillText(w.txt, x, y);
      x += w.w + sp;
    }
  });
  
  ctx.letterSpacing = '0px';
  ctx.restore();
}
