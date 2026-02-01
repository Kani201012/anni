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

# --- 2. ADVANCED UI SYSTEM (Streamlit Admin UI) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; color: #1e293b; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #e2e8f0; padding: 8px; border-radius: 12px; }
    .stButton>button {
        width: 100%; border-radius: 8px; height: 3.5rem;
        background: linear-gradient(135deg, #0f172a 0%, #2563eb 100%);
        color: white; font-weight: 800; border: none; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
    }
    /* Preview Radio Buttons styling */
    div[role="radiogroup"] { display: flex; gap: 10px; }
    div[role="radiogroup"] label { background: white; padding: 5px 15px; border-radius: 20px; border: 1px solid #cbd5e1; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: THE CONTROL CENTER ---
with st.sidebar:
    st.title("Titan v26.2")
    st.caption("Universal Modular Engine")
    st.divider()
    
    with st.expander("🎨 Visual DNA", expanded=True):
        theme_mode = st.selectbox("Select Theme", [
            "Clean Corporate (Light)", 
            "Midnight SaaS (Dark)", 
            "Emerald Forest", 
            "Cyber Neon", 
            "Sunset Luxury", 
            "Nordic Frost", 
            "Rose Gold"
        ])
        
        # Theme Logic Colors
        defaults = {"Light":("#0F172A","#3B82F6"), "Dark":("#F8FAFC","#60A5FA"), "Emerald":("#064E3B","#10B981"), 
                    "Cyber":("#00FF41","#0D0D0D"), "Sunset":("#7C2D12","#F97316"), "Nordic":("#1E3A8A","#60A5FA"), "Rose":("#831843","#FB7185")}
        
        # Set colors based on theme selection
        p_def = defaults["Light"][0]
        s_def = defaults["Light"][1]
        if "Dark" in theme_mode: p_def, s_def = defaults["Dark"]
        elif "Emerald" in theme_mode: p_def, s_def = defaults["Emerald"]
        elif "Cyber" in theme_mode: p_def, s_def = defaults["Cyber"]
        elif "Sunset" in theme_mode: p_def, s_def = defaults["Sunset"]
        elif "Nordic" in theme_mode: p_def, s_def = defaults["Nordic"]
        elif "Rose" in theme_mode: p_def, s_def = defaults["Rose"]

        p_color = st.color_picker("Primary Brand Color", p_def) 
        s_color = st.color_picker("Accent (Buttons/Links)", s_def)  
        
        h_font = st.selectbox("Heading Font", ["Space Grotesk", "Montserrat", "Playfair Display", "Oswald"])
        b_font = st.selectbox("Body Font", ["Inter", "Roboto", "Satoshi", "Lora"])
        border_rad = st.select_slider("Corner Radius", ["0px", "4px", "12px", "24px", "40px"], value="12px")

    with st.expander("🧩 Section Manager", expanded=False):
        show_stats = st.checkbox("Trust Stats", value=True)
        show_features = st.checkbox("Feature Grid", value=True)
        show_inventory = st.checkbox("Inventory (CSV)", value=True)
        show_testimonials = st.checkbox("Testimonials", value=True)
        show_faq = st.checkbox("F.A.Q.", value=True)

    with st.expander("⚙️ Technical SEO", expanded=False):
        gsc_tag = st.text_input("GSC Verification ID")
        og_image = st.text_input("OG Share Image URL")

# --- 4. MAIN WORKSPACE ---
tabs = st.tabs(["1. Identity", "2. Content", "3. Inventory", "4. Legal"])

with tabs[0]:
    c1, c2 = st.columns(2)
    biz_name = c1.text_input("Business Name", "Nova Dynamics")
    biz_phone = c1.text_input("Phone", "+1 (555) 000-0000")
    biz_email = c1.text_input("Email", "hello@novadynamics.io")
    biz_addr = c2.text_area("Address", "101 Tech Plaza, Silicon Valley, CA", height=68)
    prod_url = c2.text_input("Production URL", "https://novadynamics.io")
    seo_d = st.text_input("Meta Description", "Premium services provided by Nova Dynamics.")
    logo_url = st.text_input("Logo URL (Leave blank for text-logo)")
    map_iframe = st.text_area("Map Embed Code", placeholder="Paste <iframe> from Google Maps")

with tabs[1]:
    hero_h = st.text_input("Hero Headline", "Build Faster. Scale Smarter.")
    hero_sub = st.text_input("Hero Subtext", "The all-in-one solution for modern enterprises.")
    hero_img = st.text_input("Hero BG Image", "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&q=80&w=1600")
    feat_data = st.text_area("Features (Title | Description)", "Global Reach | 50+ Countries.\n24/7 Support | Always Online.", height=100)
    about_h = st.text_input("About Title", "Our Legacy")
    about_txt = st.text_area("About Story", "Nova Dynamics has revolutionized...", height=150)
    about_img = st.text_input("About Image", "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&q=80&w=1600")

with tabs[2]:
    sheet_url = st.text_input("Google Sheet CSV Link")
    custom_feat = st.text_input("Default Product Fallback Image", "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&q=80&w=800")

with tabs[3]:
    testi_data = st.text_area("Testimonials (Name | Quote)", "CEO | Amazing work.", height=100)
    faq_data = st.text_area("FAQ (Q? ? A)", "Secure? ? Yes.", height=100)
    priv_txt = st.text_area("Privacy Policy", "Data usage details...", height=100)
    term_txt = st.text_area("Terms", "Terms of use...", height=100)

# --- 5. COMPILER ENGINE ---

def get_theme_css():
    # Dynamic CSS Variables based on Theme
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
    body {{ background: var(--bg); color: var(--txt); font-family: var(--b-font); margin: 0; line-height: 1.6; }}
    h1, h2, h3 {{ font-family: var(--h-font); color: var(--p); }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
    nav {{ position: fixed; top: 0; width: 100%; z-index: 999; background: var(--nav); backdrop-filter: blur(10px); padding: 1rem 0; border-bottom: 1px solid rgba(128,128,128,0.1); }}
    .btn {{ display: inline-block; padding: 0.8rem 2rem; border-radius: var(--radius); font-weight: 700; text-decoration: none; transition: 0.3s; }}
    .btn-accent {{ background: var(--s); color: white !important; }}
    .hero {{ padding: 150px 0 100px; text-align: center; background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{hero_img}'); background-size: cover; color: white; }}
    .hero h1 {{ color: white; font-size: 4rem; }}
    section {{ padding: 80px 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
    
    /* PRODUCT CARD FIX - NO TRUNCATION */
    .card {{ background: var(--card); padding: 25px; border-radius: var(--radius); border: 1px solid rgba(128,128,128,0.1); transition: 0.3s; display: flex; flex-direction: column; }}
    .card img {{ width: 100%; height: 200px; object-fit: cover; border-radius: 10px; margin-bottom: 15px; }}
    .card h3 {{ margin: 0 0 10px; font-size: 1.4rem; }}
    .card p {{ font-size: 0.95rem; opacity: 0.8; margin-bottom: 20px; flex-grow: 1; }} /* flex-grow ensures button stays at bottom */
    
    /* FOOTER FIX - NO BLUE LINKS */
    footer {{ background: var(--p); color: white; padding: 60px 0; }}
    footer a {{ color: rgba(255,255,255,0.7) !important; text-decoration: none !important; }}
    footer a:hover {{ color: white !important; }}
    """

def gen_nav():
    logo = f'<img src="{logo_url}" height="40">' if logo_url else f'<span style="font-weight:900; font-size:1.5rem; color:var(--p)">{biz_name}</span>'
    return f"""<nav><div class="container" style="display:flex; justify-content:space-between; align-items:center;">
    <a href="index.html" style="text-decoration:none;">{logo}</a>
    <div style="display:flex; gap:20px; align-items:center;">
        <a href="index.html" style="color:var(--txt); text-decoration:none;">Home</a>
        <a href="about.html" style="color:var(--txt); text-decoration:none;">About</a>
        <a href="contact.html" style="color:var(--txt); text-decoration:none;">Contact</a>
        <a href="tel:{biz_phone}" class="btn btn-accent">CALL NOW</a>
    </div></div></nav>"""

def gen_inventory_block():
    if not show_inventory: return ""
    return f"""<section id="inventory" style="background:rgba(0,0,0,0.02);"><div class="container">
    <h2 style="text-align:center; margin-bottom:50px;">Live Inventory</h2>
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
                const row = lines[i].match(/(".*?"|[^",\s]+)(?=\s*,|\s*$)/g);
                if(!row || row.length < 2) continue;
                const clean = row.map(v => v.replace(/^"|"$/g, '').trim());
                let img = (clean[3] && clean[3].length > 10) ? clean[3] : (clean[6] && clean[6].length > 10 ? clean[6] : '{custom_feat}');
                grid.innerHTML += `
                <div class="card">
                    <img src="${{img}}" onerror="this.src='{custom_feat}'">
                    <h3>${{clean[0]}}</h3>
                    <p style="font-weight:bold; color:var(--s);">${{clean[1]}}</p>
                    <p>${{clean[2] || ''}}</p>
                    <a href="https://wa.me/{biz_phone.replace(' ','').replace('+','')}?text=Interest: ${{clean[0]}}" class="btn btn-accent" style="text-align:center;">Order Now</a>
                </div>`;
            }}
        }} catch(e) {{ console.log(e); }}
    }}
    window.onload = loadInv;
    </script>"""

def build_page(title, content):
    css = get_theme_css()
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{title} | {biz_name}</title>
    <meta name="description" content="{seo_d}"><style>{css}</style>
    <link href="https://fonts.googleapis.com/css2?family={h_font.replace(' ','+')}&family={b_font.replace(' ','+')}&display=swap" rel="stylesheet">
    </head><body>{gen_nav()}{content}
    <footer><div class="container grid">
        <div><h3>{biz_name}</h3><p>{biz_addr}</p></div>
        <div><h4>Links</h4><a href="about.html">About Us</a><br><a href="contact.html">Contact</a></div>
        <div><h4>Legal</h4><a href="privacy.html">Privacy Policy</a><br><a href="terms.html">Terms</a></div>
    </div></footer></body></html>"""

# --- 6. PAGE CONTENT GENERATORS ---
def gen_home_content():
    c = f'<section class="hero"><div class="container"><h1>{hero_h}</h1><p>{hero_sub}</p><a href="#inventory" class="btn btn-accent">View Products</a></div></section>'
    if show_features:
        f_cards = "".join([f'<div class="card"><h3>{l.split("|")[0]}</h3><p>{l.split("|")[1]}</p></div>' for l in feat_data.split('\n') if "|" in l])
        c += f'<section id="features"><div class="container"><h2 style="text-align:center;">Expertise</h2><div class="grid">{f_cards}</div></div></section>'
    c += gen_inventory_block()
    return c

def gen_about_content():
    return f'<section class="hero" style="min-height:40vh;"><h1>{about_h}</h1></section><section><div class="container grid" style="grid-template-columns: 1fr 1fr;"><div><p>{about_txt}</p></div><img src="{about_img}" style="width:100%; border-radius:12px;"></div></section>'

def gen_contact_content():
    return f'<section class="hero" style="min-height:40vh;"><h1>Get in Touch</h1></section><section><div class="container grid"><div><h2>Contact Us</h2><p><b>Phone:</b> {biz_phone}</p><p><b>Email:</b> {biz_email}</p><p><b>Address:</b> {biz_addr}</p></div><div>{map_iframe}</div></div></section>'

# --- 7. PREVIEW & DEPLOY ---
st.divider()
st.subheader("🚀 Live Multi-Page Preview")
prev_page = st.radio("Switch Page to Preview", ["Home", "About", "Contact", "Privacy", "Terms"], horizontal=True)

if prev_page == "Home": html = build_page("Home", gen_home_content())
elif prev_page == "About": html = build_page("About", gen_about_content())
elif prev_page == "Contact": html = build_page("Contact", gen_contact_content())
elif prev_page == "Privacy": html = build_page("Privacy", f'<section><div class="container"><h1>Privacy Policy</h1><p>{priv_txt}</p></div></section>')
else: html = build_page("Terms", f'<section><div class="container"><h1>Terms</h1><p>{term_txt}</p></div></section>')

st.components.v1.html(html, height=600, scrolling=True)

if st.button("🚀 DEPLOY FULL PACKAGE"):
    z_b = io.BytesIO()
    with zipfile.ZipFile(z_b, "a", zipfile.ZIP_DEFLATED, False) as zf:
        zf.writestr("index.html", build_page("Home", gen_home_content()))
        zf.writestr("about.html", build_page("About", gen_about_content()))
        zf.writestr("contact.html", build_page("Contact", gen_contact_content()))
        zf.writestr("privacy.html", build_page("Privacy", f'<section><div class="container"><h1>Privacy Policy</h1><p>{priv_txt}</p></div></section>'))
        zf.writestr("terms.html", build_page("Terms", f'<section><div class="container"><h1>Terms</h1><p>{term_txt}</p></div></section>'))
    st.download_button("📥 Download Final Zip", z_b.getvalue(), f"{biz_name.lower().replace(' ','_')}_v26.zip")
