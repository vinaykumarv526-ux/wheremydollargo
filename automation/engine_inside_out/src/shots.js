// 2D Flat Architectural Explainer: Shot Controller
// 9-Cut Progression, safe zone anchored at cam: [540, 760]
import { ctx, C, W, H, fillAll } from './core/lib.js';
import { L, Le, Wd, T } from './core/timing.js';
import * as K from './core/taxKit.js';

export function buildShots() {
  const S = [], CUES = [];
  const add = (o) => (S.push(o), o);
  const cue = (t, type, o = {}) => CUES.push({ t: +t.toFixed(3), type, ...o });
  const cut = (i) => (i === 0 ? 0 : L(i) - 0.08);

  // ── Cut 1: The Hook (Why do countries collect taxes?) ───────────────────
  {
    const st = cut(0);
    add({
      id: 'S01', at: st, cam: [540, 760], zoom: 0.05, note: 'Hero civic treasury structure',
      draw(lt) {
        fillAll(C.bg);
        K.heroCivicTreasury(540, 740, 1.0);
      }
    });
    cue(st + 0.1, 'whoosh');
    cue(st + 0.4, 'pop', { gain: 0.6 });
  }

  // ── Cut 2: The Flawed Myth (Takes hard-earned cash) ─────────────────────
  {
    const st = cut(1);
    add({
      id: 'S02', at: st, cam: [540, 760], zoom: 0.04, note: 'Citizen flaw myth representation',
      draw(lt) {
        fillAll(C.bg);
        K.flawedMythScene(540, 760, 1.0, lt);
      }
    });
    cue(st, 'whoosh');
    cue(st + 0.35, 'pop', { gain: 0.65 });
  }

  // ── Cut 3: The Failure Point (Zero taxes collapse) ───────────────────────
  {
    const st = cut(2);
    add({
      id: 'S03', at: st, cam: [540, 760], zoom: 0.06, note: 'Crumbling system failure point',
      draw(lt) {
        fillAll(C.navyDark);
        K.failurePointScene(540, 760, 1.0, lt);
      }
    });
    cue(st, 'whoosh');
    cue(st + 0.25, 'slam');
  }

  // ── Cut 4: The Architectural Secret (Civic Subscription) ────────────────
  {
    const st = cut(3);
    add({
      id: 'S04', at: st, cam: [540, 760], zoom: 0.05, note: 'Blueprint core cutaway',
      draw(lt) {
        fillAll(C.navyDark);
        K.architecturalCutaway(540, 760, 1.0, lt);
      }
    });
    cue(st, 'whoosh');
    cue(st + 0.3, 'pop', { gain: 0.7 });
  }

  // ── Cut 5: Dynamics & Flow (Three Inflow Pipelines) ──────────────────────
  {
    const st = cut(4);
    add({
      id: 'S05', at: st, cam: [540, 760], zoom: 0.05, note: 'Dynamic 3-pipeline liquidity flow',
      draw(lt) {
        fillAll(C.navyDark);
        K.threePipelineFlow(540, 760, 1.0, lt);
      }
    });
    cue(st, 'whoosh');
    cue(st + 0.25, 'slide', { dur: 1.2 });
  }

  // ── Cut 6: Self-Balancing Loop (Redistribution & Stability) ──────────────
  {
    const st = cut(5);
    add({
      id: 'S06', at: st, cam: [540, 760], zoom: 0.05, note: 'Self-balancing civic feedback loop',
      draw(lt) {
        fillAll(C.navyDark);
        K.redistributionLoop(540, 760, 1.0, lt);
      }
    });
    cue(st, 'whoosh');
    cue(st + 0.35, 'pop', { gain: 0.65 });
  }

  // ── Cut 7: Engine X-Ray (Collective Bulk Power) ──────────────────────────
  {
    const st = cut(6);
    add({
      id: 'S07', at: st, cam: [540, 760], zoom: 0.05, note: 'Collective purchasing power x-ray',
      draw(lt) {
        fillAll(C.navyDark);
        K.engineXRayScene(540, 760, 1.0, lt);
      }
    });
    cue(st, 'whoosh');
    cue(st + 0.3, 'pop', { gain: 0.7 });
  }

  // ── Cut 8: Efficiency Metric (Five Trillion Scale) ───────────────────────
  {
    const st = cut(7);
    add({
      id: 'S08', at: st, cam: [540, 760], zoom: 0.05, note: 'Hard efficiency metric close-up',
      draw(lt) {
        fillAll(C.navyDark);
        K.efficiencyMetricScene(540, 760, 1.0, lt);
      }
    });
    cue(st, 'whoosh');
    cue(st + 0.25, 'pop', { gain: 0.8 });
  }

  // ── Cut 9: Loop Outro (Engine of Society) ────────────────────────────────
  {
    const st = cut(8);
    add({
      id: 'S09', at: st, cam: [540, 760], zoom: 0.04, note: 'Illuminated resolution looping back to Hook',
      draw(lt) {
        fillAll(C.bg);
        K.loopOutroScene(540, 740, 1.0, lt);
      }
    });
    cue(st, 'whoosh');
    cue(st + 0.2, 'ding', { gain: 0.8 });
  }

  return { shots: S, cues: CUES };
}
