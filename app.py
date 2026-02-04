# app.py
# Streamlit "5-minutilised" generator (Matemaatika / Eesti keel / Loogika / Emotsionaalne soojendus)
# Run: streamlit run app.py

import random
import textwrap
import streamlit as st
import streamlit.components.v1 as components

# ----------------------------
# UI helpers
# ----------------------------
def hr():
    st.markdown("---")

def wrap(s: str, width: int = 88) -> str:
    return "\n".join(textwrap.fill(line, width=width) for line in s.split("\n"))

def render_copy_button(text: str, label: str = "📋 Kopeeri"):
    """
    Streamlit doesn't have a native clipboard API.
    This uses a tiny HTML+JS snippet to copy 'text' to clipboard.
    """
    safe_text = text.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    html = f"""
    <div style="display:flex; gap:8px; align-items:center;">
      <button id="copyBtn"
        style="
          background:#2b2b2b; color:#f2f2f2; border:1px solid #444;
          padding:8px 12px; border-radius:10px; cursor:pointer; font-weight:600;
        ">{label}</button>
      <span id="copyStatus" style="color:#9aa0a6; font-size:13px;"></span>
    </div>
    <script>
      const text = `{safe_text}`;
      const btn = document.getElementById("copyBtn");
      const status = document.getElementById("copyStatus");
      btn.addEventListener("click", async () => {{
        try {{
          await navigator.clipboard.writeText(text);
          status.textContent = "Kopeeritud!";
          setTimeout(()=>status.textContent="", 1500);
        }} catch (e) {{
          status.textContent = "Ei saanud kopeerida (brauseri piirang).";
          setTimeout(()=>status.textContent="", 2500);
        }}
      }});
    </script>
    """
    components.html(html, height=60)

# ----------------------------
# Template banks
# Each template is a dict:
#  title, teacher_phrase, task, harder
# Placeholders allowed: {a},{b},{c},{word},{word2},{verb},{noun},{adj}
# ----------------------------

VOCAB = {
    1: {
        "nouns": ["koolikott", "pliiats", "vihik", "kumm", "raamat", "aken", "uks", "tool", "laud", "kell"],
        "verbs": ["jookseb", "loeb", "kirjutab", "istub", "seisab", "naerab", "kuulab", "vaatab"],
        "adjs":  ["suur", "väike", "kiire", "aeglane", "ilus", "uus", "vana"],
    },
    2: {
        "nouns": ["sõber", "õpetaja", "klass", "vahetund", "pliiatsikarp", "joonlaud", "vihmavari", "jalgratas"],
        "verbs": ["mängib", "õpib", "joonistab", "räägib", "külastab", "koristab", "aitab"],
        "adjs":  ["tark", "lahke", "huvitav", "rahulik", "lõbus", "töökas"],
    },
    3: {
        "nouns": ["kodutöö", "reegel", "lause", "küsimus", "vastus", "lugu", "tähendus", "näide"],
        "verbs": ["selgitab", "võrdleb", "otsustab", "kontrollib", "parandab", "arutleb", "kirjeldab"],
        "adjs":  ["täpne", "oluline", "keeruline", "lihtne", "selge", "segane"],
    },
    4: {
        "nouns": ["kokkuvõte", "põhjus", "tagajärg", "arvamus", "tõend", "võimalus", "lahendus"],
        "verbs": ["põhjendab", "järeldab", "analüüsib", "võtab kokku", "esitab", "toetab"],
        "adjs":  ["loogiline", "usutav", "veenev", "ebaselge", "tähelepanelik"],
    },
}

TEMPLATES = {
    "Matemaatika": [
        {
            "title": "Kiire lahutamine",
            "teacher_phrase": "Räägime täislausega: ‘Järele jääb …’",
            "task": "Mul on {a} kommi. Annan ära {b}. Mitu jääb alles?",
            "harder": "Kui annan ära veel {c}, mitu jääb kokku alles?",
        },
        {
            "title": "Võrdlemine",
            "teacher_phrase": "Kasuta sõnu: rohkem / vähem / sama palju.",
            "task": "Võrdle: {a} ja {b}. Kumb on suurem? Ütle täislausega.",
            "harder": "Leia arv, mis on {a}-st 2 võrra suurem.",
        },
        {
            "title": "Liitmise mõte",
            "teacher_phrase": "Küsimus: ‘Kui palju kokku?’",
            "task": "Karbis on {a} pliiatsit ja laual {b}. Kui palju kokku?",
            "harder": "Mitu oleks kokku, kui lisame veel {c}?",
        },
        {
            "title": "Puuduv liige",
            "teacher_phrase": "Mõtle: mis lisandub, et saada kokku?",
            "task": "{a} + __ = {b}. Leia puuduv arv.",
            "harder": "Tee ise üks samasugune ülesanne ja vaheta naabriga.",
        },
        {
            "title": "Kiirusemäng (vaikselt)",
            "teacher_phrase": "Mõtle vaikselt, näita sõrmedega vastust.",
            "task": "Arvuta: {a} + {b} = ?",
            "harder": "Arvuta: {a} + {b} + {c} = ?",
        },
    ],

    "Loogika": [
        {
            "title": "Järjend",
            "teacher_phrase": "Ütle reegel: mis muutub iga sammuga?",
            "task": "Jätka rida: {a}, {b}, {c}, __",
            "harder": "Mõtle ise üks rida ja ütle reegel.",
        },
        {
            "title": "Klassifitseeri",
            "teacher_phrase": "Nimeta tunnus, mille järgi rühmitad.",
            "task": "Rühmita: {word}, {word2}, {noun}, {adj}. (nt ‘asjad’ vs ‘omadused’)",
            "harder": "Lisa 2 oma sõna õigesse rühma.",
        },
        {
            "title": "Mis on puudu?",
            "teacher_phrase": "Otsi mustrit (kuju, arv, sõna).",
            "task": "Muster: ▲ ● ▲ ● __  Mis tuleb järgmiseks?",
            "harder": "Tee oma muster 6 sümboliga.",
        },
        {
            "title": "Tõene / väär",
            "teacher_phrase": "Põhjenda ühe lausega.",
            "task": "Väide: ‘Kui {a} > {b}, siis {b} < {a}.’ Tõene või väär?",
            "harder": "Tee ise üks väide ja lase klassil otsustada.",
        },
    ],

    "Emotsionaalne soojendus": [
        {
            "title": "Ilmateade seestpoolt",
            "teacher_phrase": "Me ei naera kellegi tunde üle. Me märkame.",
            "task": "Vali: täna on minu sees **päike / pilv / vihm / tuul**. Ütle üks sõna.",
            "harder": "Ütle üks lause: ‘Täna ma tunnen …, sest …’",
        },
        {
            "title": "1 heategu (mikro)",
            "teacher_phrase": "Üks väike asi teeb klassi paremaks.",
            "task": "Ütle naabrile üks lahke fraas (nt ‘Aitäh’, ‘Tubli!’).",
            "harder": "Ütle sama fraas teisele inimesele uue põhjusega.",
        },
        {
            "title": "3 asja, mida märkan",
            "teacher_phrase": "Harjutame tähelepanu, mitte kiirust.",
            "task": "Vaata ringi ja ütle vaikselt 3 asja, mida märkad.",
            "harder": "Ütle üks neist täislausega: ‘Ma märkan …’",
        },
        {
            "title": "Hingamine 4–2–4",
            "teacher_phrase": "Teeme koos: aeglaselt ja rahulikult.",
            "task": "Hinga sisse 4, hoia 2, hinga välja 4 (2 korda).",
            "harder": "Lisa õlgade lõdvestus: ‘lase õlad alla’ väljahingamisel.",
        },
    ],
}

# ----------------------------
# Generation logic
# ----------------------------
def pick_vocab(grade: int):
    pool = VOCAB[grade]
    noun = random.choice(pool["nouns"])
    verb = random.choice(pool["verbs"])
    adj = random.choice(pool["adjs"])
    word = random.choice(pool["nouns"] + pool["adjs"] + pool["verbs"])
    word2 = random.choice(pool["nouns"] + pool["adjs"] + pool["verbs"])

    for _ in range(5):
        if word2 != word:
            break
        word2 = random.choice(pool["nouns"] + pool["adjs"] + pool["verbs"])

    return noun, verb, adj, word, word2

def generate_block(grade: int, subject: str, level: str, minutes: int) -> dict:
    templates_src = TEMPLATES
    tpl = random.choice(templates_src[subject])


    # numbers tuned by grade
    if grade == 1:
        a = random.randint(3, 10)
        b = random.randint(1, min(6, a))
        c = random.randint(1, 4)
    elif grade == 2:
        a = random.randint(6, 20)
        b = random.randint(2, 10)
        c = random.randint(1, 8)
    elif grade == 3:
        a = random.randint(10, 50)
        b = random.randint(5, 30)
        c = random.randint(2, 20)
    else:
        a = random.randint(20, 100)
        b = random.randint(10, 80)
        c = random.randint(5, 50)

    noun, verb, adj, word, word2 = pick_vocab(grade)

    data = {
        "a": a, "b": b, "c": c,
        "noun": noun, "verb": verb, "adj": adj,
        "word": word, "word2": word2,
    }

    title = tpl["title"]
    teacher = tpl["teacher_phrase"]
    task = tpl["task"].format(**data)
    harder = tpl["harder"].format(**data)
    # L2: fix teacher question based on subject kind (Kes vs Mis)
    if subject == "Eesti keel" and lang_mode == "Eesti keel (L2 – lihtsustatud)":
        if teacher.strip() == "Küsimus: Kes teeb?" and subject_kind == "object":
            teacher = "Küsimus: Mis teeb?"

    # For "level", adjust: if basic, keep "harder" optional; if harder, emphasize it.
    if level == "Baas":
        harder_label = "➕ (Valik) Raskem"
    else:
        harder_label = "🔥 Raskem"

    return {
        "title": title,
        "teacher": teacher,
        "task": task,
        "harder_label": harder_label,
        "harder": harder,
        "minutes": minutes,
        "subject": subject,
        "grade": grade,
    }

def format_for_copy(block: dict) -> str:
    s = f"""5-minutiline: {block['title']}
Klass: {block['grade']}  |  Aine: {block['subject']}  |  Aeg: ~{block['minutes']} min

Õpetajale (fraas):
- {block['teacher']}

Ülesanne:
- {block['task']}

{block['harder_label']}:
- {block['harder']}
"""
    return wrap(s, 92)

# ----------------------------
# App
# ----------------------------
st.set_page_config(
    page_title="5-minutilised (algklass)",
    page_icon="⏱️",
    layout="centered",
)

st.title("⏱️ 5-minutiliste harjutuste generaator (1–4 klass)")
st.caption("Matemaatika • Eesti keel • Loogika • Emotsionaalne soojendus — kiireks tunnialguseks või vahepausiks.")

# Sidebar controls
with st.sidebar:
    st.header("Seaded")
    grade = st.selectbox("Klass", [1, 2, 3, 4], index=1)
    subject = st.selectbox("Aine", ["Matemaatika", "Loogika", "Emotsionaalne soojendus"], index=0)
    level = st.radio("Tase", ["Baas", "Raskem"], horizontal=True, index=0)
    minutes = st.select_slider("Kestus", options=[3, 5, 7], value=5)
    seed = st.text_input("Seed (valikuline)", value="", help="Kui sisestad numbri, saad korratavaid tulemusi.")
    if seed.strip():
        try:
            random.seed(int(seed.strip()))
        except:
            st.warning("Seed peab olema number. Jätkan ilma seed'ita.")

if "block" not in st.session_state:
    st.session_state.block = generate_block(grade, subject, level, minutes)

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("🎲 Genereeri", use_container_width=True):
        st.session_state.block = generate_block(grade, subject, level, minutes)
with col2:
    if st.button("🔁 Veel üks", use_container_width=True):
        st.session_state.block = generate_block(grade, subject, level, minutes)
with col3:
    st.write("")  # spacer

hr()

block = st.session_state.block

# If user changed settings, regenerate automatically to match
if (block["grade"], block["subject"], block["minutes"]) != (grade, subject, minutes):
    st.session_state.block = generate_block(grade, subject, level, minutes)
    block = st.session_state.block

st.subheader(f"🧩 {block['title']}")
subject_label = block["subject"]
if block["subject"] == "Eesti keel" and lang_mode == "Eesti keel (L2 – lihtsustatud)":
    subject_label = "Eesti keel (L2)"

st.write(
    f"**Klass:** {block['grade']}  |  "
    f"**Aine:** {subject_label}  |  "
    f"**Aeg:** ~{block['minutes']} min"
)


st.markdown("**Õpetajale (fraas):**")
st.info(block["teacher"])

st.markdown("**Ülesanne:**")
st.success(block["task"])

st.markdown(f"**{block['harder_label']}:**")
st.warning(block["harder"])

hr()

copy_text = format_for_copy(block)
st.markdown("**Kopeerimiseks / tunnikavasse:**")
st.text_area(
    "Kopeerimise tekst",
    value=copy_text,
    height=220,
    label_visibility="collapsed"
)


render_copy_button(copy_text, label="📋 Kopeeri tekst lõikelauale")

hr()

st.download_button(
    "⬇️ Laadi alla .txt",
    data=copy_text.encode("utf-8"),
    file_name=f"5-minutiline_{block['subject'].replace(' ', '_')}_klass{block['grade']}.txt",
    mime="text/plain; charset=utf-8",
)

st.caption("Nipp: kui tahad hiljem lisada PDF/Docx, saab selle sama tekstiploki põhjal automaatselt koostada.")
