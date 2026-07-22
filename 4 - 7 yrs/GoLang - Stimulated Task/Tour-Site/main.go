package main

import (
	"html/template"
	"log"
	"net/http"
)

var homePage = template.Must(template.New("home").Parse(`<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Roamly — Find your next story</title>
  <style>
    :root { --ink:#19302b; --cream:#fbf7ee; --coral:#ef6b4d; --mint:#b9ddd0; --white:#fff; }
    * { box-sizing:border-box; }
    body { margin:0; color:var(--ink); background:var(--cream); font-family:Arial, sans-serif; }
    header { position:absolute; z-index:2; width:100%; padding:24px 7%; display:flex; align-items:center; justify-content:space-between; color:white; }
    .logo { font:800 25px Georgia, serif; letter-spacing:.5px; }
    nav { display:flex; gap:28px; align-items:center; }
    nav a { color:inherit; text-decoration:none; font-size:14px; font-weight:700; }
    .nav-button { border:1px solid rgba(255,255,255,.7); padding:11px 18px; border-radius:999px; }
    .hero { min-height:720px; display:grid; place-items:center; padding:120px 7% 80px; text-align:center; color:white; position:relative; overflow:hidden; background:linear-gradient(135deg,rgba(10,44,40,.45),rgba(18,44,39,.1)),linear-gradient(160deg,#204f49 0%,#558c7c 52%,#d6a66f 100%); }
    .hero:before,.hero:after { content:""; position:absolute; border-radius:50%; filter:blur(2px); }
    .hero:before { width:520px; height:520px; right:-150px; top:80px; background:rgba(239,107,77,.28); }
    .hero:after { width:440px; height:440px; left:-130px; bottom:-180px; background:rgba(185,221,208,.27); }
    .hero-content { position:relative; z-index:1; max-width:820px; }
    .eyebrow { text-transform:uppercase; letter-spacing:3px; font-size:12px; font-weight:bold; }
    h1 { margin:20px 0; font:700 clamp(48px,8vw,92px)/.98 Georgia,serif; }
    .hero p { margin:0 auto 34px; max-width:610px; font-size:18px; line-height:1.65; color:rgba(255,255,255,.9); }
    .search { max-width:760px; margin:auto; display:grid; grid-template-columns:1fr 1fr auto; gap:10px; padding:10px; background:white; border-radius:18px; text-align:left; box-shadow:0 20px 60px rgba(10,35,31,.25); }
    .field { padding:8px 18px; border-right:1px solid #e8e5de; }
    .field span { display:block; color:#71817d; font-size:11px; text-transform:uppercase; letter-spacing:1px; margin-bottom:5px; }
    .field strong { color:var(--ink); font-size:14px; }
    button { border:0; border-radius:13px; background:var(--coral); color:white; padding:0 26px; font-weight:bold; cursor:pointer; }
    section { padding:90px 7%; }
    .section-head { display:flex; justify-content:space-between; align-items:end; gap:24px; margin-bottom:35px; }
    h2 { margin:8px 0 0; font:700 clamp(34px,5vw,54px)/1.08 Georgia,serif; }
    .section-head a { color:var(--ink); font-weight:bold; text-decoration:none; border-bottom:2px solid var(--coral); padding-bottom:4px; }
    .cards { display:grid; grid-template-columns:repeat(3,1fr); gap:22px; }
    .card { min-height:390px; border-radius:22px; overflow:hidden; position:relative; display:flex; align-items:end; padding:26px; color:white; box-shadow:0 15px 30px rgba(25,48,43,.12); }
    .card:after { content:""; position:absolute; inset:0; background:linear-gradient(transparent 35%,rgba(8,30,26,.78)); }
    .card:nth-child(1) { background:linear-gradient(145deg,#b9ddd0,#3e786b); }
    .card:nth-child(2) { background:linear-gradient(145deg,#e9b46d,#a64f40); }
    .card:nth-child(3) { background:linear-gradient(145deg,#9ec4db,#324f6e); }
    .card-content { position:relative; z-index:1; width:100%; }
    .card h3 { font:700 29px Georgia,serif; margin:7px 0; }
    .card-row { display:flex; justify-content:space-between; align-items:center; color:rgba(255,255,255,.86); }
    .promise { margin:0 7% 80px; padding:58px; border-radius:28px; background:var(--ink); color:white; display:grid; grid-template-columns:1.2fr 1fr; gap:60px; align-items:center; }
    .promise h2 { color:white; }
    .features { display:grid; gap:22px; }
    .feature { display:grid; grid-template-columns:45px 1fr; gap:15px; align-items:start; }
    .icon { width:42px; height:42px; display:grid; place-items:center; border-radius:50%; background:var(--coral); font-size:19px; }
    .feature strong { display:block; margin:2px 0 6px; }
    .feature small { color:#c5d2ce; line-height:1.5; }
    footer { padding:25px 7% 40px; display:flex; justify-content:space-between; color:#71817d; font-size:13px; }
    @media (max-width:760px) { nav a:not(.nav-button) { display:none; } .hero { min-height:680px; } .search { grid-template-columns:1fr; } .field { border-right:0; border-bottom:1px solid #e8e5de; } button { padding:18px; } .cards,.promise { grid-template-columns:1fr; } .promise { padding:36px 28px; margin-inline:4%; } }
  </style>
</head>
<body>
  <header>
    <div class="logo">ROAMLY.</div>
    <nav><a href="#trips">Destinations</a><a href="#why">Why Roamly</a><a class="nav-button" href="#trips">Plan a trip</a></nav>
  </header>

  <main>
    <section class="hero">
      <div class="hero-content">
        <div class="eyebrow">Small groups · Big adventures</div>
        <h1>Find your next story.</h1>
        <p>Thoughtfully designed journeys that bring you closer to remarkable places, local people, and the moments you will remember forever.</p>
        <div class="search">
          <div class="field"><span>Where to?</span><strong>Choose a destination</strong></div>
          <div class="field"><span>When?</span><strong>Pick your travel month</strong></div>
          <button type="button">Explore trips →</button>
        </div>
      </div>
    </section>

    <section id="trips">
      <div class="section-head">
        <div><div class="eyebrow">Curated escapes</div><h2>Trending journeys</h2></div>
        <a href="#trips">View all trips →</a>
      </div>
      <div class="cards">
        <article class="card"><div class="card-content"><small>8 DAYS · PORTUGAL</small><h3>Coast & cobblestones</h3><div class="card-row"><span>From $1,890</span><span>→</span></div></div></article>
        <article class="card"><div class="card-content"><small>10 DAYS · MOROCCO</small><h3>Desert after dark</h3><div class="card-row"><span>From $2,240</span><span>→</span></div></div></article>
        <article class="card"><div class="card-content"><small>7 DAYS · NORWAY</small><h3>Beyond the fjords</h3><div class="card-row"><span>From $2,690</span><span>→</span></div></div></article>
      </div>
    </section>

    <section class="promise" id="why">
      <div><div class="eyebrow">Travel better</div><h2>Every detail handled. Every moment yours.</h2></div>
      <div class="features">
        <div class="feature"><div class="icon">✦</div><div><strong>Local at heart</strong><small>Travel with expert local guides who know every hidden corner.</small></div></div>
        <div class="feature"><div class="icon">♧</div><div><strong>Lighter footprint</strong><small>Smaller groups and stays that support local communities.</small></div></div>
        <div class="feature"><div class="icon">✓</div><div><strong>Effortlessly planned</strong><small>We handle the details so you can stay present for the adventure.</small></div></div>
      </div>
    </section>
  </main>

  <footer><span>© 2026 Roamly Travel Co.</span><span>Made for the journey.</span></footer>
</body>
</html>`))

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			http.NotFound(w, r)
			return
		}
		if err := homePage.Execute(w, nil); err != nil {
			http.Error(w, "Unable to render page", http.StatusInternalServerError)
		}
	})

	log.Println("Tour site running at http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
