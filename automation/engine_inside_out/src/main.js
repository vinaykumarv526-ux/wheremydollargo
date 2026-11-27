// 2D Flat Architectural Explainer Engine - Main Boot & Camera System
import { W, H, setCtx, ctx, clamp, eo, eio, C } from './core/lib.js';
import { T, loadTiming } from './core/timing.js';
import { buildCaptions, drawCaption, captionList } from './core/captions.js';
import { buildShots } from './shots.js';

const cv = document.getElementById('cv');
setCtx(cv.getContext('2d'));
const OP = (window.OP = { ready: false });

function draw(t) {
  t = clamp(t, 0, T.dur - 1e-4);
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.globalAlpha = 1;
  ctx.letterSpacing = '0px';
  ctx.fillStyle = C.navyDark;
  ctx.fillRect(0, 0, W, H);

  const S = OP._shots;
  let i = S.length - 1;
  while (i > 0 && S[i].at > t) i--;

  const sh = S[i];
  const end = i < S.length - 1 ? S[i + 1].at : T.dur;
  const d = end - sh.at;
  const lt = t - sh.at;

  // Architectural Camera: punch-in on cut + continuous technical push
  const punch = 1 + 0.10 * (1 - eo(clamp(lt / 0.28)));
  const drift = 1 + (sh.zoom ?? 0.05) * eio(clamp(lt / d));
  // Default camera target anchored in upper safe zone (540, 760)
  const [cx, cy] = sh.cam || [540, 760];

  ctx.save();
  ctx.translate(cx, cy);
  ctx.scale(punch * drift, punch * drift);
  ctx.translate(-cx, -cy);

  // Draw bespoke architectural scene
  sh.draw(lt, d, t);
  ctx.restore();

  // Subtle cut transition flash
  ctx.globalAlpha = 1;
  ctx.letterSpacing = '0px';
  if (i > 0 && lt < 0.10) {
    ctx.fillStyle = '#FFFFFF';
    ctx.globalAlpha = 0.45 * (1 - lt / 0.10);
    ctx.fillRect(0, 0, W, H);
    ctx.globalAlpha = 1;
  }

  // Smooth intro / outro fades
  const fade = Math.min(clamp(t / 0.2), clamp((T.dur - t) / 0.3));
  if (fade < 1) {
    ctx.fillStyle = '#000000';
    ctx.globalAlpha = 1 - fade;
    ctx.fillRect(0, 0, W, H);
    ctx.globalAlpha = 1;
  }

  // Word-synced karaoke captions in bottom safe zone (y: 1420)
  drawCaption(t);
}

(async () => {
  try {
    await document.fonts.load('900 90px Inter');
    const script = await (await fetch('script.json', { cache: 'no-store' })).json();
    await loadTiming();
    buildCaptions(script);
    const { shots, cues } = buildShots();
    shots.sort((a, b) => a.at - b.at);

    OP._shots = shots;
    OP.script = script;
    OP.duration = () => T.dur;
    OP.draw = draw;
    OP.frame = (t, q = 0.92) => {
      draw(t);
      return cv.toDataURL('image/jpeg', q);
    };
    OP.shots = () =>
      shots.map((s, i) => ({
        id: s.id,
        at: +s.at.toFixed(3),
        end: +(i < shots.length - 1 ? shots[i + 1].at : T.dur).toFixed(3),
        note: s.note || '',
      }));
    OP.captions = () =>
      captionList().map((c) => ({
        s: +c.s.toFixed(3),
        e: +c.e.toFixed(3),
        text: c.words.map((w) => (w.hi ? '*' : '') + w.txt).join(' '),
      }));
    OP.cues = () => cues.slice().sort((a, b) => a.t - b.t);
    OP.ready = true;

    // Interactive preview player
    const q = new URLSearchParams(location.search);
    if (!q.has('capture')) {
      if (q.has('t')) {
        draw(+q.get('t'));
      } else {
        const audio = new Audio('data/mix.wav');
        let t0 = null;
        const btn = document.getElementById('play');
        if (btn) {
          btn.hidden = false;
          btn.onclick = () => {
            btn.hidden = true;
            t0 = performance.now();
            audio.currentTime = 0;
            audio.play().catch(() => {});
          };
        }
        const loop = (now) => {
          const t = t0 == null ? 0 : (now - t0) / 1000;
          draw(t0 == null ? 0 : t);
          if (t0 != null && t > T.dur) {
            t0 = null;
            if (btn) btn.hidden = false;
          }
          requestAnimationFrame(loop);
        };
        requestAnimationFrame(loop);
      }
    }
  } catch (e) {
    OP.bootError = String((e && e.stack) || e);
    console.error(e);
  }
})();
