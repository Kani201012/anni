import streamlit as st
import zipfile
import io
import json
from datetime import datetime

# --- 1. DESIGN STUDIO CONFIGURATION ---
st.set_page_config(page_title="Kaydiem Titan v5.1 | Supreme Web Architect", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    .main { background: #0f172a; color: white; }
    .stTabs [data-baseweb="tab"] { color: white; font-weight: bold; font-size: 1.1rem; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 4em; 
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
        color: white; font-weight: 900; border: none; font-size: 1.4rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); transition: all 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); filter: brightness(1.2); }
    .stExpander { background-color: #1e293b !important; border: 1px solid #334155 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: DESIGN STUDIO ---
with st.sidebar:
    st.image("https://www.gstatic.com/images/branding/product/2x/business_profile_96dp.png", width=50)
    st.title("Titan v5.1 Studio")
    
    with st.expander("🎭 1. Layout & DNA", expanded=True):
        layout_dna = st.selectbox("Design DNA", ["Industrial Titan", "Classic Royal", "Soft-UI", "Glass-Tech", "Brutalist"])
        p_color = st.color_picker("Primary Brand Color", "#1E293B")
        s_color = st.color_picker("Accent/CTA Color", "#2563EB")
        border_rad = st.select_slider("Corner Roundness", options=["0px", "4px", "12px", "24px", "60px"], value="24px")

    with st.expander("✍️ 2. Typography Studio", expanded=True):
        h_font = st.selectbox("Heading Font", ["Montserrat", "Oswald", "Playfair Display", "Syncopate", "Inter"])
        b_font = st.selectbox("Body Font", ["Inter", "Roboto", "Open Sans", "Lora"])
        h_weight = st.select_slider("Weight", options=["300", "400", "700", "900"], value="900")
        ls = st.select_slider("Letter Spacing", options=["-0.05em", "-0.02em", "0em", "0.05em", "0.1em"], value="-0.02em")

    gsc_tag = st.text_input("GSC Verification Tag")
    st.info("Built by www.kaydiemscriptlab.com")

st.title("🏗️ Kaydiem Titan Supreme Engine v5.1")

# --- 2. MULTI-TAB DATA COLLECTION ---
tabs = st.tabs(["📍 Identity", "🏗️ Content & SEO", "🖼️ Photo Manager", "🌟 Social Proof", "⚖️ Legal Pages"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        biz_name = st.text_input("Business Name (NAP)", "Top Quality Glass & Aluminium")
        biz_phone = st.text_input("Verified Phone", "+966 55 860 7407")
        biz_email = st.text_input("Business Email", "info@business.sa")
    with c2:
        biz_cat = st.text_input("Category", "Industrial Supplier")
        biz_hours = st.text_input("Hours", "Sat-Thu: 08:00 - 18:00")
        prod_url = st.text_input("Production URL", "https://kani201012.github.io/site/")
    
    # NEW: LOGO URL INPUT
    biz_logo = st.text_input("Business Logo URL", placeholder="Paste PNG link or images/logo.png")
    
    biz_addr = st.text_area("Full Maps Physical Address")
    biz_areas = st.text_area("Service Neighborhoods (Comma separated)", 
                            placeholder="Al Olaya, Al Mashael, Malham, Sulay, Riyadh North")
    map_iframe = st.text_area("Map Embed HTML Code (<iframe>)")

with tabs[1]:
    hero_h = st.text_input("Main Hero Headline", "Precision Industrial Excellence")
    seo_d = st.text_input("Meta Description", "Verified industrial solutions for the Riyadh 2030 vision.")
    biz_key = st.text_input("SEO Keywords")
    biz_serv = st.text_area("Services (One per line)")
    about_txt = st.text_area("Our Story (800+ Words for E-E-A-T)", height=250)

with tabs[2]:
    st.header("📸 Premium Photo Management")
    custom_hero = st.text_input("Hero Background Image URL")
    custom_feat = st.text_input("Feature Image URL")
    custom_gall = st.text_input("Gallery Image URL")

with tabs[3]:
    st.header("🌟 Trust Signals")
    testi = st.text_area("Testimonials (Name | Quote)")
    faqs = st.text_area("FAQ (Question? ? Answer)")

with tabs[4]:
    st.header("⚖️ Mandatory Legal Pages")
    priv_body = st.text_area("Privacy Policy Content", height=300)
    terms_body = st.text_area("Terms Content", height=300)

# --- 3. THE SUPREME ENGINE V5.1 ---

if st.button("🚀 DEPLOY MARKET-LEADING BUSINESS ASSET"):
    
    # Image Fallbacks
    img_h = custom_hero if custom_hero else "https://images.unsplash.com/photo-1517420812313-80d6492259ef?auto=format&fit=crop&q=80&w=1600"
    img_f = custom_feat if custom_feat else "https://images.unsplash.com/photo-1590486803833-ffc45744f5bf?auto=format&fit=crop&q=80&w=800"
    img_g = custom_gall if custom_gall else "https://images.unsplash.com/photo-1565011523534-747a8601f10a?auto=format&fit=crop&q=80&w=1600"

    # Logo Logic
    logo_html = f'<img src="{biz_logo}" alt="{biz_name} Logo" class="h-12 w-auto object-contain">' if biz_logo else f'<span class="text-2xl font-black tracking-tighter" style="color:var(--p)">{biz_name}</span>'
    footer_logo = f'<img src="{biz_logo}" alt="{biz_name} Logo" class="h-10 w-auto mb-6 opacity-80">' if biz_logo else f'<h4 class="text-white text-3xl font-black mb-6 tracking-tighter uppercase">{biz_name}</h4>'

    wa_clean = biz_phone.replace(" ", "").replace("+", "")
    wa_url = f"https://wa.me/{wa_clean}?text=Hello%20{biz_name.replace(' ', '%20')},%20I%20am%20interested%20in%20your%20{biz_cat.replace(' ', '%20')}%20services."
    area_list = [a.strip() for a in biz_areas.split(",")]
    schema_areas = json.dumps(area_list)

    theme_css = f"""
    :root {{ --p: {p_color}; --s: {s_color}; --radius: {border_rad}; }}
    body {{ font-family: '{b_font}', sans-serif; color: #0f172a; line-height: 1.8; overflow-x: hidden; width: 100%; }}
    h1, h2, h3 {{ font-family: '{h_font}', sans-serif; font-weight: {h_weight}; letter-spacing: {ls}; text-transform: uppercase; line-height: 1.1; overflow-wrap: break-word; }}
    .hero-title {{ font-size: clamp(2rem, 8vw, 85px); text-shadow: 0 4px 15px rgba(0,0,0,0.4); }}
    .section-title {{ font-size: clamp(1.8rem, 5vw, 65px); }}
    .btn-supreme {{ background: var(--p); color: white; padding: 1.1rem 2.8rem; border-radius: var(--radius); font-weight: 900; transition: all 0.4s; display: inline-block; text-align: center; }}
    .glass-nav {{ background: rgba(255, 255, 255, 0.98); backdrop-filter: blur(15px); border-bottom: 1px solid rgba(0,0,0,0.08); width: 100%; }}
    .hero-mask {{ background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.5)), url('{img_h}'); background-size: cover; background-position: center; min-height: 85vh; display: flex; align-items: center; justify-content: center; }}
    .wa-float {{ position: fixed; bottom: 30px; right: 30px; background: #25d366; color: white; width: 65px; height: 65px; border-radius: 50px; display: flex; align-items: center; justify-content: center; z-index: 99999; box-shadow: 0 10px 25px rgba(37,211,102,0.4); transition: 0.3s; }}
    .legal-text {{ white-space: pre-wrap; word-wrap: break-word; font-size: 1.1rem; color: #334155; }}
    .legal-title {{ font-weight: 900; font-size: clamp(2.5rem, 6vw, 5rem); color: var(--p); margin-bottom: 2rem; text-transform: uppercase; }}
    """

    def get_layout(title, desc, content, is_index=False):
        v_tag = f'<meta name="google-site-verification" content="{gsc_tag}">' if (is_index and gsc_tag) else ""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    {v_tag}
    <title>{title} | {biz_name}</title>
    <meta name="description" content="{desc}"><meta name="keywords" content="{biz_key}">
    <link rel="canonical" href="{prod_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family={h_font.replace(' ', '+')}:wght@700;900&family={b_font.replace(' ', '+')}:wght@400;700&display=swap" rel="stylesheet">
    <style>{theme_css}</style>
    <script type="application/ld+json">
    {{ 
        "@context": "https://schema.org", 
        "@type": "LocalBusiness", 
        "name": "{biz_name}", 
        "logo": "{biz_logo}",
        "address": {{ "@type": "PostalAddress", "streetAddress": "{biz_addr}" }}, 
        "telephone": "{biz_phone}", "url": "{prod_url}", "areaServed": {schema_areas}
    }}
    </script>
</head>
<body class="bg-white flex flex-col min-h-screen text-slate-900">
    <nav class="glass-nav sticky top-0 z-50 p-4 md:p-6">
        <div class="max-w-[1440px] mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
            <a href="index.html" class="flex items-center">{logo_html}</a>
            <div class="flex items-center space-x-6 md:space-x-10 text-[10px] md:text-xs font-black uppercase tracking-widest text-slate-600">
                <a href="index.html" class="hover:text-blue-600">Home</a> 
                <a href="about.html" class="hover:text-blue-600">About</a> 
                <a href="contact.html" class="hover:text-blue-600">Contact</a>
                <a href="tel:{biz_phone}" class="bg-slate-900 text-white px-5 py-2 rounded-full font-bold">Call Now</a>
            </div>
        </div>
    </nav>
    <main class="flex-grow">{content}</main>
    <a href="{wa_url}" class="wa-float" target="_blank">
        <svg style="width:38px;height:38px" viewBox="0 0 24 24"><path fill="currentColor" d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91c0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.24 8.23c-1.48 0-2.93-.39-4.19-1.15l-.3-.17l-3.12.82l.83-3.04l-.2-.32a8.188 8.188 0 0 1-1.26-4.38c.01-4.54 3.7-8.24 8.25-8.24m-3.53 3.16c-.13 0-.35.05-.54.26c-.19.2-.72.7-.72 1.72s.73 2.01.83 2.14c.1.13 1.44 2.19 3.48 3.07c.49.21.87.33 1.16.43c.49.16.94.13 1.29.08c.4-.06 1.21-.5 1.38-.98c.17-.48.17-.89.12-.98c-.05-.09-.18-.13-.37-.23c-.19-.1-.1.13-.1.13s-1.13-.56-1.32-.66c-.19-.1-.32-.15-.45.05c-.13.2-.51.65-.62.78c-.11.13-.23.15-.42.05c-.19-.1-.8-.3-1.53-.94c-.57-.5-1.02-1.12-1.21-1.45c-.11-.19-.01-.29.09-.38c.09-.08.19-.23.29-.34c.1-.11.13-.19.19-.32c.06-.13.03-.24-.01-.34c-.05-.1-.45-1.08-.62-1.48c-.16-.4-.36-.34-.51-.35c-.11-.01-.25-.01-.4-.01Z"/></svg>
    </a>
    <footer class="bg-slate-950 text-slate-400 py-24 px-10 border-t border-slate-900">
        <div class="max-w-[1440px] mx-auto grid md:grid-cols-4 gap-16">
            <div class="col-span-2">
                {footer_logo}
                <p class="text-lg leading-relaxed mb-10 max-w-md">{biz_addr}</p>
                <div class="bg-slate-900/50 p-6 border border-slate-800 rounded-3xl">
                    <h5 class="text-white text-xs font-black uppercase tracking-widest mb-4">Geo-Verification</h5>
                    <div class="flex flex-wrap gap-2">
                        {"".join([f'<span class="bg-slate-800 text-[10px] px-3 py-1 rounded-full uppercase font-bold">{area}</span>' for area in area_list])}
                    </div>
                </div>
                <p class="text-[10px] mt-10 opacity-30 uppercase font-black tracking-widest italic">Built by <a href="https://www.kaydiemscriptlab.com" class="text-white underline">Kaydiem Script Lab</a></p>
            </div>
            <div><h4 class="text-white font-bold mb-8 uppercase text-xs">Navigation</h4>
                <ul class="space-y-4 text-sm font-bold uppercase"><li><a href="privacy.html" class="hover:text-white transition">Privacy Policy</a></li><li><a href="terms.html" class="hover:text-white transition">Terms</a></li></ul>
            </div>
            <div><h4 class="text-white font-bold mb-8 uppercase text-xs">Direct Support</h4><p class="text-lg font-bold text-white leading-loose">{biz_phone}<br>{biz_email}</p></div>
        </div>
    </footer>
</body></html>"""

    # Index Builder
    serv_html = "".join([f'<div class="bg-slate-50 p-10 rounded-[2.5rem] border border-slate-100 shadow-xl"><h3 class="text-2xl font-black mb-4 uppercase" style="color:var(--p)">{s.strip()}</h3><p class="text-slate-500 text-sm leading-relaxed font-bold uppercase tracking-tighter italic">Premium verified solution for {biz_name} projects.</p></div>' for s in biz_serv.splitlines() if s.strip()])
    testi_html = "".join([f'<div class="p-10 bg-slate-50 rounded-[3rem] border border-slate-100 italic text-xl shadow-inner mb-8">"{t.split("|")[1].strip()}"<br><span class="font-black not-italic text-sm block mt-6 uppercase tracking-widest text-brand" style="color:var(--p)">— {t.split("|")[0].strip()} <span class="text-emerald-500 font-black ml-2">● Verified Partner</span></span></div>' for t in testi.splitlines() if "|" in t])
    faq_html = "".join([f'<details class="mb-6 bg-white p-6 rounded-2xl border border-slate-100 cursor-pointer shadow-sm"><summary class="font-black text-lg uppercase tracking-tight">{f.split("?")[0].strip()}?</summary><p class="mt-4 text-slate-600 leading-relaxed font-medium">{f.split("?")[1].strip()}</p></details>' for f in faqs.splitlines() if "?" in f])

    idx_content = f"""
    <section class="hero-mask px-6 text-center text-white">
        <div class="max-w-[1200px] mx-auto">
            <h1 class="hero-title mb-10 uppercase tracking-tighter leading-none">{hero_h}</h1>
            <p class="text-lg md:text-3xl font-light mb-16 max-w-4xl mx-auto opacity-90 leading-tight">{seo_d}</p>
            <a href="tel:{biz_phone}" class="btn-supreme uppercase tracking-[0.4em] text-[10px] md:text-sm shadow-2xl">Connect Now</a>
        </div>
    </section>
    <section class="max-w-[1440px] mx-auto py-24 px-6 text-center">
        <h2 class="section-title mb-20 uppercase tracking-tighter" style="color:var(--p)">Our Expertise</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10 text-left">{serv_html}</div>
    </section>
    <section class="bg-slate-50 py-32 px-6 border-y">
        <div class="max-w-[1440px] mx-auto grid md:grid-cols-2 gap-24 items-center">
            <img src="{img_f}" class="shadow-2xl" style="border-radius: var(--radius)">
            <div>
                <h2 class="text-5xl font-black mb-12 uppercase tracking-tighter leading-none" style="color:var(--p)">Verified 2026 Authority</h2>
                <p class="text-2xl text-slate-600 mb-12 leading-relaxed italic">"Providing the technical foundation for the 2026 Saudi landscape. Precision mixing, certified safety, and direct owner oversight."</p>
                <a href="about.html" class="btn-supreme text-xs tracking-widest uppercase">View Full Story</a>
            </div>
        </div>
    </section>
    <section class="py-32 px-6 max-w-[1440px] mx-auto">
        <div class="grid md:grid-cols-2 gap-24">
            <div><h2 class="text-4xl font-black mb-16 uppercase tracking-tighter" style="color:var(--p)">Partner Success</h2>{testi_html}</div>
            <div><h2 class="text-4xl font-black mb-16 uppercase tracking-tighter" style="color:var(--p)">Expert Insights</h2>{faq_html}</div>
        </div>
    </section>
    """

    # --- ZIP OUTPUT ---
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "a", zipfile.ZIP_DEFLATED, False) as zf:
        zf.writestr("index.html", get_layout("Home", seo_d, idx_content, True))
        zf.writestr("about.html", get_layout("About Us", "History", f"<section class='max-w-7xl mx-auto py-32 px-6'><h1 class='legal-title'>About Us</h1><div class='text-xl md:text-2xl leading-relaxed text-slate-700 legal-text'>{about_txt}</div><img src='{img_g}' class='mt-20 w-full h-[600px] object-cover shadow-2xl' style='border-radius: var(--radius)'></section>"))
        zf.writestr("contact.html", get_layout("Contact", "Location", f"<section class='max-w-[1440px] mx-auto py-32 px-6 text-center'><h1 class='legal-title'>Connect</h1><div class='grid md:grid-cols-2 gap-16 text-left'><div class='bg-slate-950 p-12 md:p-24 text-white' style='border-radius: var(--radius)'><p class='text-4xl font-black mb-8'>{biz_phone}</p><p class='text-2xl mb-12 opacity-80'>{biz_addr}</p></div><div class='rounded-[3rem] overflow-hidden border shadow-2xl bg-slate-100'>{map_iframe}</div></div></section>"))
        zf.writestr("privacy.html", get_layout("Privacy", "Legal", f"<div class='max-w-[1440px] mx-auto py-32 px-10'><h1 class='legal-title'>Privacy Policy</h1><div class='legal-text'>{priv_body}</div></div>"))
        zf.writestr("terms.html", get_layout("Terms", "Legal", f"<div class='max-w-[1440px] mx-auto py-32 px-10'><h1 class='legal-title'>Terms & Conditions</h1><div class='legal-text'>{terms_body}</div></div>"))
        zf.writestr("404.html", get_layout("404", "Not Found", "<div class='py-64 text-center'><h1 class='text-[120px] font-black uppercase tracking-widest'>404</h1></div>"))
        zf.writestr("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {prod_url}sitemap.xml")
        zf.writestr("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{prod_url}index.html</loc></url><url><loc>{prod_url}about.html</loc></url></urlset>')

    st.success("💎 TITAN SUPREME v5.1 DEPLOYED. Logo branding engine active.")
    st.download_button("📥 DOWNLOAD COMPLETE BIZ PACKAGE", zip_buf.getvalue(), f"{biz_name.lower()}_v5_1.zip")
