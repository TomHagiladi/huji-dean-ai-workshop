# -*- coding: utf-8 -*-
"""Generates the workshop platform: index.html (home) + station-1..6.html into site/.
Re-run after any edit. Content lives here; layout is one template."""
import io, os

OUT = os.path.dirname(os.path.abspath(__file__))  # the repo root: pages are written next to this script
URL = "tomhagiladi.github.io/huji-dean-ai-workshop"

CSS = r"""
:root{
  --primary:#5E9A28; --primary-text:#3F6E1C; --primary-bright:#75B743;
  --primary-container:#EDF5E4; --surface:#FFFFFF; --surface-2:#F6F9F2;
  --outline:#C9D6BC; --outline-dim:#DCE5D0; --on-surface:#4A4845; --on-surface-muted:#66645F;
  --tertiary:#AF242A; --tertiary-container:#FBECEC; --anchor:#3F6E1C; --anchor-hover:#345c17;
  --font-display:'Heebo','Noto Sans Hebrew',Arial,sans-serif; --font-body:'Noto Sans Hebrew','Heebo',Arial,sans-serif;
  --r-sm:12px; --r-md:18px; --r-lg:26px; --ease:cubic-bezier(.2,0,0,1);
  --fs-body:clamp(18px,1.05vw + 11px,24px);
  --fs-lead:clamp(20px,1.25vw + 12px,28px);
  --fs-h1:clamp(34px,2.6vw + 16px,64px);
  --fs-h2:clamp(28px,2vw + 12px,48px);
  --fs-h3:clamp(22px,1.4vw + 10px,32px);
}
body.st{--fs-body:clamp(20px,1.35vw + 12px,30px);--fs-lead:clamp(22px,1.6vw + 13px,34px);--fs-h1:clamp(38px,3vw + 18px,72px);--fs-h3:clamp(24px,1.7vw + 11px,38px)}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--font-body);color:var(--on-surface);background:var(--surface-2);font-size:var(--fs-body);line-height:1.65;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:var(--font-display);line-height:1.2}
p{margin:0 0 .8em}
a{color:var(--primary-text)}
.en{direction:ltr;unicode-bidi:isolate;font-family:var(--font-display);font-weight:500}
.wrap{max-width:min(1720px,94vw);margin:0 auto;padding:0 20px}
.c{text-align:center}

/* accessibility */
.skip-link{position:absolute;top:-100%;right:0;background:var(--tertiary);color:#fff;padding:.75rem 1.5rem;font-weight:700;z-index:200;text-decoration:none}
.skip-link:focus{top:0;outline:3px solid #1F1E1C;outline-offset:2px}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
a:focus-visible,button:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--tertiary);outline-offset:3px;border-radius:8px}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}

/* header (home) */
.hero{background:var(--surface);border-bottom:1px solid var(--outline-dim);padding:34px 0 26px;text-align:center}
.hero .logo{height:clamp(70px,6vw,120px);width:auto;display:block;margin:0 auto 18px}
.hero h1{font-size:var(--fs-h1);font-weight:800;margin-bottom:6px}
.hero .sub{font-size:var(--fs-lead);color:var(--on-surface-muted);margin:0}
.join{display:none;flex-direction:column;align-items:center;gap:14px;background:var(--primary-container);border:1px solid var(--outline);border-radius:var(--r-lg);padding:28px 30px;margin:26px auto 0;max-width:820px}
.join img{width:clamp(220px,18vw,320px);height:auto;border-radius:var(--r-sm);background:#fff;padding:10px;border:1px solid var(--outline)}
.join .t{font-family:var(--font-display);font-weight:800;font-size:var(--fs-h3);margin:0}
.join .u{font-size:var(--fs-body);color:var(--on-surface-muted);margin:0}
@media (min-width:900px){.join{display:flex}}

/* tools (buttons) */
.tools{margin:34px 0 10px;text-align:center}
.tools h2{font-size:var(--fs-h2);font-weight:800;margin-bottom:18px}
.tools ul{list-style:none;display:grid;grid-template-columns:repeat(5,1fr);gap:18px;max-width:1560px;margin:0 auto}
@media (max-width:1100px){.tools ul{grid-template-columns:repeat(2,1fr)}}
@media (max-width:600px){.tools ul{grid-template-columns:1fr}}
.tool{display:flex;flex-direction:column;align-items:center;justify-content:flex-start;gap:8px;height:100%;min-height:170px;padding:20px 22px;
  border-radius:var(--r-md);background:linear-gradient(180deg,#fff,var(--primary-container));border:2px solid var(--primary);color:var(--on-surface);text-decoration:none;
  box-shadow:0 3px 0 var(--primary),0 8px 18px rgba(74,72,69,.10);transition:transform .2s var(--ease),box-shadow .2s var(--ease)}
.tool:hover{transform:translateY(-2px);box-shadow:0 5px 0 var(--primary),0 12px 24px rgba(74,72,69,.14)}
.tool:active{transform:translateY(1px);box-shadow:0 1px 0 var(--primary)}
.tool .nm{font-family:var(--font-display);font-weight:800;font-size:var(--fs-h3)}
.tool .ln{font-size:calc(var(--fs-body) * .8);color:var(--on-surface-muted);line-height:1.4}
.tool .nm svg{width:.8em;height:.8em;vertical-align:-.05em;margin-right:6px;color:var(--primary-text)}

/* cards */
.card{background:var(--surface);border:1px solid var(--outline-dim);border-radius:var(--r-lg);padding:30px 34px;margin:26px 0}
.card.tone{background:var(--primary-container);border-color:var(--outline)}
.card.warn{border-right:8px solid var(--tertiary);background:var(--tertiary-container)}
.card h2{font-size:var(--fs-h2);font-weight:800;margin-bottom:12px}
.lead{font-size:var(--fs-lead)}
.callout{border-right:6px solid var(--primary-bright);background:var(--surface-2);border-radius:var(--r-sm);padding:18px 22px;margin:20px 0}
.callout b{color:var(--primary-text)}
ol.steps{padding-right:34px;margin:12px 0} ol.steps li{margin:10px 0;padding-right:8px}
ul.tips{padding-right:30px;margin:12px 0} ul.tips li{margin:10px 0}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media (max-width:900px){.grid2{grid-template-columns:1fr}}

/* route (home) */
.route{margin:40px 0 10px;scroll-margin-top:16px}
.route h2{font-size:var(--fs-h2);font-weight:800;text-align:center;margin-bottom:8px}
.route .hint{text-align:center;color:var(--on-surface-muted);font-size:var(--fs-lead);margin-bottom:24px}
.stcard{display:flex;align-items:center;gap:24px;background:var(--surface);border:2px solid var(--outline);border-radius:var(--r-lg);padding:26px 30px;text-decoration:none;color:var(--on-surface);
  transition:transform .2s var(--ease),box-shadow .2s var(--ease);box-shadow:0 4px 14px rgba(74,72,69,.06);min-height:120px}
.stcard:hover{transform:translateY(-3px);box-shadow:0 12px 28px rgba(74,72,69,.14)}
.stcard .n{width:clamp(60px,5vw,84px);height:clamp(60px,5vw,84px);border-radius:50%;border:4px solid var(--primary);display:grid;place-items:center;font-family:var(--font-display);font-weight:800;font-size:var(--fs-h3);color:var(--primary-text);background:#fff;flex:none}
.stcard .tt{flex:1}
.stcard h3{font-size:var(--fs-h3);font-weight:800;margin-bottom:4px}
.stcard .what{color:var(--on-surface-muted);margin:0;font-size:var(--fs-body)}
.stcard .go{flex:none;width:52px;height:52px;border-radius:50%;background:var(--primary-container);display:grid;place-items:center;color:var(--primary-text)}
.stcard .go svg{width:26px;height:26px}
.stcard.anchor{background:var(--anchor);border-color:var(--anchor);color:#fff;flex-direction:column;text-align:center;align-items:center;gap:12px;padding:36px 30px}
.stcard.anchor .n{background:#fff;border-color:#fff;color:var(--anchor)}
.stcard.anchor .what{color:rgba(255,255,255,.9)}
.stcard.anchor .go{background:rgba(255,255,255,.18);color:#fff}
.stcard.anchor .tag{display:inline-block;background:#fff;color:var(--anchor);border-radius:999px;padding:4px 16px;font-family:var(--font-display);font-weight:800;font-size:calc(var(--fs-body) * .85);margin-bottom:8px}
.optional{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin:18px 0}
@media (max-width:900px){.optional{grid-template-columns:1fr}}
.group-title{display:flex;align-items:center;gap:16px;margin:26px 0 6px}
.group-title h3{font-size:var(--fs-h3);font-weight:800;color:var(--on-surface-muted);white-space:nowrap}
.group-title:before,.group-title:after{content:"";flex:1;height:3px;background:var(--outline-dim)}

/* station pages */
.topbar{background:var(--surface);border-bottom:1px solid var(--outline-dim);position:sticky;top:0;z-index:50}
.topbar .row{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 0;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:10px;min-height:52px;padding:0 22px;border-radius:999px;border:2px solid var(--primary);background:var(--primary-container);color:var(--on-surface);
  font-family:var(--font-display);font-weight:800;font-size:var(--fs-body);text-decoration:none;cursor:pointer;transition:background .2s var(--ease),transform .2s var(--ease)}
.btn:hover{background:#E1EFD3;transform:translateY(-1px)}
.btn svg{width:22px;height:22px;flex:none}
.btn.primary{background:var(--anchor);border-color:var(--anchor);color:#fff}
.btn.primary:hover{background:var(--anchor-hover)}
.stepper{list-style:none;display:flex;align-items:center;gap:8px}
.stepper a{width:48px;height:48px;border-radius:50%;border:3px solid var(--primary);background:#fff;display:grid;place-items:center;font-family:var(--font-display);font-weight:800;font-size:18px;color:var(--primary-text);text-decoration:none}
.stepper a.big{border-color:var(--anchor);background:var(--anchor);color:#fff}
.stepper a[aria-current]{background:var(--primary-bright);color:#fff;transform:scale(1.12)}
.stepper a.big[aria-current]{background:var(--anchor)}
.stepper .ln{width:14px;height:4px;background:var(--primary-bright)}
.minitools{list-style:none;display:flex;gap:8px;flex-wrap:wrap}
.minitools a{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border-radius:999px;border:1.5px solid var(--primary);background:var(--surface);color:var(--on-surface);text-decoration:none;font-weight:700;font-size:calc(var(--fs-body) * .82)}
.minitools a:hover{background:var(--primary-container)}
.station-hero{padding:30px 0 6px}
.station-hero .head{display:flex;align-items:center;gap:22px;margin-bottom:8px}
.station-hero .n{width:clamp(64px,5.5vw,92px);height:clamp(64px,5.5vw,92px);border-radius:50%;border:4px solid var(--primary);display:grid;place-items:center;font-family:var(--font-display);font-weight:800;font-size:var(--fs-h2);color:var(--primary-text);background:#fff;flex:none}
.station-hero.anchor .n{background:var(--anchor);border-color:var(--anchor);color:#fff}
.station-hero h1{font-size:var(--fs-h1);font-weight:800}
.banner{display:inline-flex;align-items:center;gap:10px;background:var(--anchor);color:#fff;border-radius:999px;padding:10px 22px;font-family:var(--font-display);font-weight:800;font-size:var(--fs-lead);margin:0 0 14px}
.banner svg{width:24px;height:24px}
.prompt{background:var(--surface);border:2px solid var(--outline);border-radius:var(--r-md);padding:20px 24px 16px;margin:18px 0}
.prompt .lb{display:flex;align-items:center;justify-content:space-between;gap:14px;margin-bottom:10px;flex-wrap:wrap}
.prompt .lb b{font-family:var(--font-display);font-size:var(--fs-h3);color:var(--primary-text)}
.prompt pre{white-space:pre-wrap;word-wrap:break-word;font-family:var(--font-body);font-size:var(--fs-body);line-height:1.7;margin:0}
.prompt .hint{font-size:calc(var(--fs-body) * .85);color:var(--on-surface-muted);margin:12px 0 0}
.copy{display:inline-flex;align-items:center;gap:10px;min-height:52px;padding:0 22px;border-radius:999px;border:2px solid var(--primary);background:var(--primary-container);color:var(--on-surface);font-family:var(--font-display);font-weight:800;font-size:var(--fs-body);cursor:pointer;transition:background .2s var(--ease),transform .2s var(--ease);flex:none}
.copy:hover{background:#E1EFD3}
.copy:active{transform:scale(.97)}
.copy.done{background:var(--anchor);border-color:var(--anchor);color:#fff}
.copy svg{width:22px;height:22px;flex:none}
.pagenav{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;margin:40px 0 20px}

/* tables */
table{border-collapse:collapse;width:100%;font-size:var(--fs-body);margin:12px 0}
th{background:var(--primary-container);text-align:right;padding:12px 14px;border:1px solid var(--outline-dim);font-weight:700}
td{padding:12px 14px;border:1px solid var(--outline-dim);vertical-align:top}
.table-scroll-wrapper{width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;margin:1rem 0;border-radius:8px}

footer{border-top:1px solid var(--outline-dim);background:var(--surface);padding:34px 0 44px;font-size:calc(var(--fs-body) * .85);color:var(--on-surface-muted);text-align:center;margin-top:40px}
.accessibility-statement{background:var(--surface-2);border:1px solid var(--outline-dim);border-radius:10px;padding:1.5rem 2rem;margin:1.5rem auto 0;max-width:820px;text-align:right}
.accessibility-statement h3{font-size:var(--fs-h3);margin-bottom:8px;color:var(--on-surface)}
"""

COPY_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>'
ARROW_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M19 12H5M12 5l-7 7 7 7"/></svg>'
HOME_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M3 11l9-8 9 8v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></svg>'
EXT_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M19 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h5"/></svg>'
CHECK_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M5 12l5 5L20 7"/></svg>'
START_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'

TOOLS = [
    ("Claude", "https://claude.ai", "claude.ai", "הכי חזק בכתיבה ובניתוח מסמכים ארוכים, ובשיחה שמחזיקה הקשר לאורך זמן"),
    ("Gemini", "https://gemini.google.com", "gemini.google.com", "מחובר לגוגל דרייב; כאן בונים Gem, וכאן יש Canvas לוויב קודינג"),
    ("ChatGPT", "https://chatgpt.com", "chatgpt.com", "הכי מוכר, הממשק הכי פשוט, טוב בכל תחום"),
    ("Grok", "https://grok.com", "grok.com", "הכי פחות פוליטיקלי קורקט, ברוח אילון מאסק - עונה ישיר גם כשלא נעים"),
    ("Gemini Notebook", "https://notebook.google.com", "notebook.google.com", "לשעבר NotebookLM. עונה רק מהמקורות שהזנתם; כאן בונים מחברת"),
]

STATIONS = [
    # (num, slug, title, what, anchor_kind)
    (1, "station-1", "ממשיכים את היעדים מאתמול", "ההקשר של היחידה, שיחה מתמשכת, ותוצר בכמה צורות", "start"),
    (2, "station-2", "מחברת Gemini Notebook עם חומרי הדיקנט", "מחברת שעונה רק מהנהלים שלכם - ואז פודקאסט, מפת חשיבה וסרטון", None),
    (3, "station-3", "בונים Gem בג'מיני", "מומחה שמור - בוט זכויות הסטודנט - בעשר דקות", None),
    (4, "station-4", "פרומפטים לקשב", "חמש הטכניקות מהמצגת, כתובות כמו שסטודנט אמיתי היה כותב", None),
    (5, "station-5", "וויב קודינג בג'מיני", "אפליקציה קטנה ליחידה - בלי לדעת לתכנת", None),
    (6, "station-6", "ואיך זה נראה אצלנו", "שיחה בזוג, ומשפט אחד של היחידה שנאמר בקול", "end"),
]

def prompt(label, text, hint=None, aria=None):
    a = aria or ("העתק את " + label)
    h = f'<p class="hint">{hint}</p>' if hint else ''
    return (f'<div class="prompt"><div class="lb"><b>{label}</b>'
            f'<button class="copy" type="button" aria-label="{a}">{COPY_SVG}<span>העתק</span></button></div>'
            f'<pre>{text}</pre>{h}</div>')

BASIS = "בסיס לעריכה - שנו, קצרו, הוסיפו."

BODY = {}

BODY[1] = f'''
<p class="lead">לוקחים את המטרות שנוסחו אתמול, נותנים למודל את ההקשר המלא של היחידה, ומנהלים איתו שיחה - לא שאלה אחת.</p>
<div class="callout"><b>לפני שמעתיקים:</b> הפרומפט הוא בסיס לעריכה ולדיוק. לא חייבים להעתיק אותו כמו שהוא, ואף מומלץ שלא - שנו, קצרו, הוסיפו. גם סדר פרומפטי ההמשך לא מחייב: עדיף לזרום עם השיחה ולשלב אותם כשרואים לנכון.</div>
{prompt("תבנית ההקשר", """אני [תפקיד] ביחידת [שם היחידה] בדיקנט הסטודנטים של האוניברסיטה העברית.
היחידה שלנו אחראית על [תיאור של שתיים-שלוש שורות: מה עושים, למי, בכמה סטודנטים מדובר].
אתמול, ביום היעדים של הריטריט, ניסחנו את המטרות הבאות לשנה הקרובה:
[הדביקו כאן את המטרות כפי שנכתבו]
האילוצים שלנו: [תקנים, תקציב, לוח זמנים, מערכות מידע קיימות].
מה שכבר ניסינו בעבר ולא עבד: [אם יש].
אני רוצה שתעזור לי להפוך את המטרות האלה לטיוטת תוכנית עבודה עם שלבים, אחראים ולוחות זמנים.
לפני שאתה כותב משהו - שאל אותי שלוש שאלות הבהרה שיעזרו לך להבין את ההקשר טוב יותר, וחכה לתשובות שלי.""", BASIS)}
{prompt("המשך - עורך הדין של השטן", "עכשיו תהיה עורך הדין של השטן. מה בתוכנית הזו ייכשל, ולמה? התייחס לכל שלב בנפרד.")}
{prompt("המשך - מה לא שאלתי", "מה אני לא שואל אותך, שהייתי צריך לשאול?")}
{prompt("המשך - השוואה לעולם", "איך אוניברסיטאות מובילות בעולם מטפלות באותו אתגר בדיוק? תן לי שלוש דוגמאות קונקרטיות עם מקורות, ומה מהן אפשר לאמץ אצלנו בהתאמה.",
        '<b>המלצה חמה:</b> כאן הפעילו את מצב המחקר העמוק (<span class="en">Deep Research</span>) של הכלי שבחרתם. הוא מריץ עשרות חיפושים, קורא מאות מקורות, ומחזיר דוח מובנה תוך דקות.')}
{prompt("המשך - להוציא תוצר", "סכם את כל מה שהגענו אליו בשיחה. תן לי את זה בארבע צורות: כטקסט רציף, כטבלה של שלבים-אחראים-לוחות זמנים, כרשימת נקודות קצרה למייל להנהלה, וכתרשים זרימה. נתחיל מהטבלה.")}
<div class="callout"><b>שאלה לזוג:</b> מה בתוכנית שקיבלתם הפתיע אתכם? במה נחלקתם ביניכם, ומה אמר המודל על המחלוקת?</div>
<div class="callout"><b>סיימתם?</b> הכפתור למעלה מחזיר לבחירת תחנה - כל זוג לפי המסלול והקצב שלו.</div>
'''

BODY[2] = f'''
<p class="lead">בונים מחברת שעונה רק מהנהלים שלכם - ואז נותנים לה להפוך אותם לפודקאסט, למפת חשיבה ולסרטון. המחברת הזו תשמש בתחנה 3 כמקור ל-Gem.</p>
<ol class="steps">
<li>נכנסים ל-<a href="https://notebook.google.com" target="_blank" rel="noopener"><span class="en">notebook.google.com</span></a></li>
<li>לוחצים <span class="en">Create new notebook</span></li>
<li>בוחרים <span class="en">Upload a source</span> - קבצי PDF, מסמכי וורד, כתובות אתר, סרטוני יוטיוב, קבצי אודיו</li>
<li>מזינים לפחות שלושה מקורות: עמודי הנהלים הפומביים מאתר הדיקנט. מוצאים אותם בעצמכם - זה חלק מההתנסות</li>
<li>בחלונית הצ'אט שואלים שלוש שאלות אמיתיות, ובודקים שכל תשובה מגיעה עם הפניה ממוספרת למקור</li>
<li>בחלונית ה-<span class="en">Studio</span> מייצרים <span class="en">Audio Overview</span>, <span class="en">Mind Map</span>, ואם יש זמן <span class="en">Video Overview</span></li>
</ol>
{prompt("שלוש שאלות לדוגמה", """1. סטודנט במילואים פספס מועד הגשה. מה מגיע לו, ולפי איזה סעיף?
2. הכן לי רשימה של עשר השאלות הנפוצות ביותר שסטודנט חדש ישאל על הנהלים האלה, עם תשובה קצרה לכל אחת.
3. אילו זכויות מופיעות בתקנון אבל כמעט לא מוזכרות בטפסים?""")}
<div class="callout"><b>שאלה לזוג:</b> הקשיבו לדקה מהפודקאסט. למי ביחידה, או לאילו סטודנטים, זה היה חוסך זמן אמיתי?</div>
'''

BODY[3] = f'''
<p class="lead">בונים "מומחה שמור" - בוט זכויות הסטודנט. מי שבנה מחברת בתחנה 2 יכול לצרף אותה כידע ל-Gem בלחיצה אחת.</p>
<ol class="steps">
<li>נכנסים ל-<a href="https://gemini.google.com" target="_blank" rel="noopener"><span class="en">gemini.google.com</span></a></li>
<li>פותחים את סרגל הצד (<span class="en">Open Sidebar</span>) ולוחצים <span class="en">Gems</span></li>
<li>לוחצים <span class="en">New Gem</span></li>
<li>נותנים שם, ומדביקים את ההוראות (התבנית למטה - בסיס לעריכה)</li>
<li>תחת <span class="en">Knowledge</span> לוחצים <span class="en">Add files</span> - מהמחשב, מהדרייב, או <span class="en">More uploads</span> ואז <span class="en">Notebooks</span> כדי לצרף את המחברת מתחנה 2</li>
<li>לוחצים <span class="en">Save</span>. ה-Gem מופיע תחת <span class="en">My Gems</span></li>
</ol>
<p>גוגל ממליצה על ארבעה רכיבים בהוראות - פרסונה, משימה, הקשר, פורמט - ומציעה כפתור שמרחיב שתי שורות להוראות מלאות. התבנית בנויה כך:</p>
{prompt("הוראות ה-Gem - בוט זכויות הסטודנט", """פרסונה: את/ה עוזר/ת מומחה/ית לזכויות הסטודנט בדיקנט הסטודנטים של האוניברסיטה העברית. הטון ענייני, אדיב ומדויק.

משימה: לענות על שאלות של אנשי צוות הדיקנט בנוגע לזכויות, זכאויות, התאמות ונהלים - על בסיס המסמכים שצורפו בלבד.

הקשר: המשתמשים הם רכזים ומנהלים ביחידות הדיקנט, לא סטודנטים. המסמכים שצורפו הם: תקנון זכויות הסטודנט, נהלי ועדות חריגים, התאמות למשרתי מילואים ולהורים, זכאות למלגות, ולוחות זמנים לערעורים.

פורמט: תשובה קצרה בעברית, ומיד אחריה הפניה לסעיף המדויק במסמך שממנו נלקחה. אם התשובה לא נמצאת במסמכים - אמור/י זאת במפורש, אל תנחש/י, והפנה/י לרכז/ת הרלוונטי/ת.""", "בסיס לעריכה - התאימו את רשימת המסמכים למה שבאמת צירפתם.")}
<div class="callout"><b>מבחן:</b> שלוש שאלות אמיתיות שרכזים שואלים כל שבוע. האם הוא הפנה לסעיף? האם הודה כשלא ידע?</div>
<div class="callout"><b>שאלה לזוג:</b> אם היה לכם Gem כזה ביחידה - מה היה משתנה ביום העבודה של רכז חדש?</div>
'''

BODY[4] = f'''
<p class="lead">מנסים על עצמכם את הטכניקות מהמצגת. הפרומפטים מלאים - עם הקשר אמיתי - כדי שתראו מה המודל באמת מחזיר. החליפו את הפרטים בשלכם.</p>
{prompt("1 - פורס הגבינה", """אני סטודנטית שנה ב' לפסיכולוגיה. יש לי עבודה סמינריונית של עשרה עמודים על השפעת שינה על זיכרון עבודה, להגשה בעוד שנים עשר ימים. יש לי הפרעת קשב מאובחנת, וכבר שבוע אני לא מצליחה להתחיל - כל פעם שאני פותחת את המסמך אני נתקעת וסוגרת. קראתי כבר שלושה מאמרים ויש לי הערות מבולגנות בגוגל דוקס.
פרק לי את כל העבודה לצעדים הכי קטנים שאפשר, כך שאף צעד לא ייקח יותר מחמש עשרה דקות. סדר אותם ברשימה כרונולוגית עם תיבות סימון, וכתוב ליד כל צעד מה נחשב "סיימתי". התחל מהצעד הכי קל שאני יכולה לעשות ממש עכשיו, בשתי הדקות הקרובות.""")}
{prompt("2 - לוח זמנים הפוך", """אני צריך להגיע מחר לבחינה בקמפוס הר הצופים בשמונה וחצי בבוקר. אני גר בגבעת שאול, הנסיעה באוטובוס לוקחת כארבעים דקות ואני תמיד מפספס את האוטובוס. לפני שאני יוצא אני צריך: להתקלח, לאכול משהו, לארגן תיק עם הציוד לבחינה, ולמצוא את אישור ההתאמות שלי שאני לא זוכר איפה שמתי. יש לי הפרעת קשב ואני מוסח בקלות, במיוחד בבוקר.
בנה לי לוח זמנים הפוך שמתחיל בשמונה וחצי ועובד אחורה. כלול חמש דקות באפר בין כל שתי משימות, ועוד עשר דקות באפר לפני היציאה. תגיד לי בדיוק באיזו שעה להתעורר, ובאיזו שעה לחפש את האישור - כי זה הדבר שהכי סביר שייקח יותר זמן ממה שאני חושב.""")}
{prompt("3 - הקאת מוח", """הנה כל מה שעובר לי בראש עכשיו, בלי סדר: צריך לשלם שכר לימוד עד סוף החודש ואין לי מושג כמה נשאר. יש עבודה בסטטיסטיקה שלא התחלתי. אמא מתקשרת כל יום ואני לא עונה. צריך לקבוע תור לרופא בגלל המרשם לריטלין שנגמר. יש מבחן בפסיכולוגיה התפתחותית בעוד שבועיים. השותף לדירה כועס על הכלים. אני רוצה להתחיל ללכת לחדר כושר. צריך להגיש בקשה לסיוע כלכלי ולא יודע איפה הטופס. הלפטופ שלי איטי. יש לי תחושה שאני שוכח משהו חשוב.
אחת, מיין את כל זה לקטגוריות: פעולות מיידיות, לימודים, אדמיניסטרציה, ואישי. שתיים, זהה את המשימה האחת שתוריד לי הכי הרבה חרדה אם אסיים אותה היום. שלוש, הערך זמן ביצוע ריאלי לכל פריט. ארבע, תגיד לי מה כנראה הדבר החשוב שאני שוכח.""")}
{prompt("4 - מנתח הטון", """קיבלתי את המייל הזה מהמרצה ואני בטוח שהוא כועס עליי ושהוא הולך להכשיל אותי:
"שלום, ראיתי את ההגשה. יש בעיה בפרק השלישי, הניתוח לא תואם את המתודולוגיה שהצהרת עליה בהקדמה. תתקן ותגיש עד יום חמישי. בברכה, ד"ר לוי."
נתח את הטון של המייל באופן אובייקטיבי לחלוטין. האם הוא תוקפני, או פשוט ענייני וישיר? מה בדיוק הוא מבקש, ומה הוא לא אומר? ואז עזור לי לנסח תשובה קצרה ומקצועית שמכירה בביקורת, מאשרת שאתקן עד יום חמישי, ושואלת שאלה אחת ממוקדת - בלי להתגונן ובלי להתנצל יתר על המידה.""")}
{prompt("5 - חונך סוקרטי", """אני מדביק כאן קטע ממאמר שאני צריך להבין לעומק למבחן. אל תסכם אותו לי. במקום זה, פעל כחונך סוקרטי: שאל אותי שאלה אחת בכל פעם על הטקסט כדי לבדוק אם הבנתי. חכה לתשובה שלי, ורק אז תקן אותי או תעבור לשאלה הבאה. התחל מהשאלה הכי בסיסית.
[הדבק כאן את הקטע]""")}
<div class="callout"><b>לקרוא עם האוזניים:</b> לא פרומפט אלא פעולה - מזינים מאמר ל-Gemini Notebook ומייצרים <span class="en">Audio Overview</span>. מי שעבר בתחנה 2 כבר יודע איך.</div>
<div class="callout"><b>שאלה לזוג:</b> איזו מהטכניקות הייתם מלמדים לסטודנט מחר בבוקר - ואיפה בדיקנט זה היה יושב?</div>
'''

BODY[5] = f'''
<p class="lead">בונים אפליקציה קטנה ליחידה שלכם על ידי תיאור של מה אתם צריכים.</p>
<div class="callout"><b>הרציונל:</b> וויב קודינג הוא לתאר את הצורך בשפה טבעית ולתת לבינה לכתוב את הקוד, להריץ אותו, ולתקן. מי שיודע להסביר מה הוא צריך - יכול לבנות כלי שעובד. זה הופך את "צריך מחלקת מחשוב" ל"צריך שעה ורעיון ברור".</div>
<ol class="steps">
<li>נכנסים ל-<a href="https://gemini.google.com" target="_blank" rel="noopener"><span class="en">gemini.google.com</span></a> ומפעילים את כפתור <span class="en">Canvas</span> בסרגל הכלים של תיבת ההודעה</li>
<li>חושבים על אפליקציה אחת שהייתם רוצים ליחידה - משהו קטן ושימושי: מחשבון זכאות, טופס קבלת פנייה, לוח תורנויות, מדריך אינטראקטיבי לסטודנט חדש</li>
<li>כותבים את הצורך (התבנית למטה), שולחים, ומנסים את מה שנוצר</li>
<li>מבקשים תיקונים בשפה טבעית: "תוסיף...", "תשנה את...", "זה לא עובד כש..."</li>
</ol>
<p><b>איך מנסחים פרומפט לוויב קודינג:</b></p>
<ul class="tips">
<li><b>לנסח את הצורך, לא בהכרח את הדרך.</b> "אני צריך שרכז יוכל לראות בשנייה מי מהסטודנטים במעונות עוד לא הגיש טופס" - ולא "תבנה טבלה עם עמודות א' ב' ג'". הבינה תמצא את הדרך לשם.</li>
<li>לתאר מי המשתמש ומה הוא עושה עם זה ביום עבודה רגיל.</li>
<li>לתת דוגמה אחת אמיתית, עם נתונים בדויים, של מה נכנס ומה יוצא.</li>
<li>להתחיל קטן ולהוסיף בשיחה - לא לבקש הכל בבת אחת.</li>
</ul>
{prompt("תבנית", "אני [תפקיד] ביחידת [שם היחידה] בדיקנט הסטודנטים. אני רוצה כלי קטן שיעזור לי ב[הצורך, במשפט אחד]. מי שישתמש בו: [מי]. מה שקורה היום בלי הכלי: [תיאור קצר של הכאב]. דוגמה: [נתונים בדויים - מה נכנס, מה אמור לצאת]. בנה לי גרסה ראשונה פשוטה שאפשר להשתמש בה, בעברית, ותסביר לי בשתי שורות מה בנית. אחר כך נשפר יחד.", "בסיס לעריכה - מלאו את הסוגריים בשלכם.")}
<div class="callout"><b>מה חשוב לדעת:</b> הכלי הזה בג'מיני מוגבל ביכולות שלו - הוא טעימה. אבל <span class="en">ChatGPT Work</span>, <span class="en">Claude Code</span>, <span class="en">Grok Bot</span> ועוד שחקנים בשוק מאפשרים היום לבנות אפליקציות ייעודיות בקלות - כאלה שמשרתות את צוות היחידה או את הסטודנטים, עם נתונים אמיתיים ועם תחזוקה לאורך זמן.</div>
<div class="callout"><b>שאלה לזוג:</b> מה הדבר הראשון שהאפליקציה שלכם עשתה נכון, ומה היא לא הבינה? מה בניסוח שלכם גרם לזה?</div>
'''

BODY[6] = '''
<p class="lead">עוצרים את ההתנסות ומדברים בזוג. המטרה: לצאת עם משפט אחד - "הדבר הראשון שננסה ביחידה שלנו הוא..." - שנאמר אחר כך בקול במליאה.</p>
<ol class="steps">
<li>מה מכל מה שניסיתם היום הכי קרוב לשימוש אמיתי ביחידה שלכם - ומה חוסם אותו?</li>
<li>איזה ידע ביחידה שלכם "מתאדה" היום - ואיפה הייתם מתחילים לאסוף אותו?</li>
<li>אם היה לכם Gem או מחברת שעובדים - מי ביחידה משתמש בהם ראשון, ועל מה?</li>
<li>מה צריך לקרות ברמת האוניברסיטה - רישיון, אישור, מדיניות - כדי שזה יעבור מטעימה להטמעה?</li>
<li>מה אתם רוצים ללמד את הסטודנטים שלכם - ומי מלמד את זה היום?</li>
<li><b>וויב קודינג:</b> איזו אפליקציה הייתם מפתחים היום, אילו ידעתם לעבוד עם סוכני קידוד מתקדמים? האם כבר יצא לכם להתנסות?</li>
</ol>
<div class="callout"><b>המשפט של היחידה:</b> כשאתם מוכנים - מרימים יד. נשמע את כולם במליאה.</div>
'''

HEAD = '''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<meta name="description" content="{{DESC}}">
<link rel="icon" type="image/png" href="assets/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;800&family=Noto+Sans+Hebrew:wght@400;500;700&display=swap" rel="stylesheet">
<style>{{CSS}}</style>
</head>
<body>
<a href="#main-content" class="skip-link">דלג לתוכן הראשי</a>
'''

FOOT = '''
<footer>
  <div class="wrap">
    <p>סדנת בינה מלאכותית לדיקנט הסטודנטים, האוניברסיטה העברית &middot; תום הגלעדי &middot; <a href="deck/" target="_blank" rel="noopener">למצגת של ההרצאה</a></p>
    <div class="accessibility-statement">
      <h3>הצהרת נגישות</h3>
      <p>אתר זה עומד בדרישות תקנות שוויון זכויות לאנשים עם מוגבלות (התאמות נגישות לשירות), התשע"ג-2013, ותקן ישראלי ת"י 5568 המבוסס על הנחיות WCAG 2.0 ברמה AA.</p>
      <p>אם נתקלתם בבעיית נגישות באתר, אנא פנו אלינו ונשמח לסייע:</p>
      <p><strong>רכז נגישות:</strong> תום הגלעדי<br><strong>אימייל:</strong> <a href="mailto:tomhagiladi@gmail.com">tomhagiladi@gmail.com</a></p>
    </div>
  </div>
</footer>
<div class="sr-only" aria-live="polite" id="live"></div>
<script>
(function(){
  const live=document.getElementById('live');
  const check='__CHECK__';
  document.querySelectorAll('.copy').forEach(btn=>{
    const original=btn.innerHTML;
    btn.addEventListener('click',async()=>{
      const text=btn.closest('.prompt').querySelector('pre').innerText;
      try{ await navigator.clipboard.writeText(text); }
      catch(e){ const ta=document.createElement('textarea'); ta.value=text; ta.setAttribute('readonly',''); ta.style.position='absolute'; ta.style.left='-9999px'; document.body.appendChild(ta); ta.select(); try{document.execCommand('copy');}catch(_){ } document.body.removeChild(ta); }
      btn.classList.add('done'); btn.innerHTML=check+'<span>הועתק</span>'; live.textContent='הפרומפט הועתק ללוח';
      setTimeout(()=>{ btn.classList.remove('done'); btn.innerHTML=original; live.textContent=''; },1800);
    });
  });
  document.querySelectorAll('table').forEach(t=>{ const w=document.createElement('div'); w.className='table-scroll-wrapper'; w.setAttribute('tabindex','0'); w.setAttribute('role','region'); w.setAttribute('aria-label','טבלה ניתנת לגלילה'); t.parentNode.insertBefore(w,t); w.appendChild(t); });
})();
</script>
</body>
</html>
'''.replace('__CHECK__', CHECK_SVG.replace("'", "\\'"))

def page(title, desc, body):
    return HEAD.replace('{{TITLE}}', title).replace('{{DESC}}', desc).replace('{{CSS}}', CSS) + body + FOOT

def tools_buttons():
    items = ''.join(
        f'<li><a class="tool" href="{u}" target="_blank" rel="noopener"><span class="nm">{EXT_SVG}<span class="en">{n}</span></span><span class="ln">{d}</span></a></li>'
        for n, u, short, d in TOOLS)
    return f'<section class="tools" aria-labelledby="tools-h"><h2 id="tools-h">קישורים לכלים - לחצו לפתיחה בלשונית חדשה</h2><ul>{items}</ul></section>'

def stcard(num, slug, title, what, kind):
    cls = 'stcard anchor' if kind else 'stcard'
    tag = ''
    if kind == 'start': tag = '<span class="tag">כולם מתחילים כאן</span><br>'
    if kind == 'end':   tag = '<span class="tag">כולם מסיימים כאן</span><br>'
    return (f'<a class="{cls}" href="{slug}.html"><span class="n" aria-hidden="true">{num}</span>'
            f'<span class="tt">{tag}<h3>{title}</h3><p class="what">{what}</p></span>'
            f'<span class="go" aria-hidden="true">{ARROW_SVG}</span></a>')

def home():
    s = {n: (num, slug, t, w, k) for (num, slug, t, w, k) in STATIONS for n in [num]}
    body = f'''
<header class="hero">
  <div class="wrap">
    <img class="logo" src="assets/logo.png" alt="תום הגלעדי - Empowering through AI">
    <h1>סדנת AI - דיקנט הסטודנטים</h1>
    <p class="sub">האוניברסיטה העברית &middot; 8 בספטמבר 2026 &middot; החלק המעשי</p>
    <div class="join">
      <img src="assets/qr-platform.png" alt="קוד QR לכתובת הפלטפורמה">
      <p class="t">סרקו והצטרפו מהטלפון או מהמחשב</p>
      <p class="u"><span class="en">{URL}</span></p>
    </div>
  </div>
</header>
<main id="main-content">
<div class="wrap">
  {tools_buttons()}
  <div class="grid2">
    <section class="card tone" aria-labelledby="how-h">
      <h2 id="how-h">איך עובדים היום</h2>
      <p class="lead">בזוגות, מחשב אחד לזוג. המטרה היא לעשות יחד, לדבר על ההתנסות תוך כדי, ולקיים סיעור מוחות של שני מוחות אנושיים עם מוח מלאכותי - ולדון בחוויה.</p>
      <p>מומלץ לתפוס מרחק ולהתפזר בחלל. תום זמין ומסתובב בין כולם - מרימים יד וקוראים לו להתייעצות או לעזרה.</p>
    </section>
    <section class="card warn" aria-labelledby="sec-h">
      <h2 id="sec-h">אבטחת מידע</h2>
      <p class="lead">לא מזינים שמות, מספרי זהות או פרטים מזהים של סטודנטים לכלים החינמיים.</p>
      <p>מי שעובד עם מנוי ארגוני של המוסד - מתנהל לפי הנחיות המוסד.</p>
    </section>
  </div>
  <section class="route" id="route" aria-labelledby="route-h">
    <h2 id="route-h">המסלול</h2>
    <p class="hint">כולם מתחילים בתחנה 1. אחרי שמיציתם אותה - בחירה חופשית בין תחנות 2 עד 5, כל זוג לפי המסלול והקצב שלו. כולם מסיימים בתחנה 6.</p>
    {stcard(*s[1])}
    <div class="group-title"><h3>בחירה חופשית - אחרי תחנה 1</h3></div>
    <div class="optional">{stcard(*s[2])}{stcard(*s[3])}{stcard(*s[4])}{stcard(*s[5])}</div>
    {stcard(*s[6])}
  </section>
</div>
</main>
'''
    return page("סדנת AI - דיקנט הסטודנטים",
                "פלטפורמת ההתנסות של סדנת הבינה המלאכותית לדיקנט הסטודנטים באוניברסיטה העברית: שש תחנות, פרומפטים מוכנים להעתקה, והוראות צעד אחר צעד.",
                body)

def station(num, slug, title, what, kind):
    steps = ''
    for (n2, slug2, t2, w2, k2) in STATIONS:
        cls = 'big' if k2 else ''
        cur = ' aria-current="page"' if n2 == num else ''
        steps += f'<li><a class="{cls}" href="{slug2}.html" aria-label="תחנה {n2} - {t2}"{cur}>{n2}</a></li>'
        if n2 < 6: steps += '<li class="ln" aria-hidden="true"></li>'
    minitools = ''.join(f'<li><a href="{u}" target="_blank" rel="noopener"><span class="en">{n}</span></a></li>' for n, u, sh, d in TOOLS)
    banner = ''
    hero_cls = 'station-hero anchor' if kind else 'station-hero'
    if kind == 'start': banner = f'<p class="banner">{START_SVG}כולם מתחילים כאן</p>'
    if kind == 'end':   banner = f'<p class="banner">{CHECK_SVG}כולם מסיימים כאן</p>'
    # bottom nav
    if kind:
        nav = ''
    else:
        nn = num + 1 if num < 5 else 6
        nslug = [x[1] for x in STATIONS if x[0] == nn][0]
        nav = f'<nav class="pagenav" aria-label="ניווט בין תחנות"><span></span><a class="btn" href="{nslug}.html">לתחנה {nn}{ARROW_SVG}</a></nav>'
    body = f'''
<header class="topbar">
  <div class="wrap"><div class="row">
    <a class="btn primary" href="index.html#route">{HOME_SVG}חזרה לדף הבית - לבחירת תחנה</a>
    <nav aria-label="מסלול התחנות"><ol class="stepper">{steps}</ol></nav>
    <nav aria-label="קישורים לכלים"><ul class="minitools">{minitools}</ul></nav>
  </div></div>
</header>
<main id="main-content">
<div class="wrap">
  <section class="{hero_cls}">
    {banner}
    <div class="head"><span class="n" aria-hidden="true">{num}</span><h1>{title}</h1></div>
  </section>
  <section class="card">
    {BODY[num]}
  </section>
  {nav}
</div>
</main>
'''
    return page(f"תחנה {num} - {title}", f"תחנה {num} בסדנת AI לדיקנט הסטודנטים: {what}", body).replace('<body>', '<body class="st">', 1)

os.makedirs(OUT, exist_ok=True)
io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(home())
for st in STATIONS:
    io.open(os.path.join(OUT, st[1] + ".html"), "w", encoding="utf-8").write(station(*st))
print("built: index.html +", len(STATIONS), "station pages")
