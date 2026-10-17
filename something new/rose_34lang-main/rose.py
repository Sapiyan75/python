import math as m
import random as r
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="A Rose Written in Every Language",
    page_icon="🌹",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #060208;
    }
    </style>
""",
    unsafe_allow_html=True,
)

rose_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  body {
    background-color: #060208;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    overflow: hidden;
  }
  canvas {
    background: #060208;
  }
</style>
</head>
<body>
<canvas id="roseCanvas" width="800" height="800"></canvas>
<script>
const canvas = document.getElementById('roseCanvas');
const ctx = canvas.getContext('2d');

const W = 800, H = 800;
const DURATION = 10;
const TICK = 16;
const ANIM = 38;
const LIFT = 32;
const GAP = 3;
const BG = "#060208";
const SEED = 17;

const PHRASES = [
    "I LOVE YOU", "I love you", "Te amo", "Ti amo", "Je t'aime",
    "Ich liebe dich", "Eu te amo", "Seni seviyorum", "Я тебя люблю",
    "사랑해", "愛してる", "我爱你", "मैं तुमसे प्यार करती हूँ",
    "मैं तुमसे प्यार करता हूँ", "Σ' αγαπώ", "Ik hou van jou",
    "Jag älskar dig", "Kocham cię", "ฉันรักคุณ", "Anh yêu em",
    "Aku cinta kamu", "Mahal kita", "אני אוהבת אותך", "أحبك",
    "నేను నిన్ను ప్రేమిస్తున్నాను", "நான் உன்னை காதலிக்கிறேன்",
    "আমি তোমাকে ভালোবাসি", "Volim te", "Te iubesc", "Ljubim te",
    "Nakupenda", "Я тебе кохаю", "Miluji tě", "Szeretlek",
    "Rakastan sinua", "Jeg elsker dig"
];

const ACCENTS = [
    "LOVE", "TE AMO", "AMOUR", "TI AMO", "I LOVE YOU", "AMOR",
    "愛してる", "사랑해", "我爱你", "LOVE YOU", "JE T'AIME",
    "SZERETLEK", "NAKUPENDA"
];

const SHORT_PHRASES = [
    "Te amo", "Ti amo", "AMOR", "LOVE", "愛してる", "사랑해", "我爱你",
    "Amour", "I love you", "Mahal kita", "Te iubesc", "Volim te",
    "Szeretlek", "Miluji tě", "Nakupenda"
];

const HEAD_WORDS = PHRASES.concat([
    "LOVE", "LOVE", "LOVE YOU", "AMOR", "AMOR", "AMOUR", "AMOUR",
    "AMORE", "LIEBE", "TE AMO", "TE AMO", "TI AMO", "TI AMO",
    "TE QUIERO", "TE QUIERO", "JE T'AIME", "I LOVE YOU", "I LOVE YOU",
    "愛", "愛してる", "愛してる", "사랑", "사랑해", "사랑해", "我爱你",
    "Mahal kita", "รักคุณ", "ANH YÊU EM", "तुमसे प्यार है",
    "నిన్ను ప్రేమిస్తున్నా", "உன்னை காதலிக்கிறேன்", "ভালোবাসি",
    "أحبك", "LOVE", "AMOR", "AMOUR", "Nakupenda", "Szeretlek"
]);

const HEAD_SIZES = [7, 8, 9, 10, 11, 12, 13, 14];
const HEAD_WEIGHTS = [2, 4, 5, 5, 4, 2, 1, 0.5];

// Custom seeded Pseudo-Random Number Generator matching Python's random.Random(17)
class MathRandom {
    constructor(seed) {
        this.m = 0x80000000;
        this.a = 1103515245;
        this.c = 12345;
        this.state = seed ? seed : Math.floor(Math.random() * (this.m - 1));
    }
    nextInt() {
        this.state = (this.a * this.state + this.c) % this.m;
        return this.state;
    }
    nextFloat() {
        return this.nextInt() / (this.m - 1);
    }
    choice(array) {
        return array[Math.floor(this.nextFloat() * array.length)];
    }
    choices(array, weights) {
        let total = weights.reduce((a, b) => a + b, 0);
        let r = this.nextFloat() * total;
        for (let i = 0; i < array.length; i++) {
            if (r < weights[i]) return array[i];
            r -= weights[i];
        }
        return array[array.length - 1];
    }
    uniform(min, max) {
        return min + this.nextFloat() * (max - min);
    }
    shuffle(array) {
        let arr = array.slice();
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(this.nextFloat() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }
}

const rng = new MathRandom(SEED);

function ellipse_poly(cx, cy, rx, ry, points=160) {
    let poly = [];
    for (let i = 0; i < points; i++) {
        let angle = 2 * Math.PI * i / points;
        poly.push([cx + rx * Math.cos(angle), cy + ry * Math.sin(angle)]);
    }
    return poly;
}

const HEAD_SHAPES = [
    ellipse_poly(400, 180, 145, 90),
    ellipse_poly(330, 180, 120, 83),
    ellipse_poly(470, 180, 120, 83),
    ellipse_poly(275, 260, 98, 112),
    ellipse_poly(525, 260, 98, 112),
    ellipse_poly(338, 325, 118, 126),
    ellipse_poly(462, 325, 118, 126),
    [[230, 330], [290, 365], [348, 414], [400, 532],
     [452, 414], [510, 365], [570, 330], [522, 452],
     [400, 542], [278, 452]]
];

const STEM = [[378, 493], [422, 493], [427, 752], [408, 772], [390, 760], [374, 600]];
const LEFT_LEAF = [[395, 594], [359, 554], [304, 535], [244, 541], [215, 562], [253, 609], [321, 631], [374, 617]];
const RIGHT_LEAF = [[406, 619], [442, 581], [491, 561], [553, 578], [578, 600], [535, 640], [476, 660], [425, 649]];

function hexToRgb(hex) {
    hex = hex.replace("#", "");
    return [
        parseInt(hex.substring(0, 2), 16) / 255,
        parseInt(hex.substring(2, 4), 16) / 255,
        parseInt(hex.substring(4, 6), 16) / 255
    ];
}

const BGC = hexToRgb(BG);

function mix(a, b, k) {
    return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k];
}

function hx(rgb) {
    let r = Math.floor(Math.max(0, Math.min(1, rgb[0])) * 255);
    let g = Math.floor(Math.max(0, Math.min(1, rgb[1])) * 255);
    let b = Math.floor(Math.max(0, Math.min(1, rgb[2])) * 255);
    return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
}

function polygon_spans(poly, y) {
    let xs = [];
    for (let i = 0; i < poly.length; i++) {
        let p1 = poly[i];
        let p2 = poly[(i + 1) % poly.length];
        let x1 = p1[0], y1 = p1[1];
        let x2 = p2[0], y2 = p2[1];
        if ((y1 <= y && y < y2) || (y2 <= y && y < y1)) {
            if (y2 !== y1) {
                xs.push(x1 + (y - y1) * (x2 - x1) / (y2 - y1));
            }
        }
    }
    xs.sort((a, b) => a - b);
    let spans = [];
    for (let i = 0; i < xs.length; i += 2) {
        if (i + 1 < xs.length) spans.push([xs[i], xs[i + 1]]);
    }
    return spans;
}

function merge_spans(spans) {
    if (!spans.length) return [];
    spans.sort((a, b) => a[0] - b[0]);
    let merged = [[spans[0][0], spans[0][1]]];
    for (let i = 1; i < spans.length; i++) {
        let lo = spans[i][0], hi = spans[i][1];
        if (lo <= merged[merged.length - 1][1] + 1) {
            merged[merged.length - 1][1] = Math.max(merged[merged.length - 1][1], hi);
        } else {
            merged.push([lo, hi]);
        }
    }
    return merged;
}

function shape_spans(polygons, y) {
    let raw = [];
    for (let poly of polygons) {
        raw.push(...polygon_spans(poly, y));
    }
    return merge_spans(raw);
}

function intersect_spans(a_spans, b_spans, minimum=15) {
    let out = [];
    for (let a of a_spans) {
        for (let b of b_spans) {
            let lo = Math.max(a[0], b[0]);
            let hi = Math.min(a[1], b[1]);
            if (hi - lo >= minimum) {
                out.push([lo, hi]);
            }
        }
    }
    return merge_spans(out);
}

function rose_color(x, y, size, edge=false) {
    let dx = (x - 400) / 210;
    let dy = (y - 300) / 220;
    let rad = Math.sqrt(dx * dx + dy * dy);
    let palette;
    if (rad > 0.82) {
        palette = ["#8f0b2b", "#ae1238", "#c41d48", "#d52b53"];
    } else if (rad > 0.48) {
        palette = ["#b9143d", "#d21e49", "#e33b60", "#f04e73"];
    } else {
        palette = ["#c51b49", "#e83c68", "#f16b8b", "#ff91a9"];
    }
    if (edge) palette = palette.concat(["#f5a0b3", "#ef6488"]);
    if (size >= 14) palette = palette.concat(["#ff9ab1", "#ffd0dc"]);
    return hexToRgb(rng.choice(palette));
}

function green_color(x, y, size, edge=false) {
    let palette = ["#3e8034", "#559c3c", "#72b84b", "#91cf62", "#b1e184"];
    if (size >= 9) palette = palette.concat(["#a7d486", "#c0e19a"]);
    return hexToRgb(rng.choice(palette));
}

let phrase_cycles = {};

function phrase_from_pool(pool_name, size) {
    let pool = size >= 14 ? ACCENTS : (pool_name !== "head" ? SHORT_PHRASES : HEAD_WORDS);
    let key = `${pool_name}_${size >= 14 ? "accent" : "normal"}`;
    if (!phrase_cycles[key] || !phrase_cycles[key].items.length) {
        let items = rng.shuffle(pool);
        phrase_cycles[key] = { items: items, index: 0 };
    }
    let state = phrase_cycles[key];
    let phrase = state.items[state.index];
    state.index++;
    if (state.index >= state.items.length) {
        state.items = [];
    }
    return phrase;
}

function size_for(pool_name) {
    if (pool_name === "head") {
        return rng.choices(HEAD_SIZES, HEAD_WEIGHTS);
    }
    return rng.choice(pool_name === "stem" ? [6, 7, 8] : [7, 8, 9, 10]);
}

function color_for(x, y, size, kind, edge=false) {
    if (kind === "head") return rose_color(x, y, size, edge);
    return green_color(x, y, size, edge);
}

function measureTextWidth(text, size) {
    ctx.font = `bold ${size}px Georgia, "Times New Roman", "Malgun Gothic", "Yu Gothic UI", "Microsoft YaHei", "Nirmala UI", Arial, sans-serif`;
    return ctx.measureText(text).width;
}

function build_region(polygons, y_start, y_end, row_h, kind) {
    let placed = [];
    let half = row_h / 2;
    let y = y_start + half;

    while (y < y_end - half) {
        let top = shape_spans(polygons, y - half + 1);
        let bottom = shape_spans(polygons, y + half - 1);
        let row = intersect_spans(top, bottom, kind === "head" ? 19 : 16);

        for (let [lo, hi] of row) {
            let margin = kind === "head" ? 3 : 1;
            lo += margin;
            hi -= margin;
            let available = hi - lo;
            if (available < 18) continue;

            let line = [];
            let cur = lo + rng.uniform(0, Math.min(3, Math.max(1, available * 0.02)));
            while (cur < hi - 15) {
                let remaining = hi - cur;
                let candidates = [];
                let target_width = Math.min(74, Math.max(19, remaining * 0.22));
                let tries = kind === "head" ? 45 : 55;
                for (let t = 0; t < tries; t++) {
                    let size = size_for(kind);
                    let text = phrase_from_pool(kind, size);
                    let width = measureTextWidth(text, size);
                    if (width <= remaining && width >= Math.min(18, remaining * 0.20)) {
                        let score = Math.abs(width - target_width) + rng.uniform(0, 13);
                        candidates.push({ score, text, size, width });
                    }
                }
                if (!candidates.length) break;
                candidates.sort((a, b) => a.score - b.score);
                let top_candidates = candidates.slice(0, Math.min(4, candidates.length));
                let pick = rng.choice(top_candidates);
                line.push({
                    x: cur + pick.width / 2,
                    y: y,
                    text: pick.text,
                    size: pick.size,
                    width: pick.width,
                    kind: kind
                });
                cur += pick.width + (kind === "head" ? GAP : 1);
            }

            if (!line.length) continue;

            let used = line.reduce((acc, item) => acc + item.width, 0) + Math.max(0, line.length - 1) * (kind === "head" ? GAP : 1);
            let slack = Math.max(0, available - used);
            let extra = line.length > 1 ? slack / (line.length - 1) : 0;
            for (let i = 0; i < line.length; i++) {
                let item = line[i];
                item.x += extra * i;
                item.edge = (i === 0 || i === line.length - 1);
                item.color = color_for(item.x, item.y, item.size, kind, item.edge);
                placed.push(item);
            }
        }
        y += row_h;
    }
    return placed;
}

const head_row_h = 16;
const leaf_row_h = 12;
const stem_row_h = 10;

let placed = [];
placed = placed.concat(build_region(HEAD_SHAPES, 88, 540, head_row_h, "head"));
placed = placed.concat(build_region([LEFT_LEAF], 543, 618, leaf_row_h, "leaf"));
placed = placed.concat(build_region([RIGHT_LEAF], 575, 651, leaf_row_h, "leaf"));
placed = placed.concat(build_region([STEM], 492, 773, stem_row_h, "stem"));

let outer = placed.filter(p => p.edge);
let inner = placed.filter(p => !p.edge);
outer.sort((a, b) => (Math.atan2(a.y - 300, a.x - 400) % (2 * Math.PI)) - (Math.atan2(b.y - 300, b.x - 400) % (2 * Math.PI)));
inner.sort(() => rng.nextFloat() - 0.5);

const ORDER = outer.concat(inner);

let active = [];
let all_main_items = [];

ORDER.forEach(p => {
    p.frame = 0;
    p.dx = rng.uniform(-6, 6);
});

let itemsIter = ORDER[Symbol.iterator]();
let rate = ORDER.length / (DURATION * 1000 / TICK);
let acc = 0.0;
let spawning = true;

function spawn(p) {
    all_main_items.push(p);
    active.push(p);
}

function clamp(v) {
    return Math.max(0.0, Math.min(1.0, v));
}

function drawItem(p) {
    let u = clamp(p.frame / ANIM);
    let eased = 1 - Math.pow(1 - u, 3);
    let px = p.x + p.dx * (1 - eased);
    let py = p.y - LIFT * (1 - eased);

    ctx.font = `bold ${p.size}px Georgia, "Times New Roman", "Malgun Gothic", "Yu Gothic UI", "Microsoft YaHei", "Nirmala UI", Arial, sans-serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    // Shadow
    let shadowCol = hx(mix(BGC, [p.color[0] * 0.23, p.color[1] * 0.23, p.color[2] * 0.23], eased));
    ctx.fillStyle = shadowCol;
    ctx.fillText(p.text, px + 1, py + 2);

    // Halo
    let haloCol = hx(mix(BGC, [p.color[0] * 0.30, p.color[1] * 0.30, p.color[2] * 0.30], eased * eased));
    ctx.fillStyle = haloCol;
    ctx.fillText(p.text, px, py);

    // Main text with entrance flash
    let flash = 0.55 * Math.sin(Math.PI * clamp((u - 0.58) / 0.42));
    let mainCol = mix(mix(BGC, p.color, Math.pow(eased, 1.35)), [1.0, 0.83, 0.88], flash);
    ctx.fillStyle = hx(mainCol);
    ctx.fillText(p.text, px, py);

    p.frame++;
    return u < 1;
}

let shimmering = false;
function shimmer() {
    if (all_main_items.length > 0) {
        let pick = all_main_items[Math.floor(Math.random() * all_main_items.length)];
        pick.shimmerUntil = Date.now() + 210;
    }
    setTimeout(shimmer, 145);
}

function step() {
    ctx.fillStyle = BG;
    ctx.fillRect(0, 0, W, H);

    if (spawning) {
        acc += rate;
        while (acc >= 1) {
            acc -= 1;
            let nextVal = itemsIter.next();
            if (!nextVal.done) {
                spawn(nextVal.value);
            } else {
                spawning = false;
                break;
            }
        }
    }

    active = active.filter(p => drawItem(p));

    // Render settled items
    let now = Date.now();
    for (let p of all_main_items) {
        if (p.frame >= ANIM) {
            ctx.font = `bold ${p.size}px Georgia, "Times New Roman", "Malgun Gothic", "Yu Gothic UI", "Microsoft YaHei", "Nirmala UI", Arial, sans-serif`;
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";

            let col = p.color;
            if (p.shimmerUntil && now < p.shimmerUntil) {
                col = mix(p.color, [1.0, 0.82, 0.88], 0.55);
            }

            ctx.fillStyle = hx(mix(BGC, [p.color[0] * 0.23, p.color[1] * 0.23, p.color[2] * 0.23], 1));
            ctx.fillText(p.text, p.x + 1, p.y + 2);

            ctx.fillStyle = hx(mix(BGC, [p.color[0] * 0.30, p.color[1] * 0.30, p.color[2] * 0.30], 1));
            ctx.fillText(p.text, p.x, p.y);

            ctx.fillStyle = hx(col);
            ctx.fillText(p.text, p.x, p.y);
        }
    }

    if (!spawning && active.length === 0 && !shimmering) {
        shimmering = true;
        shimmer();
    }

    setTimeout(step, TICK);
}

setTimeout(step, 200);
</script>
</body>
</html>
"""

components.html(rose_html, height=820)