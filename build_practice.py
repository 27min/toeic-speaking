# -*- coding: utf-8 -*-
"""문장 연습 PWA(콘텐츠 무포함) 생성기.

앱에는 문장 데이터를 포함하지 않는다. 사용자가 텍스트 파일을 업로드하거나
붙여넣으면 브라우저에서 파싱하여 각 기기(localStorage)에만 저장하고 연습한다.

생성물:
  index.html              연습 페이지 (GitHub Pages 진입점)
  manifest.webmanifest    PWA 매니페스트
  sw.js                   서비스워커 (오프라인 캐싱)
  icon.svg                앱 아이콘
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

MANIFEST = """{
  "name": "스피킹 만능문장 연습",
  "short_name": "만능문장",
  "description": "스피킹 만능문장 암기/발음 연습 (문장은 직접 불러오기)",
  "lang": "ko",
  "start_url": "./index.html",
  "scope": "./",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#0f172a",
  "theme_color": "#0f172a",
  "icons": [
    { "src": "./icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable" }
  ]
}
"""

ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="104" fill="#0f172a"/>
  <rect x="216" y="96" width="80" height="180" rx="40" fill="#38bdf8"/>
  <path d="M160 248a96 96 0 0 0 192 0" fill="none" stroke="#38bdf8" stroke-width="22" stroke-linecap="round"/>
  <rect x="246" y="344" width="20" height="56" rx="10" fill="#38bdf8"/>
  <rect x="196" y="404" width="120" height="20" rx="10" fill="#38bdf8"/>
  <text x="50%" y="468" font-size="56" font-family="Arial, sans-serif" font-weight="bold"
        fill="#94a3b8" text-anchor="middle">SPEAKING</text>
</svg>
"""

SW = """const CACHE = "tsmun-v3";
const ASSETS = ["./", "./index.html", "./manifest.webmanifest", "./icon.svg"];
self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks =>
    Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request).then(resp => {
      const copy = resp.clone();
      caches.open(CACHE).then(c => c.put(e.request, copy));
      return resp;
    }).catch(() => caches.match("./index.html")))
  );
});
"""


def main():
    for name, content in [
        ("index.html", TEMPLATE),
        ("manifest.webmanifest", MANIFEST),
        ("sw.js", SW),
        ("icon.svg", ICON),
    ]:
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(content)
    print("생성: index.html, manifest.webmanifest, sw.js, icon.svg")
    print("앱에 문장 데이터는 포함되지 않습니다(업로드 방식).")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>스피킹 만능문장 연습</title>
<meta name="description" content="스피킹 만능문장 암기/발음 연습 도구 (문장은 직접 불러오기)">
<meta name="theme-color" content="#0f172a">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="만능문장">
<link rel="manifest" href="./manifest.webmanifest">
<link rel="apple-touch-icon" href="./icon.svg">
<link rel="icon" href="./icon.svg">
<style>
  :root{
    --bg:#0f172a; --card:#1e293b; --card2:#273449; --line:#334155;
    --txt:#e2e8f0; --muted:#94a3b8; --accent:#38bdf8; --accent2:#22c55e;
    --warn:#fbbf24; --hide:#475569;
  }
  [data-theme="light"]{
    --bg:#f1f5f9; --card:#ffffff; --card2:#eef2f7; --line:#d8e0ea;
    --txt:#0f172a; --muted:#5b6b7f; --accent:#0284c7; --accent2:#16a34a;
    --warn:#b45309; --hide:#cbd5e1;
  }
  *{box-sizing:border-box;}
  body{margin:0;background:var(--bg);color:var(--txt);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Apple SD Gothic Neo",sans-serif;
    line-height:1.5;-webkit-tap-highlight-color:transparent;}
  header{position:sticky;top:0;z-index:20;background:var(--bg);
    border-bottom:1px solid var(--line);padding:max(14px,env(safe-area-inset-top)) 16px 10px;}
  h1{font-size:18px;margin:0 0 8px;display:flex;align-items:center;gap:8px;}
  h1 .grow{flex:1;}
  .iconbtn{background:var(--card);border:1px solid var(--line);color:var(--txt);
    border-radius:8px;height:36px;min-width:36px;padding:0 9px;font-size:14px;cursor:pointer;}
  .ovbar{height:8px;background:var(--card);border-radius:999px;overflow:hidden;margin:2px 0 4px;}
  .ovfill{height:100%;width:0;background:linear-gradient(90deg,var(--accent),var(--accent2));transition:width .3s;}
  .ovnum{font-size:11.5px;color:var(--muted);margin-bottom:8px;}
  .controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;}
  select,input[type=search]{background:var(--card);color:var(--txt);
    border:1px solid var(--line);border-radius:8px;padding:7px 10px;font-size:13px;max-width:100%;}
  input[type=search]{flex:1;min-width:120px;}
  .toggles{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;}
  .tg{background:var(--card);color:var(--muted);border:1px solid var(--line);
    border-radius:999px;padding:6px 12px;font-size:12.5px;cursor:pointer;user-select:none;}
  .tg.active{background:var(--accent);color:#06283d;border-color:var(--accent);font-weight:600;}
  .tg.danger.active{background:var(--warn);color:#3a2c00;border-color:var(--warn);}
  .modebar{display:flex;gap:6px;margin-top:8px;}
  .modebar .tg{flex:1;text-align:center;}
  main{max-width:760px;margin:0 auto;padding:14px 14px calc(80px + env(safe-area-inset-bottom));}
  .part-head{margin:26px 0 8px;}
  .part-title{font-size:15px;font-weight:800;color:var(--txt);}
  .part-title .pnum{font-size:12px;color:var(--muted);font-weight:500;margin-left:6px;}
  .pbar{height:5px;background:var(--card);border-radius:999px;overflow:hidden;margin-top:5px;}
  .pfill{height:100%;width:0;background:var(--accent2);transition:width .3s;}
  .sec-title{font-size:13px;color:var(--accent);font-weight:700;margin:18px 0 8px;
    border-left:3px solid var(--accent);padding-left:8px;}
  .card{background:var(--card);border:1px solid var(--line);border-radius:12px;
    padding:12px 14px;margin:8px 0;transition:.15s;}
  .card.done{opacity:.5;border-color:var(--accent2);}
  .row{display:flex;align-items:flex-start;gap:10px;}
  .chk{flex:0 0 auto;width:22px;height:22px;border-radius:6px;border:2px solid var(--line);
    background:transparent;cursor:pointer;margin-top:2px;display:flex;align-items:center;
    justify-content:center;font-size:14px;color:transparent;}
  .card.done .chk{background:var(--accent2);border-color:var(--accent2);color:#06280f;}
  .body{flex:1;min-width:0;}
  .en{font-size:16px;font-weight:600;color:var(--txt);cursor:pointer;}
  .ko{font-size:13.5px;color:var(--muted);margin-top:3px;cursor:pointer;}
  .pron{font-size:12.5px;color:var(--accent);margin-top:3px;cursor:pointer;}
  .speak{flex:0 0 auto;background:var(--card2);border:1px solid var(--line);color:var(--accent);
    border-radius:8px;width:34px;height:34px;cursor:pointer;font-size:16px;}
  .speak:active{transform:scale(.92);}
  .hide-en .en, .hide-ko .ko, .hide-pron .pron{
    color:transparent !important;background:var(--hide);border-radius:6px;padding:0 6px;}
  .reveal .en{color:var(--txt) !important;background:transparent !important;}
  .reveal .ko{color:var(--muted) !important;background:transparent !important;}
  .reveal .pron{color:var(--accent) !important;background:transparent !important;}
  .empty{text-align:center;color:var(--muted);padding:40px 10px;}
  /* 로더 */
  #loader{display:none;}
  #loader.on{display:block;}
  .loadcard{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px 18px;margin-top:18px;}
  .loadcard h2{font-size:17px;margin:0 0 8px;}
  .loadcard p{font-size:13px;color:var(--muted);margin:0 0 16px;}
  .filebtn{display:block;text-align:center;background:var(--accent);color:#06283d;font-weight:700;
    border-radius:12px;padding:16px;cursor:pointer;font-size:15px;}
  .or{text-align:center;color:var(--muted);font-size:12px;margin:14px 0 8px;}
  textarea{width:100%;min-height:120px;background:var(--bg);color:var(--txt);border:1px solid var(--line);
    border-radius:10px;padding:10px;font-size:13px;font-family:inherit;resize:vertical;}
  .loadcard details{margin-top:16px;}
  .loadcard summary{cursor:pointer;color:var(--accent);font-size:13px;}
  .loadcard pre{background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:10px;
    overflow:auto;font-size:12px;color:var(--muted);}
  .loaderr{color:#f87171;font-size:12.5px;margin-top:8px;min-height:16px;}
  #practice{display:none;}
  #practice.on{display:block;}
  #flash{display:none;} #flash.on{display:block;}
  .fc{background:var(--card);border:1px solid var(--line);border-radius:16px;
    padding:34px 20px;text-align:center;min-height:230px;display:flex;flex-direction:column;
    justify-content:center;gap:14px;margin-top:14px;}
  .fc .fc-ko{font-size:19px;color:var(--txt);}
  .fc .fc-en{font-size:22px;font-weight:700;color:var(--txt);}
  .fc .fc-pron{font-size:14px;color:var(--accent);}
  .fc .muted{color:var(--muted);font-size:13px;}
  .fcnav{display:flex;gap:8px;margin-top:12px;}
  .btn{flex:1;background:var(--card2);color:var(--txt);border:1px solid var(--line);
    border-radius:10px;padding:12px;font-size:14px;cursor:pointer;font-weight:600;}
  .btn.primary{background:var(--accent);color:#06283d;border-color:var(--accent);}
  .btn.danger{color:#f87171;}
  .fcprog{text-align:center;color:var(--muted);font-size:12.5px;margin-top:10px;}
  .hint{color:var(--muted);font-size:11.5px;margin-top:6px;}
  ::placeholder{color:#94a3b8;}
</style>
</head>
<body>
<header>
  <h1>🎤 만능문장 연습 <span class="grow"></span>
    <button class="iconbtn" id="dataBtn" title="데이터 불러오기/교체">📁</button>
    <button class="iconbtn" id="themeBtn" title="테마">☀️</button>
  </h1>
  <div id="hdrApp">
    <div class="ovbar"><div class="ovfill" id="ovfill"></div></div>
    <div class="ovnum" id="ovnum"></div>
    <div class="controls">
      <select id="partSel"></select>
      <input type="search" id="search" placeholder="검색 (영어/뜻/발음)">
    </div>
    <div class="controls" style="margin-top:8px;">
      <select id="voiceSel" title="목소리 선택" style="flex:1;min-width:140px;"></select>
      <button class="tg" id="testVoice">🔊 미리듣기</button>
    </div>
    <div class="modebar">
      <div class="tg active" data-mode="list">📋 목록</div>
      <div class="tg" data-mode="flash">🃏 플래시카드</div>
    </div>
    <div class="toggles" id="listToggles">
      <div class="tg" data-toggle="en">영어 가리기</div>
      <div class="tg" data-toggle="ko">뜻 가리기</div>
      <div class="tg" data-toggle="pron">발음 가리기</div>
      <div class="tg danger" data-toggle="onlyTodo">미암기만</div>
      <div class="tg" id="resetBtn">암기 초기화</div>
    </div>
    <div class="hint" id="hint">💡 가려진 글자를 탭하면 잠깐 보입니다. 체크박스로 암기 표시(자동 저장).</div>
  </div>
</header>

<main>
  <!-- 데이터 불러오기 -->
  <div id="loader">
    <div class="loadcard">
      <h2>📥 문장 데이터 불러오기</h2>
      <p>저작권 보호를 위해 이 앱에는 문장이 포함되어 있지 않습니다. 본인이 가진 텍스트 파일을 불러와 연습하세요.
         불러온 내용은 <b>이 기기 브라우저에만</b> 저장되며 서버로 전송되지 않습니다.</p>
      <label class="filebtn">📁 텍스트 파일 선택 (.txt)
        <input type="file" id="fileInput" accept=".txt,.md,text/plain" hidden>
      </label>
      <div class="or">— 또는 붙여넣기 —</div>
      <textarea id="pasteArea" placeholder="여기에 문장 텍스트를 붙여넣으세요"></textarea>
      <button class="btn primary" id="pasteLoad" style="margin-top:8px;">붙여넣은 내용 불러오기</button>
      <div class="loaderr" id="loadErr"></div>
      <details>
        <summary>지원하는 파일 형식 보기</summary>
        <pre>## Part 1. 제목 (선택)

### 섹션 제목 (선택)

* **English sentence.**
* 뜻: 한국어 뜻
* 발음: 한글 발음</pre>
      </details>
      <button class="btn danger" id="clearData" style="margin-top:14px;display:none;">불러온 데이터 삭제</button>
    </div>
  </div>

  <!-- 연습 영역 -->
  <div id="practice">
    <div id="list"></div>
    <div id="flash">
      <div class="fcprog" id="fcProg"></div>
      <div class="fc" id="fcCard">
        <div class="fc-ko" id="fcKo"></div>
        <div id="fcAnswer" style="display:none">
          <div class="fc-en" id="fcEn"></div>
          <div class="fc-pron" id="fcPron"></div>
        </div>
        <div class="muted" id="fcTapHint">탭하여 정답 보기</div>
      </div>
      <div class="fcnav">
        <button class="btn" id="fcPrev">← 이전</button>
        <button class="btn" id="fcSpeak">🔊 듣기</button>
        <button class="btn primary" id="fcNext">다음 →</button>
      </div>
      <div class="fcnav">
        <button class="btn" id="fcShuffle">🔀 섞기</button>
        <button class="btn" id="fcMark">✅ 암기 표시</button>
      </div>
    </div>
  </div>
</main>

<script>
const LS_DATA = "tsmun_data_v1";
const LS_DONE = "tsmun_done_v1";

function escapeHtml(s){return String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]));}

/* ---- 텍스트 파서 (build_practice.py와 동일 규칙) ---- */
function parseText(text){
  const parts=[]; let cp=null, cs=null, ci=null;
  const push=()=>{ if(ci && ci.en){ cs.items.push(ci); } ci=null; };
  const ensureSec=()=>{ if(!cs){ if(!cp){cp={title:"",sections:[]};parts.push(cp);} cs={title:"",items:[]}; cp.sections.push(cs);} };
  text.split(/\r?\n/).forEach(raw=>{
    const s=raw.trim(); let m;
    if(s.startsWith("## ")){ push(); cp={title:s.slice(3).trim(),sections:[]}; parts.push(cp); cs=null; return; }
    if(s.startsWith("### ")){ push(); if(!cp){cp={title:"",sections:[]};parts.push(cp);} cs={title:s.slice(4).trim(),items:[]}; cp.sections.push(cs); return; }
    if((m=s.match(/^\*\s+\*\*(.+?)\*\*\s*$/))){ push(); ensureSec(); ci={en:m[1].trim(),ko:"",pron:""}; return; }
    if((m=s.match(/^\*\s*뜻\s*:\s*(.*)$/)) && ci){ ci.ko=m[1].trim(); return; }
    if((m=s.match(/^\*\s*발음\s*:\s*(.*)$/)) && ci){ ci.pron=m[1].trim(); return; }
  });
  push();
  parts.forEach(p=>p.sections=p.sections.filter(x=>x.items.length));
  return parts.filter(p=>p.sections.length);
}

/* ---- 상태 ---- */
let DATA=[], FLAT=[], TOTAL=0;
const partTotals={};
let done={}; try{ done=JSON.parse(localStorage.getItem(LS_DONE)||"{}"); }catch(e){ done={}; }
function saveDone(){ localStorage.setItem(LS_DONE, JSON.stringify(done)); }
const state={ part:"all", q:"", hide:{en:false,ko:false,pron:false}, onlyTodo:false, mode:"list" };

function buildFlat(){
  FLAT=[]; for(const k in partTotals) delete partTotals[k];
  DATA.forEach((p,pi)=>p.sections.forEach(sec=>sec.items.forEach(it=>{
    FLAT.push({...it, part:p.title, sec:sec.title, pi, id:p.title+"|"+sec.title+"|"+it.en});
  })));
  FLAT.forEach(it=>{ partTotals[it.pi]=(partTotals[it.pi]||0)+1; });
  TOTAL=FLAT.length;
}

/* ---- 데이터 로드/저장 ---- */
function setData(parts, persist){
  DATA=parts; buildFlat();
  if(persist) localStorage.setItem(LS_DATA, JSON.stringify(DATA));
  fillPartSel(); showApp(true); refresh(); updateProgress();
}
function loadStored(){
  try{ const raw=localStorage.getItem(LS_DATA); if(raw){ const d=JSON.parse(raw); if(d&&d.length){ DATA=d; buildFlat(); return true; } } }catch(e){}
  return false;
}
function showApp(hasData){
  document.getElementById("loader").classList.toggle("on", !hasData);
  document.getElementById("practice").classList.toggle("on", hasData);
  document.getElementById("hdrApp").style.display = hasData ? "block" : "none";
  document.getElementById("clearData").style.display = (DATA && DATA.length) ? "block" : "none";
}
function handleText(text){
  const parts=parseText(text);
  const err=document.getElementById("loadErr");
  const n=parts.reduce((a,p)=>a+p.sections.reduce((b,s)=>b+s.items.length,0),0);
  if(!n){ err.textContent="형식을 인식하지 못했습니다. '* **문장**' / '* 뜻:' / '* 발음:' 형식인지 확인하세요."; return; }
  err.textContent="";
  setData(parts, true);
}
document.getElementById("fileInput").addEventListener("change",e=>{
  const f=e.target.files[0]; if(!f) return;
  const r=new FileReader(); r.onload=()=>handleText(r.result); r.readAsText(f,"utf-8");
});
document.getElementById("pasteLoad").addEventListener("click",()=>{
  const t=document.getElementById("pasteArea").value; if(t.trim()) handleText(t);
});
document.getElementById("dataBtn").addEventListener("click",()=>{
  const showing=document.getElementById("loader").classList.contains("on");
  if(showing && DATA.length){ showApp(true); }      // 로더 닫기
  else { document.getElementById("loader").classList.add("on");
    document.getElementById("practice").classList.remove("on");
    document.getElementById("hdrApp").style.display="none";
    document.getElementById("clearData").style.display = DATA.length ? "block" : "none"; }
});
document.getElementById("clearData").addEventListener("click",()=>{
  if(confirm("불러온 문장 데이터를 삭제할까요? (암기 체크는 유지됩니다)")){
    localStorage.removeItem(LS_DATA); DATA=[]; buildFlat(); fillPartSel();
    document.getElementById("pasteArea").value=""; showApp(false);
  }
});

/* ---- 테마 ---- */
const THEME_KEY="tsmun_theme";
const themeBtn=document.getElementById("themeBtn");
function applyTheme(t){
  document.documentElement.dataset.theme=t; localStorage.setItem(THEME_KEY,t);
  document.querySelector('meta[name=theme-color]').setAttribute('content', t==="light"?"#f1f5f9":"#0f172a");
  themeBtn.textContent = t==="light" ? "🌙" : "☀️";
}
themeBtn.addEventListener("click",()=>applyTheme(document.documentElement.dataset.theme==="light"?"dark":"light"));
applyTheme(localStorage.getItem(THEME_KEY)||"dark");

/* ---- TTS ---- */
let voices=[]; let chosenURI=localStorage.getItem("tsmun_voice")||"";
function rankVoice(v){
  const n=(v.name+" "+v.voiceURI).toLowerCase(); let s=0;
  if(/google/.test(n)) s+=100;
  if(/natural|enhanced|premium|neural|siri/.test(n)) s+=80;
  if(/samantha|allison|ava|tom|evan|nicky|aaron|joelle/.test(n)) s+=40;
  if(/en[-_]us/i.test(v.lang)) s+=30; else if(/en[-_]gb/i.test(v.lang)) s+=20; else s+=5;
  if(/eloquence|fred|albert|zarvox|junior|ralph|bad news|good news|bells|cellos|organ|trinoids|whisper|bahh|boing|wobble|bubbles|jester|superstar|grandma|grandpa|compact/.test(n)) s-=80;
  return s;
}
function loadVoices(){
  voices=speechSynthesis.getVoices().filter(v=>/^en/i.test(v.lang));
  voices.sort((a,b)=>rankVoice(b)-rankVoice(a));
  const sel=document.getElementById("voiceSel"); if(!sel) return;
  if(!voices.length){ sel.innerHTML='<option>영어 음성 없음</option>'; return; }
  sel.innerHTML=voices.map(v=>`<option value="${escapeHtml(v.voiceURI)}">${escapeHtml(v.name)} (${v.lang})</option>`).join("");
  if(chosenURI && voices.some(v=>v.voiceURI===chosenURI)) sel.value=chosenURI;
  else { chosenURI=voices[0].voiceURI; sel.value=chosenURI; }
}
if('speechSynthesis' in window){ loadVoices(); speechSynthesis.onvoiceschanged=loadVoices; }
function speak(text){
  if(!('speechSynthesis' in window)) return;
  speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(text); u.lang="en-US"; u.rate=0.9; u.pitch=1;
  const v=voices.find(v=>v.voiceURI===chosenURI)||voices[0];
  if(v){ u.voice=v; u.lang=v.lang; }
  speechSynthesis.speak(u);
}

/* ---- 필터/진행률 ---- */
function filtered(){
  const q=state.q.trim().toLowerCase();
  return FLAT.filter(it=>{
    if(state.part!=="all" && it.part!==state.part) return false;
    if(state.onlyTodo && done[it.id]) return false;
    if(q){ if(!(it.en+" "+it.ko+" "+it.pron).toLowerCase().includes(q)) return false; }
    return true;
  });
}
function updateProgress(){
  const d=FLAT.filter(it=>done[it.id]).length;
  const pct=TOTAL?Math.round(d/TOTAL*100):0;
  document.getElementById("ovfill").style.width=pct+"%";
  document.getElementById("ovnum").textContent=`암기 ${d} / ${TOTAL}  (${pct}%)`;
  Object.keys(partTotals).forEach(pi=>{
    const bar=document.getElementById("bar-"+pi); if(!bar) return;
    const t=partTotals[pi], dn=FLAT.filter(it=>it.pi==pi && done[it.id]).length;
    bar.style.width=(t?Math.round(dn/t*100):0)+"%";
    const num=document.getElementById("num-"+pi); if(num) num.textContent=`${dn}/${t}`;
  });
}

/* ---- 목록 ---- */
function renderList(){
  const wrap=document.getElementById("list");
  const items=filtered();
  if(!items.length){ wrap.innerHTML='<div class="empty">표시할 문장이 없습니다.</div>'; return; }
  let html="", curPart=null, curSec=null;
  items.forEach(it=>{
    if(it.part!==curPart){ curPart=it.part; curSec=null;
      html+=`<div class="part-head"><div class="part-title">${escapeHtml(curPart||"문장")}<span class="pnum" id="num-${it.pi}"></span></div>
        <div class="pbar"><div class="pfill" id="bar-${it.pi}"></div></div></div>`; }
    if(it.sec!==curSec){ curSec=it.sec; if(curSec) html+=`<div class="sec-title">${escapeHtml(curSec)}</div>`; }
    const cls="card"+(done[it.id]?" done":"")+(state.hide.en?" hide-en":"")+(state.hide.ko?" hide-ko":"")+(state.hide.pron?" hide-pron":"");
    html+=`<div class="${cls}" data-id="${escapeHtml(it.id)}">
      <div class="row">
        <button class="chk" data-act="chk">✓</button>
        <div class="body">
          <div class="en" data-act="reveal">${escapeHtml(it.en)}</div>
          <div class="ko" data-act="reveal">${escapeHtml(it.ko)}</div>
          ${it.pron?`<div class="pron" data-act="reveal">🔈 ${escapeHtml(it.pron)}</div>`:""}
        </div>
        <button class="speak" data-act="speak">🔊</button>
      </div></div>`;
  });
  wrap.innerHTML=html; updateProgress();
}
document.getElementById("list").addEventListener("click",e=>{
  const card=e.target.closest(".card"); if(!card) return;
  const id=card.dataset.id;
  const act=e.target.dataset.act || e.target.closest("[data-act]")?.dataset.act;
  const it=FLAT.find(x=>x.id===id);
  if(act==="chk"){ done[id]=!done[id]; saveDone(); card.classList.toggle("done",!!done[id]);
    updateProgress(); if(state.onlyTodo && done[id]) renderList(); }
  else if(act==="speak"){ if(it) speak(it.en); }
  else if(act==="reveal"){ card.classList.toggle("reveal"); }
});

/* ---- 플래시카드 ---- */
let fcList=[], fcIdx=0, fcShown=false;
function buildFlash(){ fcList=filtered().slice(); fcIdx=0; fcShown=false; renderFlash(); }
function renderFlash(){
  const ans=document.getElementById("fcAnswer"), tap=document.getElementById("fcTapHint");
  if(!fcList.length){ document.getElementById("fcKo").textContent="표시할 문장이 없습니다.";
    ans.style.display="none"; tap.style.display="none"; document.getElementById("fcProg").textContent=""; return; }
  const it=fcList[fcIdx];
  document.getElementById("fcKo").textContent=it.ko||it.en;
  document.getElementById("fcEn").textContent=it.en;
  document.getElementById("fcPron").textContent=it.pron?("🔈 "+it.pron):"";
  ans.style.display=fcShown?"block":"none"; tap.style.display=fcShown?"none":"block";
  document.getElementById("fcProg").textContent=`${fcIdx+1} / ${fcList.length}　${it.part||""}`+(done[it.id]?"　✅":"");
  document.getElementById("fcMark").textContent=done[it.id]?"✅ 암기됨":"⬜ 암기 표시";
}
document.getElementById("fcCard").addEventListener("click",()=>{ fcShown=!fcShown; renderFlash(); });
document.getElementById("fcNext").addEventListener("click",()=>{ if(fcList.length){ fcIdx=(fcIdx+1)%fcList.length; fcShown=false; renderFlash(); }});
document.getElementById("fcPrev").addEventListener("click",()=>{ if(fcList.length){ fcIdx=(fcIdx-1+fcList.length)%fcList.length; fcShown=false; renderFlash(); }});
document.getElementById("fcSpeak").addEventListener("click",()=>{ if(fcList.length) speak(fcList[fcIdx].en); });
document.getElementById("fcShuffle").addEventListener("click",()=>{
  for(let i=fcList.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[fcList[i],fcList[j]]=[fcList[j],fcList[i]];}
  fcIdx=0; fcShown=false; renderFlash(); });
document.getElementById("fcMark").addEventListener("click",()=>{
  if(!fcList.length)return; const it=fcList[fcIdx]; done[it.id]=!done[it.id]; saveDone(); updateProgress(); renderFlash(); });

/* ---- 컨트롤 ---- */
function fillPartSel(){
  document.getElementById("partSel").innerHTML='<option value="all">전체 Part</option>'+
    DATA.filter(p=>p.title).map(p=>`<option value="${escapeHtml(p.title)}">${escapeHtml(p.title)}</option>`).join("");
}
document.getElementById("partSel").addEventListener("change",e=>{ state.part=e.target.value; refresh(); });
document.getElementById("search").addEventListener("input",e=>{ state.q=e.target.value; refresh(); });
document.getElementById("voiceSel").addEventListener("change",e=>{
  chosenURI=e.target.value; localStorage.setItem("tsmun_voice",chosenURI); speak("This is a sample voice for practice."); });
document.getElementById("testVoice").addEventListener("click",()=>speak("This is a sample voice for practice."));
document.querySelectorAll("[data-toggle]").forEach(el=>{
  el.addEventListener("click",()=>{
    const t=el.dataset.toggle;
    if(t==="onlyTodo") state.onlyTodo=!state.onlyTodo; else state.hide[t]=!state.hide[t];
    el.classList.toggle("active"); refresh();
  });
});
document.getElementById("resetBtn").addEventListener("click",()=>{
  if(confirm("암기 체크를 모두 초기화할까요?")){ done={}; saveDone(); refresh(); }});
document.querySelectorAll(".modebar .tg").forEach(el=>{
  el.addEventListener("click",()=>{
    state.mode=el.dataset.mode;
    document.querySelectorAll(".modebar .tg").forEach(x=>x.classList.toggle("active",x===el));
    const flash=state.mode==="flash";
    document.getElementById("flash").classList.toggle("on",flash);
    document.getElementById("list").style.display=flash?"none":"block";
    document.getElementById("listToggles").style.display=flash?"none":"flex";
    document.getElementById("hint").textContent= flash
      ? "💡 카드를 탭하면 정답이 보입니다. 한국어 뜻을 보고 영어를 말해보세요."
      : "💡 가려진 글자를 탭하면 잠깐 보입니다. 체크박스로 암기 표시(자동 저장).";
    refresh();
  });
});
function refresh(){ if(state.mode==="flash") buildFlash(); else renderList(); }

/* ---- 시작 ---- */
if(loadStored()){ fillPartSel(); showApp(true); refresh(); updateProgress(); }
else { showApp(false); }

if('serviceWorker' in navigator){
  window.addEventListener('load',()=>navigator.serviceWorker.register('./sw.js').catch(()=>{}));
}
</script>
</body>
</html>"""

if __name__ == "__main__":
    main()
