import streamlit as st
import zipfile
import io
import json

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="Titan v26.2 | Sovereign Builder", 
    layout="wide", 
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# --- 2. ADMIN UI CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #e2e8f0; padding: 8px; border-radius: 12px; }
    /* Preview Switcher Styling */
    div[role="radiogroup"] { display: flex; gap: 10px; background: #f1f5f9; padding: 10px; border-radius: 15px; border: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: THE CONTROL CENTER ---
with st.sidebar:
    st.title("Titan Architect")
    st.caption("v26.2 | Full Feature Build")
    st.divider()
    
    with st.expander("🎨 Visual DNA & Themes", expanded=True):
        theme_mode = st.selectbox("Select Theme", [
            "Clean Corporate (Light)", "Midnight SaaS (Dark)", 
            "Emerald Forest", "Cyber Neon", "Sunset Luxury", 
            "Nordic Frost", "Rose Gold"
        ])
        
        # Color Logic for Themes
        presets = {
            "Clean Corporate (Light)": ("#0F172A", "#3B82F6"),
            "Midnight SaaS (Dark)": ("#F8FAFC", "#60A5FA"),
            "Emerald Forest": ("#064E3B", "#10B981"),
            "Cyber Neon": ("#00FF41", "#0D0D0D"),
            "Sunset Luxury": ("#7C2D12", "#F97316"),
            "Nordic Frost": ("#1E3A8A", "#60A5FA"),
            "Rose Gold": ("#831843", "#FB7185")
        }
        p_def, s_def = presets[theme_mode]
        p_color = st.color_picker("Primary Brand Color", p_def) 
        s_color = st.color_picker("Accent (Buttons/Links)", s_def)  
        
        h_font = st.selectbox("Heading Font", ["Space Grotesk", "Montserrat", "Playfair Display", "Oswald"])
        b_font = st.selectbox("Body Font", ["Inter", "Roboto", "Satoshi", "Lora"])
        border_rad = st.select_slider("Corner Radius", ["0px", "4px", "12px", "24px", "40px"], value="12px")

    with st.expander("🧩 Section Manager", expanded=False):
        show_hero = st.checkbox("Hero Header", value=True)
        show_stats = st.checkbox("Trust Stats", value=True)
        show_features = st.checkbox("Feature Grid", value=True)
        show_inventory = st.checkbox("Inventory (CSV)", value=True)
        show_faq = st.checkbox("F.A.Q.", value=True)

# --- 4. MAIN WORKSPACE ---
tabs = st.tabs(["1. Identity", "2. Content Blocks", "3. Inventory", "4. Legal"])

with tabs[0]:
    c1, c2 = st.columns(2)
    biz_name = c1.text_input("Business Name", "Nova Dynamics")
    biz_phone = c1.text_input("Phone Number", "+1 (555) 000-0000")
    biz_email = c1.text_input("Email Address", "hello@novadynamics.io")
    biz_addr = c2.text_area("Physical Address", "101 Tech Plaza, Silicon Valley, CA")
    prod_url = c2.text_input("Website URL", "https://novadynamics.io")
    seo_d = st.text_input("Meta Description", "High-performance solutions for modern industries.")
    logo_url = st.text_input("Logo URL (PNG/SVG)")
    map_iframe = st.text_area("Map Embed Code", placeholder="Paste <iframe> from Google Maps")

with tabs[1]:
    hero_h = st.text_input("Hero Headline", "Build Faster. Scale Smarter.")
    hero_sub = st.text_input("Hero Subtext", "The all-in-one solution for modern enterprises.")
    hero_img = st.text_input("Hero BG Image", "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&q=80&w=1600")
    feat_data = st.text_area("Features (Title | Description)", "Global Reach | 50+ Countries.\n24/7 Support | Always here.", height=100)
    about_h = st.text_input("About Page Title", "Our Legacy")
    about_txt = st.text_area("About Story", "Founded on principles of excellence...", height=150)
    about_img = st.text_input("About Page Side Image", "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&q=80&w=1600")

with tabs[2]:
    sheet_url = st.text_input("Google Sheet CSV Link")
    custom_feat = st.text_input("Default Product Image", "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&q=80&w=800")
    wa_num = st.text_input("WhatsApp Number (Digits Only, e.g. 15550000000)", biz_phone.replace(" ","").replace("+","").replace("-","").replace("(","").replace(")",""))

with tabs[3]:
    testi_data = st.text_area("Testimonials (Name | Quote)", "CEO, Acme | Amazing work.", height=100)
    faq_data = st.text_area("FAQ (Q? ? A)", "Is it secure? ? Yes, 100%.", height=100)
    priv_txt = st.text_area("Privacy Policy", "Your data is safe...", height=100)
    term_txt = st.text_area("Terms of Service", "By using this site...", height=100)

# --- 5. COMPILER ENGINE ---

def get_theme_css():
    is_dark = any(x in theme_mode for x in ["Dark", "Cyber", "Midnight"])
    bg = "#0f172a" if is_dark else "#ffffff"
    txt = "#f1f5f9" if is_dark else "#0f172a"
    card = "rgba(30, 41, 59, 0.7)" if is_dark else "#ffffff"
    nav = "rgba(15, 23, 42, 0.9)" if is_dark else "rgba(255, 255, 255, 0.9)"
    
    return f"""
    :root {{
        --p: {p_color}; --s: {s_color}; --bg: {bg}; --txt: {txt}; --card: {card};
        --radius: {border_rad}; --nav: {nav};
        --h-font: '{h_font}', sans-serif; --b-font: '{b_font}', sans-serif;
    }}
    body {{ background: var(--bg); color: var(--txt); font-family: var(--b-font); margin: 0; line-height: 1.6; overflow-x: hidden; }}
    h1, h2, h3, h4 {{ font-family: var(--h-font); color: var(--p); }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
    nav {{ position: fixed; top: 0; width: 100%; z-index: 999; background: var(--nav); backdrop-filter: blur(10px); padding: 1.2rem 0; border-bottom: 1px solid rgba(128,128,128,0.1); }}
    .btn {{ display: inline-block; padding: 0.8rem 2.2rem; border-radius: var(--radius); font-weight: 700; text-decoration: none; transition: 0.3s; border: none; cursor: pointer; }}
    .btn-accent {{ background: var(--s); color: white !important; }}
    .hero {{ padding: 180px 0 100px; text-align: center; background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{hero_img}'); background-size: cover; background-position: center; color: white; }}
    .hero h1 {{ color: white; font-size: clamp(2.5rem, 5vw, 4rem); }}
    section {{ padding: 100px 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }}
    
    /* CARDS - FULL DESCRIPTION FIX */
    .card {{ background: var(--card); padding: 30px; border-radius: var(--radius); border: 1px solid rgba(128,128,128,0.15); transition: 0.3s; display: flex; flex-direction: column; height: 100%; }}
    .card img {{ width: 100%; height: 220px; object-fit: cover; border-radius: calc(var(--radius) - 4px); margin-bottom: 20px; }}
    .card p {{ font-size: 0.95rem; opacity: 0.8; margin-bottom: 25px; flex-grow: 1; }}
    
    /* FOOTER - NO MORE UGLY BLUE LINKS */
    footer {{ background: var(--p); color: white; padding: 80px 0; margin-top: 50px; }}
    footer h3, footer h4 {{ color: white; }}
    footer a {{ color: rgba(255,255,255,0.7) !important; text-decoration: none !important; transition: 0.3s; }}
    footer a:hover {{ color: white !important; }}
    .footer-grid {{ display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 50px; }}
    
    /* WhatsApp Floating Button */
    .wa-float {{ position: fixed; bottom: 30px; right: 30px; background: #25d366; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 30px rgba(37,211,102,0.4); z-index: 10000; text-decoration: none; }}
    @media (max-width: 768px) {{ .footer-grid {{ grid-template-columns: 1fr; }} }}
    """

def gen_nav():
    logo = f'<img src="{logo_url}" height="40">' if logo_url else f'<span style="font-weight:900; font-size:1.5rem; color:var(--p)">{biz_name}</span>'
    return f"""<nav><div class="container" style="display:flex; justify-content:space-between; align-items:center;">
    <a href="index.html" style="text-decoration:none;">{logo}</a>
    <div style="display:flex; gap:25px; align-items:center;">
        <a href="index.html" style="color:var(--txt); text-decoration:none; font-weight:600;">Home</a>
        <a href="about.html" style="color:var(--txt); text-decoration:none; font-weight:600;">About</a>
        <a href="contact.html" style="color:var(--txt); text-decoration:none; font-weight:600;">Contact</a>
        <a href="tel:{biz_phone}" class="btn btn-accent">CALL NOW</a>
    </div></div></nav>"""

def gen_inventory_block():
    if not show_inventory: return ""
    return f"""<section id="inventory" style="background:rgba(0,0,0,0.02);"><div class="container">
    <h2 style="text-align:center; margin-bottom:60px; font-size:2.5rem;">Live Inventory</h2>
    <div id="inv-grid" class="grid"><p style="text-align:center; grid-column: 1/-1;">Loading Items...</p></div>
    </div></section>
    <script>
    async function loadInv() {{
        try {{
            const res = await fetch('{sheet_url}');
            const txt = await res.text();
            const lines = txt.split(/\\r?\\n/);
            const grid = document.getElementById('inv-grid');
            if(!grid) return;
            grid.innerHTML = '';
            for(let i=1; i<lines.length; i++) {{
                const row = lines[i].match(/(".*?"|[^",\\s]+)(?=\\s*,|\\s*$)/g);
                if(!row || row.length < 2) continue;
                const clean = row.map(v => v.replace(/^"|"$/g, '').trim());
                let img = (clean[3] && clean[3].length > 10) ? clean[3] : (clean[6] && clean[6].length > 10 ? clean[6] : '{custom_feat}');
                grid.innerHTML += `
                <div class="card">
                    <img src="${{img}}" onerror="this.src='{custom_feat}'">
                    <h3 style="color:var(--p)">${{clean[0]}}</h3>
                    <p style="font-weight:bold; color:var(--s); margin:5px 0 15px;">${{clean[1]}}</p>
                    <p>${{clean[2] || ''}}</p>
                    <a href="https://wa.me/{wa_num}?text=I am interested in: ${{clean[0]}}" class="btn btn-accent" style="text-align:center;">Order on WhatsApp</a>
                </div>`;
            }}
        }} catch(e) {{ console.log(e); }}
    }}
    window.onload = loadInv;
    </script>"""

def build_page(title, content):
    css = get_theme_css()
    wa_btn = f'<a href="https://wa.me/{wa_num}" class="wa-float" target="_blank"><svg style="width:32px;height:32px" viewBox="0 0 24 24"><path fill="currentColor" d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91c0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.24 8.23c-1.48 0-2.93-.39-4.19-1.15l-.3-.17l-3.12.82l.83-3.04l-.2-.32a8.188 8.188 0 0 1-1.26-4.38c.01-4.54 3.7-8.24 8.25-8.24m-3.53 3.16c-.13 0-.35.05-.54.26c-.19.2-.72.7-.72 1.72s.73 2.01.83 2.14c.1.13 1.44 2.19 3.48 3.07c.49.21.87.33 1.16.43c.49.16.94.13 1.29.08c.4-.06 1.21-.5 1.38-.98c.17-.48.17-.89.12-.98c-.05-.09-.18-.13-.37-.23c-.19-.1-.1.13-.1.13s-1.13-.56-1.32-.66c-.19-.1-.32-.15-.45.05c-.13.2-.51.65-.62.78c-.11.13-.23.15-.42.05c-.19-.1-.8-.3-1.53-.94c-.57-.5-1.02-1.12-1.21-1.45c-.11-.19-.01-.29.09-.38c.09-.08.19-.23.29-.34c.1-.11.13-.19.19-.32c.06-.13.03-.24-.01-.34c-.05-.1-.45-1.08-.62-1.48c-.16-.4-.36-.34-.51-.35c-.11-.01-.25-.01-.4-.01Z"/></svg></a>'
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title} | {biz_name}</title>
    <meta name="description" content="{seo_d}"><style>{css}</style>
    <link href="https://fonts.googleapis.com/css2?family={h_font.replace(' ','+')}&family={b_font.replace(' ','+')}&display=swap" rel="stylesheet">
    </head><body>{gen_nav()}{content}{wa_btn}
    <footer><div class="container footer-grid">
        <div><h3>{biz_name}</h3><p>{biz_addr}</p><p>{biz_email}</p></div>
        <div><h4>Links</h4><a href="index.html">Home</a><br><a href="about.html">About Us</a><br><a href="contact.html">Contact</a></div>
        <div><h4>Legal</h4><a href="privacy.html">Privacy Policy</a><br><a href="terms.html">Terms</a></div>
    </div><div style="text-align:center; padding-top:40px; opacity:0.3; font-size:0.8rem;">&copy; {biz_name}. All Rights Reserved.</div></footer></body></html>"""

# --- 6. PAGE CONTENT GENERATORS ---
def gen_home_content():
    c = ""
    if show_hero: c += f'<section class="hero"><div class="container"><h1>{hero_h}</h1><p style="font-size:1.2rem; margin-bottom:30px;">{hero_sub}</p><a href="#inventory" class="btn btn-accent">Explore Inventory</a></div></section>'
    if show_stats: c += f'<div style="background:var(--p); color:white; padding:50px 0;"><div class="container grid" style="text-align:center;"><div><h2>10+</h2><p>Years</p></div><div><h2>500+</h2><p>Clients</p></div><div><h2>100%</h2><p>Secure</p></div></div></div>'
    if show_features:
        f_cards = "".join([f'<div class="card"><h3>{l.split("|")[0].strip()}</h3><p>{l.split("|")[1].strip()}</p></div>' for l in feat_data.split('\n') if "|" in l])
        c += f'<section id="features"><div class="container"><h2 style="text-align:center; margin-bottom:50px;">Core Expertise</h2><div class="grid">{f_cards}</div></div></section>'
    c += gen_inventory_block()
    return c

# --- 7. RENDER PREVIEW & DEPLOY ---
st.divider()
st.subheader("🚀 Live Multi-Page Preview")
prev_page = st.radio("Select Page to View:", ["Home", "About", "Contact", "Privacy", "Terms"], horizontal=True)

# Generate strings for switcher to avoid NameError
abt_page = f'<section class="hero" style="min-height:40vh;"><h1>{about_h}</h1></section><section><div class="container grid" style="grid-template-columns: 1.2fr 0.8fr; align-items:center;"><div><p style="font-size:1.1rem;">{about_txt}</p></div><img src="{about_img}" style="width:100%; border-radius:12px; box-shadow:0 20px 40px rgba(0,0,0,0.1);"></div></section>'
con_page = f'<section class="hero" style="min-height:40vh;"><h1>Get in Touch</h1></section><section><div class="container grid"><div><h2>Contact Details</h2><p><b>Phone:</b> {biz_phone}</p><p><b>Email:</b> {biz_email}</p><p><b>Address:</b> {biz_addr}</p></div><div>{map_iframe}</div></div></section>'

if prev_page == "Home": html = build_page("Home", gen_home_content())
elif prev_page == "About": html = build_page("About", abt_page)
elif prev_page == "Contact": html = build_page("Contact", con_page)
elif prev_page == "Privacy": html = build_page("Privacy", f'<section><div class="container"><h1>Privacy Policy</h1><p>{priv_txt}</p></div></section>')
else: html = build_page("Terms", f'<section><div class="container"><h1>Terms of Service</h1><p>{term_txt}</p></div></section>')

st.components.v1.html(html, height=700, scrolling=True)

if st.button("🚀 DEPLOY & DOWNLOAD ASSET PACKAGE", type="primary"):
    z_b = io.BytesIO()
    with zipfile.ZipFile(z_b, "a", zipfile.ZIP_DEFLATED, False) as zf:
        zf.writestr("index.html", build_page("Home", gen_home_content()))
        zf.writestr("about.html", build_page("About", abt_page))
        zf.writestr("contact.html", build_page("Contact", con_page))
        zf.writestr("privacy.html", build_page("Privacy Policy", f'<section><div class="container"><h1>Privacy Policy</h1><p>{priv_txt}</p></div></section>'))
        zf.writestr("terms.html", build_page("Terms of Service", f'<section><div class="container"><h1>Terms of Service</h1><p>{term_txt}</p></div></section>'))
    st.download_button("📥 Click to Download Website", z_b.getvalue(), f"{biz_name.lower().replace(' ','_')}_site.zip")
