// Timing engine: coordinates spoken lines and word-by-word timestamps
export const T = { dur: 30, lines: [], words: [] };

export async function loadTiming() {
  const [lr, wr] = await Promise.all([
    fetch('data/lines.json', { cache: 'no-store' }),
    fetch('data/words.json', { cache: 'no-store' }),
  ]);
  const ld = await lr.json();
  const wd = await wr.json();
  
  T.lines = Array.isArray(ld) ? ld : ld.lines;
  T.words = Array.isArray(wd) ? wd : wd.words;
  T.dur = Math.max(
    T.lines.length ? T.lines[T.lines.length - 1].end + 0.6 : 30,
    T.words.length ? T.words[T.words.length - 1].e + 0.6 : 30
  );
  return T;
}

export function L(i) {
  if (i < 0) return 0;
  if (!T.lines[i]) return i * 3.2;
  return T.lines[i].start;
}

export function Le(i) {
  if (i < 0) return 0;
  if (!T.lines[i]) return (i + 1) * 3.2;
  return T.lines[i].end;
}

export function lineWords(i) {
  return T.words.filter((w) => w.line === i);
}

export function Wd(word, lineIdx) {
  const ws = lineWords(lineIdx);
  const clean = (s) => String(s).toLowerCase().replace(/[^a-z0-9]/g, '');
  const target = clean(word);
  const found = ws.find((w) => clean(w.w).includes(target) || target.includes(clean(w.w)));
  if (found) return found.s;
  return L(lineIdx) + 0.4;
}
