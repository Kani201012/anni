import streamlit as st
import zipfile
import io
import json
from datetime import datetime

# --- 1. DESIGN STUDIO CONFIGURATION ---
st.set_page_config(page_title="Kaydiem Titan v7.0 | E-commerce Web Architect", layout="wide", page_icon="🛍️")

st.markdown("""
    <style>
    .main { background: #0f172a; color: white; }
    .stTabs [data-baseweb="tab"] { color: white; font-weight: bold; font-size: 1.1rem; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 4em; 
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%); 
        color: white; font-weight: 900; border: none; font-size: 1.4rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); transition: all 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: DESIGN STUDIO ---
with st.sidebar:
    st.image("https://www.gstatic.com/images/branding/product/2x/business_profile_96dp.png", width=50)
    st.title("Titan v7.0 Studio")
    
    with st.expander("🎭 Architecture", expanded=True):
        layout_dna = st.selectbox("Design DNA", ["Industrial Titan", "Classic Royal", "Soft-UI", "Glass-Tech", "Brutalist"])
        p_color = st.color_picker("Primary Brand Color", "#4A0E0E")
        s_color = st.color_picker("Accent/CTA Color", "#D4AF37")
        border_rad = st.select_slider("Corner Roundness", options=["0px", "12px", "24px", "60px"], value="60px")

    with st.expander("✍️ Typography", expanded=True):
        h_font = st.selectbox("Heading Font", ["Playfair Display", "Oswald", "Montserrat", "Syncopate"])
        b_font = st.selectbox("Body Font", ["Montserrat", "Inter", "Roboto"])
        h_weight = st.select_slider("Weight", options=["300", "400", "700", "900"], value="700")

    gsc_tag = st.text_input("GSC Verification Tag")
    st.info("Built by www.kaydiemscriptlab.com")

st.title("🏗️ Kaydiem Titan Supreme v7.0")

# --- 2. MULTI-TAB DATA COLLECTION ---
tabs = st.tabs(["📍 Identity", "🏗️ Content & SEO", "⚡ E-commerce Data", "🌟 Social Proof", "⚖️ Legal"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        biz_name = st.text_input("Business Name", "Red Hippo (The Planners)")
        biz_phone = st.text_input("Verified Phone", "+91 84540 02711")
        biz_email = st.text_input("Business Email", "events@redhippoplanners.in")
    with c2:
        biz_cat = st.text_input("Category", "Luxury Wedding Planner")
        biz_hours = st.text_input("Hours", "Mon-Sun: 10:00 - 19:00")
        prod_url = st.text_input("Production URL", "https://kani201012.github.io/site/")
    biz_logo = st.text_input("Logo URL (Direct Image Link)")
    biz_addr = st.text_area("Full Maps Physical Address")
    biz_areas = st.text_area("Service Areas (Comma separated)", "Vasant Kunj, Chhatarpur, South Delhi")
    map_iframe = st.text_area("Map Embed HTML Code")

with tabs[1]:
    hero_h = st.text_input("Main Hero Headline", "Crafting Dream Weddings")
    seo_d = st.text_input("Meta Description", "Luxury wedding decorators in New Delhi.")
    biz_key = st.text_input("SEO Keywords")
    biz_serv = st.text_area("Services (One per line)")
    about_txt = st.text_area("Our Story (800+ Words)", height=250)

with tabs[2]:
    st.header("🛒 E-commerce Inventory Management")
    st.info("The engine now handles commas in prices and descriptions perfectly.")
    sheet_url = st.text_input("Published CSV URL", placeholder="https://docs.google.com/spreadsheets/d/.../pub?output=csv")

with tabs[3]:
    testi = st.text_area("Testimonials (Name | Quote)")
    faqs = st.text_area("FAQ (Question? ? Answer)")

with tabs[4]:
    priv_body = st.text_area("Privacy Policy Content", height=300)
    terms_body = st.text_area("Terms Content", height=300)

# --- 3. THE TITAN ENGINE V7.0 ---

if st.button("🚀 DEPLOY WORLD-CLASS E-COMMERCE ASSET"):
    
    # Hero Image for Weddings
    img_h = "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=1600"
    img_f = "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&q=80&w=800"

    # Logo Logic
    logo_html = f'<img src="{biz_logo}" alt="{biz_name}" class="h-12 w-auto">' if biz_logo else f'<span class="text-2xl font-black tracking-tighter" style="color:var(--p)">{biz_name}</span>'

    # WhatsApp Link Logic
    wa_clean = biz_phone.replace(" ", "").replace("+", "")
    wa_base_url = f"https://wa.me/{wa_clean}?text="
    area_list = [a.strip() for a in biz_areas.split(",")]

    theme_css = f"""
    :root {{ --p: {p_color}; --s: {s_color}; --radius: {border_rad}; }}
    body {{ font-family: '{b_font}', sans-serif; color: #0f172a; line-height: 1.7; overflow-x: hidden; width: 100%; }}
    h1, h2, h3 {{ font-family: '{h_font}', sans-serif; font-weight: {h_weight}; text-transform: uppercase; line-height: 1.1; }}
    .hero-title {{ font-size: clamp(2.2rem, 9vw, 110px); text-shadow: 0 4px 20px rgba(0,0,0,0.4); }}
    .btn-p {{ background: var(--p); color: white; padding: 1.2rem 3rem; border-radius: var(--radius); font-weight: 900; transition: all 0.4s; display: inline-block; text-align: center; }}
    .btn-s {{ background: var(--s); color: white; padding: 0.8rem 2rem; border-radius: var(--radius); font-weight: 800; font-size: 0.9rem; transition: 0.3s; display: inline-block; width: 100%; text-align: center; }}
    .glass-nav {{ background: rgba(255, 255, 255, 0.98); backdrop-filter: blur(15px); border-bottom: 1px solid rgba(0,0,0,0.08); width: 100%; }}
    .hero-mask {{ background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.5)), url('{img_h}'); background-size: cover; background-position: center; min-height: 90vh; display: flex; align-items: center; justify-content: center; }}
    .wa-float {{ position: fixed; bottom: 30px; right: 30px; background: #25d366; color: white; width: 65px; height: 65px; border-radius: 50px; display: flex; align-items: center; justify-content: center; z-index: 99999; box-shadow: 0 10px 25px rgba(37,211,102,0.4); }}
    .legal-text {{ white-space: pre-wrap; word-wrap: break-word; font-size: 1.15rem; color: #334155; }}
    .legal-bold-title {{ font-weight: 900; font-size: clamp(2rem, 5vw, 4.5rem); color: var(--p); margin-bottom: 2rem; text-transform: uppercase; line-height: 1; }}
    .product-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2.5rem; }}
    """

    def get_layout(title, desc, content, is_index=False):
        v_tag = f'<meta name="google-site-verification" content="{gsc_tag}">' if (is_index and gsc_tag) else ""
        
        # --- NEW SMART PARSER SCRIPT ---
        dynamic_script = ""
        if is_index and sheet_url:
            dynamic_script = f"""
            <script>
            async function fetchLiveData() {{
                try {{
                    const response = await fetch('{sheet_url}');
                    const csvText = await response.text();
                    
                    // Robust CSV Splitter (Handles commas inside quotes)
                    const rows = csvText.split('\\n').slice(1);
                    const container = document.getElementById('live-data-container');
                    container.innerHTML = "";
                    
                    rows.forEach(line => {{
                        if (!line.trim()) return;
                        // Regex to split by comma but ignore commas inside quotes
                        const matches = line.match(/(".*?"|[^",\\s]+)(?=\\s*,|\\s*$)/g);
                        const parts = matches ? matches.map(m => m.replace(/^"|"$/g, "").trim()) : [];
                        
                        if (parts.length >= 2) {{
                            const name = parts[0];
                            const price = parts[1];
                            const description = parts[2] || "Premium service package.";
                            const wa_text = encodeURIComponent(`Hello {biz_name}, I want to book the ${{name}} (Price: ${{price}}). Please guide.`);

                            container.innerHTML += `
                            <div class="bg-white p-8 rounded-[3rem] border border-slate-100 shadow-2xl transition-all hover:scale-[1.03] flex flex-col justify-between">
                                <div>
                                    <span class="inline-block px-4 py-1 bg-slate-100 rounded-full text-[10px] font-black uppercase tracking-widest text-slate-500 mb-4">Official Package</span>
                                    <h3 class="text-2xl font-black mb-2 uppercase text-p" style="color:{p_color}">${{name}}</h3>
                                    <p class="text-blue-600 font-black text-2xl mb-6 tracking-tighter underline decoration-4 decoration-slate-100 underline-offset-8">${{price}}</p>
                                    <p class="text-slate-500 text-sm leading-relaxed mb-10">${{description}}</p>
                                </div>
                                <a href="{wa_base_url}${{wa_text}}" target="_blank" class="btn-s" style="background:{s_color}">BOOK SERVICE</a>
                            </div>`;
                        }}
                    }});
                }} catch (e) {{ console.log("E-commerce offline"); }}
            }}
            window.onload = fetchLiveData;
            </script>
            """

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    {v_tag}
    <title>{title} | {biz_name}</title>
    <meta name="description" content="{desc}">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family={h_font.replace(' ', '+')}:wght@700;900&family={b_font.replace(' ', '+')}:wght@400;700&display=swap" rel="stylesheet">
    <style>{theme_css}</style>
</head>
<body class="bg-white flex flex-col min-h-screen text-slate-900">
    <nav class="glass-nav sticky top-0 z-50 p-4 md:p-6">
        <div class="max-w-[1440px] mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
            <a href="index.html" class="flex items-center">{logo_html}</a>
            <div class="flex items-center space-x-6 md:space-x-10 text-[10px] md:text-xs font-black uppercase tracking-widest text-slate-600">
                <a href="index.html" class="hover:text-blue-600">Home</a> <a href="about.html">About</a> <a href="contact.html">Contact</a>
                <a href="tel:{biz_phone}" class="bg-slate-900 text-white px-6 py-2 rounded-full font-bold">Call</a>
            </div>
        </div>
    </nav>
    <main class="flex-grow">{content}</main>
    <a href="{wa_base_url}Hello%20{biz_name.replace(' ', '%20')}" class="wa-float" target="_blank"><svg style="width:38px;height:38px" viewBox="0 0 24 24"><path fill="currentColor" d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91c0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.24 8.23c-1.48 0-2.93-.39-4.19-1.15l-.3-.17l-3.12.82l.83-3.04l-.2-.32a8.188 8.188 0 0 1-1.26-4.38c.01-4.54 3.7-8.24 8.25-8.24m-3.53 3.16c-.13 0-.35.05-.54.26c-.19.2-.72.7-.72 1.72s.73 2.01.83 2.14c.1.13 1.44 2.19 3.48 3.07c.49.21.87.33 1.16.43c.49.16.94.13 1.29.08c.4-.06 1.21-.5 1.38-.98c.17-.48.17-.89.12-.98c-.05-.09-.18-.13-.37-.23c-.19-.1-.1.13-.1.13s-1.13-.56-1.32-.66c-.19-.1-.32-.15-.45.05c-.13.2-.51.65-.62.78c-.11.13-.23.15-.42.05c-.19-.1-.8-.3-1.53-.94c-.57-.5-1.02-1.12-1.21-1.45c-.11-.19-.01-.29.09-.38c.09-.08.19-.23.29-.34c.1-.11.13-.19.19-.32c.06-.13.03-.24-.01-.34c-.05-.1-.45-1.08-.62-1.48c-.16-.4-.36-.34-.51-.35c-.11-.01-.25-.01-.4-.01Z"/></svg></a>
    <footer class="bg-slate-950 text-slate-400 py-24 px-10">
        <div class="max-w-[1440px] mx-auto grid md:grid-cols-2 gap-16">
            <div>
                {logo_html.replace('h-12', 'h-8 mb-6 opacity-70')}
                <p class="text-sm leading-relaxed mb-10 max-w-md">{biz_addr}</p>
                <p class="text-[10px] opacity-30 font-black uppercase tracking-widest">Architected By <a href="https://www.kaydiemscriptlab.com" class="text-white underline">Kaydiem Script Lab</a></p>
            </div>
            <div class="md:text-right">
                <h4 class="text-white font-bold mb-4 uppercase text-xs">Technical Support</h4>
                <p class="text-lg font-bold text-white leading-loose">{biz_phone}<br>{biz_email}</p>
            </div>
        </div>
    </footer>
    {dynamic_script}
</body></html>"""

    # --- ENHANCED INDEX ---
    idx_content = f"""
    <section class="hero-mask px-6 text-center text-white">
        <div class="max-w-[1200px] mx-auto">
            <h1 class="hero-title mb-10 uppercase tracking-tighter leading-none">{hero_h}</h1>
            <p class="text-lg md:text-3xl font-light mb-16 max-w-4xl mx-auto opacity-90 leading-tight">{seo_d}</p>
            <a href="#inventory" class="btn-p uppercase tracking-[0.4em] text-[10px] md:text-sm">Explore Packages</a>
        </div>
    </section>

    <section id="inventory" class="py-32 px-6 max-w-[1440px] mx-auto">
        <div class="flex flex-col md:flex-row justify-between items-end mb-20 gap-8">
            <div class="max-w-2xl">
                <h2 class="section-title uppercase tracking-tighter" style="color:var(--p)">Exclusive Offers</h2>
                <p class="text-slate-500 font-bold uppercase tracking-widest text-xs mt-4 italic">Live pricing synced with our Central Event Management Hub.</p>
            </div>
            <a href="tel:{biz_phone}" class="text-sm font-black border-b-4 border-p pb-2 uppercase tracking-widest text-p">Custom Quote Request →</a>
        </div>
        <div id="live-data-container" class="product-grid">
            <p class="p-20 text-center text-slate-400 font-bold animate-pulse tracking-widest">Establishing Secure Connection to Inventory Database...</p>
        </div>
    </section>

    <section class="bg-slate-50 py-32 px-6 border-y text-center">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-5xl font-black mb-12 uppercase tracking-tighter leading-none" style="color:var(--p)">Luxury & Inclusion</h2>
            <p class="text-2xl text-slate-600 mb-12 leading-relaxed italic">"Transforming venues into masterpieces. Specializing in high-end thematic decor for discerning families across New Delhi."</p>
            <a href="about.html" class="font-black text-xs uppercase tracking-[0.4em] underline decoration-p decoration-4 underline-offset-8">Read Our Full History</a>
        </div>
    </section>
    """

    # --- ZIP ---
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "a", zipfile.ZIP_DEFLATED, False) as zf:
        zf.writestr("index.html", get_layout("Home", seo_d, idx_content, True))
        zf.writestr("about.html", get_layout("About", "History", f"<section class='max-w-7xl mx-auto py-32 px-6'><h1 class='legal-bold-title'>Our Heritage</h1><div class='text-xl md:text-2xl leading-relaxed text-slate-700 legal-text'>{about_txt}</div></section>"))
        zf.writestr("privacy.html", get_layout("Privacy", "Legal", f"<div class='max-w-4xl mx-auto py-32 px-10'><h1 class='legal-bold-title'>Privacy Policy</h1><div class='text-lg legal-text'>{priv_body}</div></div>"))
        zf.writestr("terms.html", get_layout("Terms", "Legal", f"<div class='max-w-4xl mx-auto py-32 px-10'><h1 class='legal-bold-title'>Terms & Conditions</h1><div class='text-lg legal-text'>{terms_body}</div></div>"))
        zf.writestr("contact.html", get_layout("Contact", "Location", f"<section class='max-w-[1440px] mx-auto py-32 px-6 text-center'><h1 class='legal-bold-title'>Connect with Us</h1><div class='grid md:grid-cols-2 gap-16 text-left'><div class='bg-slate-950 p-12 md:p-24 text-white' style='border-radius: var(--radius)'><p class='text-4xl font-black mb-8'>{biz_phone}</p><p class='text-2xl mb-12 opacity-80'>{biz_addr}</p></div><div class='rounded-[3rem] overflow-hidden border shadow-2xl bg-slate-100'>{map_iframe}</div></div></section>"))
        zf.writestr("404.html", get_layout("404", "Not Found", "<div class='py-64 text-center'><h1 class='text-[120px] font-black uppercase tracking-widest'>404</h1></div>"))
        zf.writestr("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {prod_url}sitemap.xml")
        zf.writestr("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{prod_url}index.html</loc></url></urlset>')

    st.success("💎 TITAN SUPREME v7.0 E-COMMERCE READY. Parsing fixed.")
    st.download_button("📥 DOWNLOAD ENTERPRISE BIZ PACKAGE", zip_buf.getvalue(), f"{biz_name.lower()}_v7_0.zip")
