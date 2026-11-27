// Bespoke Architectural Vector Kit: What is a Tax?
// Strict palette compliance: #F4F1EA, #0E1A2B, #1A1A1E, #38BDF8, #FFD43B, #EF4444, #10B981
import { ctx, C, TAU, clamp, lerp, seg, eo, eio, eob, rnd, rr, circle, ell, line, pill, tag, redX, greenCheck, blueprintBox, caliper, flowVector } from './lib.js';

// 1. Hero Civic Entity (Cut 1: Hook)
export function heroCivicTreasury(x, y, s = 1) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  
  // Base architectural ground
  rr(-360, 180, 720, 24, 12); ctx.fillStyle = C.ink; ctx.fill();
  
  // Treasury Building (Classical Flat Architectural Cross-section)
  // Steps
  rr(-320, 140, 640, 40, 8); ctx.fillStyle = C.grayLight; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.stroke();
  rr(-280, 100, 560, 40, 8); ctx.fillStyle = C.white; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.stroke();
  
  // Columns
  for (const cx of [-220, -110, 0, 110, 220]) {
    rr(cx - 24, -140, 48, 240, 6); ctx.fillStyle = C.white; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.stroke();
  }
  
  // Pediment / Triangular Roof
  ctx.beginPath(); ctx.moveTo(-290, -140); ctx.lineTo(0, -290); ctx.lineTo(290, -140); ctx.closePath();
  ctx.fillStyle = C.white; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 8; ctx.stroke();
  
  // Central Emblem
  circle(0, -200, 42, C.yellow, C.ink, 6);
  ctx.font = '900 52px Inter'; ctx.fillStyle = C.ink; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText('$', 0, -196);
  
  // Schematic Caliper
  caliper(-300, 230, 300, 230, 'NATION-STATE CIVIC CORE', C.ink, C.ink, C.yellow);
  ctx.restore();
}

// 2. Flawed Myth Citizen View (Cut 2: The Myth)
export function flawedMythScene(x, y, s = 1, lt = 0) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  
  // Citizen entity
  // Head
  circle(-140, -160, 70, C.white, C.ink, 6);
  circle(-160, -170, 8, C.ink); circle(-120, -170, 8, C.ink);
  // Frown
  ctx.beginPath(); ctx.arc(-140, -135, 24, Math.PI, 0); ctx.lineWidth = 5; ctx.strokeStyle = C.ink; ctx.stroke();
  
  // Body
  rr(-210, -80, 140, 220, 24); ctx.fillStyle = C.grayLight; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.stroke();
  
  // Wallet / Outflow
  rr(110, -50, 180, 120, 16); ctx.fillStyle = C.white; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.stroke();
  circle(200, 10, 28, C.yellow, C.ink, 4);
  
  // Siphoning line with question mark
  line([[-70, 10], [110, 10]], C.red, 8, [12, 8]);
  tag('THE POPULAR MYTH', 0, -280, 0, -20, 46, eob(seg(lt, 0.1, 0.4)), C.ink, C.yellow);
  pill('"THEY JUST TAKE IT?"', 0, 180, 40, C.red, C.white, eob(seg(lt, 0.3, 0.6)));
  
  ctx.restore();
}

// 3. Infrastructure Failure Point (Cut 3: Failure Mode)
export function failurePointScene(x, y, s = 1, lt = 0) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  
  // Collapsed bridge / crumbling civic structure
  blueprintBox(0, 0, 860, 680, 'CIVIC SYSTEM BREAKDOWN', 'FAIL-03');
  
  // Broken bridge road line
  line([[-360, 40], [-60, 40]], C.gray, 18);
  line([[60, 120], [360, 120]], C.gray, 18);
  
  // Fracture crack
  ctx.beginPath();
  ctx.moveTo(-60, 40); ctx.lineTo(-10, 80); ctx.lineTo(15, 60); ctx.lineTo(60, 120);
  ctx.lineWidth = 8; ctx.strokeStyle = C.red; ctx.stroke();
  
  // Stress concentration rays
  for (let i = 0; i < 6; i++) {
    const an = i * (Math.PI / 3);
    line([[Math.cos(an) * 50, 80 + Math.sin(an) * 50], [Math.cos(an) * 90, 80 + Math.sin(an) * 90]], C.yellow, 6);
  }
  
  // Red X on top of collapse
  redX(0, 70, lerp(1.8, 1.0, eob(seg(lt, 0.2, 0.45))), lt > 0.15 ? 1 : 0);
  tag('ZERO CIVIC REVENUE', 0, -210, 0, -20, 44, eob(seg(lt, 0.3, 0.55)), C.red, C.white);
  pill('CRITICAL INFRASTRUCTURE FAILURE', 0, 240, 36, C.red, C.white, eob(seg(lt, 0.4, 0.65)));
  
  ctx.restore();
}

// 4. Architectural Schematic Cutaway (Cut 4: Hidden Engine)
export function architecturalCutaway(x, y, s = 1, lt = 0) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  
  blueprintBox(0, 0, 880, 720, 'CIVIC SUBSCRIPTION CORE', 'ARCH-04');
  
  // Internal central reservoir (The Public Trust Pool)
  circle(0, 20, 180, C.navyDark, C.cyan, 8);
  
  // Concentric Fresnel groove arcs
  for (let r = 80; r <= 150; r += 35) {
    ctx.beginPath(); ctx.arc(0, 20, r, 0, TAU);
    ctx.strokeStyle = C.cyan; ctx.lineWidth = 2; ctx.setLineDash([12, 10]); ctx.stroke();
    ctx.setLineDash([]);
  }
  
  // Center Vault
  circle(0, 20, 50, C.yellow, C.ink, 6);
  ctx.font = '900 48px Inter'; ctx.fillStyle = C.ink; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText('$', 0, 24);
  
  // Caliper measurement
  caliper(-360, 240, 360, 240, 'SOCIETAL POOLED RESERVE', C.cyan);
  
  tag('COLLECTIVE SUBSCRIPTION', 0, -250, 0, -160, 44, eob(seg(lt, 0.1, 0.4)), C.cyan, C.navy);
  pill('SOCIETY OPERATING SYSTEM', 0, 310, 36, C.yellow, C.navy, eob(seg(lt, 0.3, 0.6)));
  
  ctx.restore();
}

// 5. Dynamic 3-Pipeline Flow (Cut 5: Dynamics & Flow)
export function threePipelineFlow(x, y, s = 1, lt = 0) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  
  blueprintBox(0, 0, 880, 720, 'MULTI-VECTOR INFLOW DYNAMICS', 'FLOW-05');
  
  // 3 Input Nodes (Top)
  const inputs = [
    { label: 'INCOME', x: -270, y: -200 },
    { label: 'SALES', x: 0, y: -240 },
    { label: 'PROPERTY', x: 270, y: -200 },
  ];
  
  const target = [0, 140];
  
  // Draw Flow Vectors FIRST
  inputs.forEach((inp, idx) => {
    const progress = (lt * 1.5 + idx * 0.33) % 1;
    flowVector([[inp.x, inp.y + 30], [inp.x * 0.35, 10], target], progress, C.cyan, 8);
  });
  
  // Central Inflow Basin
  circle(0, 140, 110, C.navyDark, C.cyan, 8);
  pill('CENTRAL TREASURY', 0, 140, 32, C.cyan, C.navy, 1);
  
  // Draw Input Pills on top
  inputs.forEach((inp) => {
    pill(inp.label, inp.x, inp.y, 34, C.yellow, C.ink, 1);
  });
  
  pill('THREE INPUT REVENUE PIPELINES', 0, -40, 34, C.navyDark, C.cyanLight, 1);
  pill('CONTINUOUS LIQUIDITY INFLOW', 0, 305, 34, C.cyan, C.navy, 1);
  
  ctx.restore();
}

// 6. Self-Balancing Redistribution Loop (Cut 6: Balance Loop)
export function redistributionLoop(x, y, s = 1, lt = 0) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  
  blueprintBox(0, 0, 880, 720, 'CLOSED-LOOP REDISTRIBUTION', 'LOOP-06');
  
  // 4 Output Spokes
  const nodes = [
    { label: 'PUBLIC ROADS', x: -260, y: -130 },
    { label: 'HOSPITALS', x: 260, y: -130 },
    { label: 'SECURITY', x: -260, y: 130 },
    { label: 'CLEAN WATER', x: 260, y: 130 }
  ];
  
  // Draw Flow Lines FIRST
  nodes.forEach((n, idx) => {
    const progress = (lt * 1.2 + idx * 0.25) % 1;
    flowVector([[0, 0], [n.x * 0.5, n.y], [n.x, n.y]], progress, C.green, 6);
  });
  
  // Center treasury hub
  circle(0, 0, 110, C.navyDark, C.green, 8);
  greenCheck(0, 0, 0.65, eob(seg(lt, 0.25, 0.55)));
  
  // Draw Spoke Pills OVER the lines for 100% legibility
  nodes.forEach((n) => {
    pill(n.label, n.x, n.y, 32, C.navyDark, C.cyanLight, 1);
  });
  
  pill('SELF-STABILIZING CIVIC FEEDBACK', 0, 305, 34, C.green, C.navy, eob(seg(lt, 0.35, 0.65)));
  
  ctx.restore();
}

// 7. Engine X-Ray Sub-Component (Cut 7: Detailed X-Ray)
export function engineXRayScene(x, y, s = 1, lt = 0) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  
  blueprintBox(0, 0, 880, 720, 'COLLECTIVE BARGAINING X-RAY', 'XRAY-07');
  
  // Side-by-side comparison cross section
  // Left: Individual Buying (Inefficient)
  rr(-380, -180, 340, 380, 20); ctx.fillStyle = C.navyDark; ctx.fill(); ctx.strokeStyle = C.red; ctx.lineWidth = 4; ctx.stroke();
  pill('INDIVIDUAL PAYER', -210, -135, 28, C.red, C.white, 1);
  
  const items = ['$10,000 / ROAD', '$4,500 / AMBULANCE', '$1,200 / SECURITY'];
  items.forEach((txt, i) => {
    circle(-330, -50 + i * 70, 12, C.red);
    pill(txt, -190, -50 + i * 70, 24, C.navyDark, C.red, 1);
  });
  
  // Right: Pooled Public Bulk Purchasing (Efficient)
  rr(40, -180, 340, 380, 20); ctx.fillStyle = C.navyDark; ctx.fill(); ctx.strokeStyle = C.green; ctx.lineWidth = 4; ctx.stroke();
  pill('POOLED CIVIC BUDGET', 210, -135, 28, C.green, C.navy, 1);
  circle(210, 30, 80, C.yellow, C.ink, 6);
  pill('10x LEVERAGE', 210, 30, 36, C.ink, C.yellow, 1);
  
  pill('10X EFFICIENCY MULTIPLIER', 0, 235, 36, C.green, C.navy, eob(seg(lt, 0.2, 0.5)));
  pill('BULK PUBLIC PURCHASING POWER', 0, 305, 34, C.cyan, C.navy, 1);
  
  ctx.restore();
}

// 8. Core Efficiency Metric (Cut 8: Metric Display)
export function efficiencyMetricScene(x, y, s = 1, lt = 0) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  blueprintBox(0, 0, 880, 720, 'ANNUAL AGGREGATE LEVERAGE', 'METRIC-08');
  
  // Metric card
  const pop = eob(seg(lt, 0.15, 0.45));
  ctx.save(); ctx.scale(pop, pop);
  
  // Big Metric Value
  ctx.font = '900 135px Inter'; ctx.fillStyle = C.yellow; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText('$5.1 TRILLION', 0, -20);
  
  pill('ANNUAL US CIVIC POOL', 0, 80, 44, C.cyan, C.navy, 1);
  caliper(-360, 180, 360, 180, 'COLLECTIVE SCALE LEVERAGE', C.cyan);
  
  tag('SHARED INFRASTRUCTURE POWER', 0, -180, 0, -90, 40, 1, C.yellow, C.navy);
  ctx.restore();
  
  pill('RESOURCES SCALE BEYOND INDIVIDUAL CAPACITY', 0, 305, 32, C.navyDark, C.cyanLight, 1);
  ctx.restore();
}

// 9. Loop Outro (Cut 9: Loop Outro)
export function loopOutroScene(x, y, s = 1, lt = 0) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  
  // Illuminated civic architecture returning to Cut 1
  heroCivicTreasury(0, 20, 0.95);
  
  greenCheck(0, -60, 0.85, eob(seg(lt, 0.15, 0.45)));
  pill('NOT A PENALTY: THE ENGINE OF MODERN SOCIETY', 0, 280, 36, C.green, C.navy, eob(seg(lt, 0.25, 0.55)));
  
  ctx.restore();
}
