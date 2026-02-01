import streamlit as st
import zipfile
import io
import urllib.parse

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="Titan v26.5 | Omni Architect", 
    layout="wide", 
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED UI SYSTEM (CSS) ---
st.markdown("""
    <style>
    /* UI Reset & Variables */
    :root { --primary: #0f172a; --accent: #3b82f6; }
    .stApp { background-color: #f8fafc; color: #1e293b; font-family: 'Inter', sans-serif; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    [data-testid="stSidebar"] h1 { 
        background: linear-gradient(90deg, #0f172a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important;
        font-size: 1.8rem !important;
    }
    
    /* Modern Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        color: #0f172a !important;
        transition: all 0.2s ease;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Action Buttons */
    .stButton>button {
        width: 100%; border-radius: 8px; height: 3.5rem;
        background: linear-gradient(135deg, #0f172a 0%, #2563eb 100%);
        color: white; font-weight: 800; border: none;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
        text-transform: uppercase; letter-spacing: 1px;
        transition: transform 0.2s;
    }
    .stButton>button:hover { transform: translateY(-2px); }
    
    /* Preview Frame */
    iframe { border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 20px 40px -10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: THE CONTROL CENTER ---
with st.sidebar:
    st.title("Titan Architect")
    st.caption("v26.5 | Omni Core")
    st.divider()
    
    # 3.1 VISUAL DNA
    with st.expander("🎨 Visual DNA", expanded=True):
        theme_mode = st.selectbox("Base Theme", [
            "Clean Corporate (Light)", 
            "Midnight SaaS (Dark)", 
            "Glassmorphism (Blur)",
            "Cyberpunk Neon",
            "Luxury Gold",
            "Forest Eco",
            "Ocean Breeze",
            "Stark Minimalist"
        ])
        c1, c2 = st.columns(2)
        p_color = c1.color_picker("Primary Brand", "#0F172A") 
        s_color = c2.color_picker("Action (CTA)", "#3B82F6")  
        
        st.markdown("**Typography**")
        h_font = st.selectbox("Headings", ["Space Grotesk", "Montserrat", "Playfair Display", "Oswald", "Clash Display"])
        b_font = st.selectbox("Body Text", ["Inter", "Roboto", "Open Sans", "Satoshi", "Lora"])
        
        st.markdown("**UI Physics**")
        border_rad = st.select_slider("Corner Roundness", ["0px", "4px", "12px", "24px", "40px"], value="12px")
        anim_type = st.selectbox("Animation Style", ["Fade Up", "Zoom In", "Slide Right", "None"])

    # 3.2 MODULE MANAGER
    with st.expander("🧩 Section Manager", expanded=False):
        st.caption("Toggle sections to include:")
        show_hero = st.checkbox("Hero Header", value=True)
        show_stats = st.checkbox("Trust Stats/Logos", value=True)
        show_features = st.checkbox("Feature Grid", value=True)
        show_inventory = st.checkbox("Live Inventory (CSV)", value=True)
        show_gallery = st.checkbox("Visual Gallery (About)", value=True)
        show_testimonials = st.checkbox("Testimonials", value=True)
        show_faq = st.checkbox("F.A.Q.", value=True)
        show_cta = st.checkbox("Final Call to Action", value=True)

    # 3.3 TECHNICAL
    with st.expander("⚙️ SEO & Analytics", expanded=False):
        gsc_tag = st.text_input("Google Verification ID")
        ga_tag = st.text_input("Google Analytics ID (G-XXXX)")
        og_image = st.text_input("Social Share Image URL")

# --- 4. MAIN WORKSPACE ---
st.title("🏗️ Site Content Builder")

tabs = st.tabs(["1. Identity", "2. Content Blocks", "3. Inventory", "4. Legal & Footer"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        biz_name = st.text_input("Business Name", "Nova Dynamics")
        biz_tagline = st.text_input("Tagline", "Future-Proof Your Infrastructure")
        biz_phone = st.text_input("Phone", "+1 (555) 000-0000")
        biz_email = st.text_input("Email", "hello@novadynamics.io")
    with c2:
        prod_url = st.text_input("Website URL (Required for Sitemap)", "https://novadynamics.io")
        biz_addr = st.text_area("Address", "101 Tech Plaza, Silicon Valley, CA", height=100)
        map_iframe = st.text_area("Google Map Embed Code", placeholder='<iframe src="..."></iframe>', height=100)
        seo_d = st.text_area("Meta Description (SEO)", "The leading provider of advanced solutions for modern enterprises.", height=100)
        logo_url = st.text_input("Logo URL (PNG/SVG)")
        
    st.subheader("Social Links (Footer Icons)")
    sc1, sc2, sc3 = st.columns(3)
    fb_link = sc1.text_input("Facebook URL")
    ig_link = sc2.text_input("Instagram URL")
    x_link = sc3.text_input("X (Twitter) URL")
    
    sc4, sc5, sc6 = st.columns(3)
    li_link = sc4.text_input("LinkedIn URL")
    yt_link = sc5.text_input("YouTube URL")
    wa_num = sc6.text_input("WhatsApp Number (No +)", "15550000000")

with tabs[1]:
    st.subheader("Hero Section")
    hero_h = st.text_input("Hero Headline", "Build Faster. Scale Smarter.")
    hero_sub = st.text_input("Hero Subtext", "The all-in-one solution for modern enterprises looking to dominate their local market.")
    hero_img = st.text_input("Hero Background Image", "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&q=80&w=1600")
    
    st.divider()
    
    st.subheader("Trust Stats Data")
    col_s1, col_s2, col_s3 = st.columns(3)
    stat_1 = col_s1.text_input("Stat 1 (e.g., Years)", "10+")
    label_1 = col_s1.text_input("Label 1", "Years Experience")
    
    stat_2 = col_s2.text_input("Stat 2 (e.g., Clients)", "500+")
    label_2 = col_s2.text_input("Label 2", "Happy Clients")
    
    stat_3 = col_s3.text_input("Stat 3 (e.g., Rating)", "100%")
    label_3 = col_s3.text_input("Label 3", "Satisfaction")

    st.divider()
    
    st.subheader("Feature Grid")
    f_title = st.text_input("Features Title", "Our Expertise")
    feat_data = st.text_area("Features List (Title | Description)", 
                             "Global Reach | We operate in 50+ countries.\n24/7 Support | Always here when you need us.\nSecure Core | Bank-grade encryption standard.",
                             height=150)
    
    st.subheader("About Content")
    st.info("💡 **Formatting Tip:** Wrap titles in double asterisks to make them bold. Example: `**Our Philosophy**`")
    
    about_h = st.text_input("About Title", "Our Legacy")
    about_img = st.text_input("About Side Image", "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&q=80&w=1600")
    
    c_a1, c_a2 = st.columns(2)
    about_short = c_a1.text_area("Home Page Summary (Short)", "Founded in 2020, Nova Dynamics has revolutionized the way businesses approach digital transformation. We are the architects of the future.", height=200)
    about_long = c_a2.text_area("Full About Page Content (Long)", "**Our Story**\nWelcome to Nova Dynamics. Based in Silicon Valley...\n\n**Our Philosophy**\nWe believe software should not just function, it should empower...", height=200)

with tabs[2]:
    st.info("⚡ Power your inventory with a Google Sheet")
    sheet_url = st.text_input("Google Sheet CSV Link", placeholder="https://docs.google.com/spreadsheets/d/e/.../pub?output=csv")
    custom_feat = st.text_input("Default Product Image URL (Fallback)", "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&q=80&w=800")
    st.caption("Required Columns: Name, Price, Description, ImageURL")

with tabs[3]:
    st.subheader("Trust & Legal")
    st.info("💡 Use `**Title**` for bold headers.")
    testi_data = st.text_area("Testimonials (Name | Quote)", "TechDaily | A game changer for our ops.\nCEO, Acme | Highly recommended.", height=100)
    
    faq_data = st.text_area("FAQ Data (Q? ? A)", "Is this secure? ? Yes, 100% encrypted.\nCan I cancel? ? Anytime.", height=100)
    
    l1, l2 = st.columns(2)
    priv_txt = l1.text_area("Privacy Policy Text", "**Introduction**\nWe respect your data...\n\n**Data Collection**\nWe collect email and usage data.", height=200)
    term_txt = l2.text_area("Terms of Service Text", "**Usage**\nBy using this site...\n\n**Liability**\nYou agree to use the site legally.", height=200)

# --- 5. COMPILER ENGINE ---

def format_text(text):
    """Converts newlines to paragraphs and **text** to Bold Headers."""
    if not text: return ""
    paragraphs = text.split('\n')
    html_out = ""
    for p in paragraphs:
        clean_p = p.strip()
        if clean_p:
            if clean_p.startswith("**") and clean_p.endswith("**"):
                header_text = clean_p[2:-2]
                html_out += f"<h3 style='margin-top:1.5rem; margin-bottom:0.5rem; color:var(--p); font-size:1.25rem;'>{header_text}</h3>"
            else:
                html_out += f"<p style='margin-bottom:1rem; opacity:0.8;'>{clean_p}</p>"
    return html_out

def get_theme_css():
    # Base Defaults
    bg_color = "#ffffff"
    text_color = "#0f172a"
    card_bg = "#ffffff"
    glass_nav = "rgba(255, 255, 255, 0.95)"
    
    # Theme Logic
    if "Midnight" in theme_mode:
        bg_color, text_color, card_bg, glass_nav = "#0f172a", "#f8fafc", "#1e293b", "rgba(15, 23, 42, 0.9)"
    elif "Cyberpunk" in theme_mode:
        bg_color, text_color, card_bg, glass_nav = "#050505", "#00ff9d", "#111", "rgba(0,0,0,0.8)"
    elif "Luxury" in theme_mode:
        bg_color, text_color, card_bg, glass_nav = "#1c1c1c", "#D4AF37", "#2a2a2a", "rgba(28,28,28,0.95)"
    elif "Forest" in theme_mode:
        bg_color, text_color, card_bg, glass_nav = "#f1f8e9", "#1b5e20", "#ffffff", "rgba(241,248,233,0.9)"
    elif "Ocean" in theme_mode:
        bg_color, text_color, card_bg, glass_nav = "#e0f7fa", "#006064", "#ffffff", "rgba(224,247,250,0.9)"
    elif "Stark" in theme_mode:
        bg_color, text_color, card_bg, glass_nav = "#ffffff", "#000000", "#ffffff", "rgba(255,255,255,1)"

    anim_css = ""
    if anim_type == "Fade Up":
        anim_css = ".reveal { opacity: 0; transform: translateY(30px); transition: all 0.8s ease-out; } .reveal.active { opacity: 1; transform: translateY(0); }"
    elif anim_type == "Zoom In":
        anim_css = ".reveal { opacity: 0; transform: scale(0.95); transition: all 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275); } .reveal.active { opacity: 1; transform: scale(1); }"
    
    hero_bg_css = f"background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.4)), url('{hero_img}');" if hero_img else "background: var(--p);"

    return f"""
    :root {{
        --p: {p_color}; --s: {s_color}; --bg: {bg_color}; --txt: {text_color}; --card: {card_bg};
        --radius: {border_rad}; --nav: {glass_nav};
        --h-font: '{h_font}', sans-serif; --b-font: '{b_font}', sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{ background-color: var(--bg); color: var(--txt); font-family: var(--b-font); margin: 0; line-height: 1.6; overflow-x: hidden; }}
    h1, h2, h3, h4 {{ font-family: var(--h-font); color: var(--p); line-height: 1.1; margin-bottom: 1rem; }}
    
    .container {{ max-width: 1280px; margin: 0 auto; padding: 0 20px; }}
    .btn {{ display: inline-block; padding: 1rem 2.5rem; border-radius: var(--radius); font-weight: 700; text-decoration: none; transition: 0.3s; text-transform: uppercase; letter-spacing: 0.5px; cursor: pointer; border: none; text-align: center; }}
    .btn-primary {{ background: var(--p); color: white; }}
    .btn-accent {{ background: var(--s); color: white; box-shadow: 0 10px 25px -5px var(--s); }}
    .btn:hover {{ transform: translateY(-3px); filter: brightness(1.15); }}
    
    nav {{ position: fixed; top: 0; width: 100%; z-index: 1000; background: var(--nav); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(100,100,100,0.1); padding: 1rem 0; }}
    .nav-flex {{ display: flex; justify-content: space-between; align-items: center; }}
    .nav-links a {{ margin-left: 2rem; text-decoration: none; font-weight: 600; color: var(--txt); font-size: 0.9rem; opacity: 0.8; transition:0.2s; }}
    .nav-links a:hover {{ opacity: 1; color: var(--s); }}
    
    .hero {{ min-height: 90vh; display: flex; align-items: center; justify-content: center; text-align: center; {hero_bg_css} background-size: cover; background-position: center; color: white; padding-top: 80px; }}
    .hero h1 {{ color: white; font-size: clamp(2.5rem, 8vw, 5rem); margin-bottom: 1.5rem; }}
    .hero p {{ color: rgba(255,255,255,0.9); font-size: clamp(1.1rem, 2vw, 1.5rem); max-width: 700px; margin: 0 auto 2.5rem auto; }}
    
    section {{ padding: 5rem 0; }}
    .section-head {{ text-align: center; margin-bottom: 4rem; }}
    .section-head h2 {{ font-size: 2.5rem; }}
    
    .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }}
    .about-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; }}
    
    .card {{ background: var(--card); padding: 2rem; border-radius: var(--radius); border: 1px solid rgba(100,100,100,0.1); transition: 0.3s; height: 100%; display: flex; flex-direction: column; }}
    .card:hover {{ transform: translateY(-5px); box-shadow: 0 20px 40px -10px rgba(0,0,0,0.1); border-color: var(--s); }}
    
    .prod-img {{ width: 100%; height: 250px; object-fit: cover; border-radius: calc(var(--radius) - 4px); margin-bottom: 1.5rem; background: #f1f5f9; }}
    
    /* FAQ Styling */
    details {{ background: var(--card); border: 1px solid rgba(100,100,100,0.1); border-radius: 8px; margin-bottom: 1rem; padding: 1rem; cursor: pointer; }}
    details summary {{ font-weight: bold; font-size: 1.1rem; }}
    details p {{ margin-top: 1rem; margin-bottom: 0; opacity: 0.8; }}

    /* Footer & Social Icons */
    footer {{ background: var(--p); color: white; padding: 4rem 0; margin-top: auto; }}
    .footer-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 3rem; }}
    .footer a, footer a {{ color: rgba(255,255,255,0.8) !important; text-decoration: none; display: block; margin-bottom: 0.5rem; transition: 0.3s; }}
    .footer a:hover, footer a:hover {{ color: #ffffff !important; text-decoration: underline; }}
    
    .social-icon {{ width: 24px; height: 24px; fill: rgba(255,255,255,0.7); transition: 0.3s; }}
    .social-icon:hover {{ fill: #ffffff; transform: scale(1.1); }}

    /* Real Brand Share Buttons */
    .share-btn {{ width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: none; cursor: pointer; transition: 0.3s; color: white; }}
    .share-btn:hover {{ transform: scale(1.1); filter: brightness(1.1); }}
    .share-btn svg {{ width: 20px; height: 20px; fill: currentColor; }}
    
    .share-wa {{ background: #25D366; }}
    .share-fb {{ background: #1877F2; }}
    .share-x {{ background: #000000; }}
    .share-li {{ background: #0A66C2; }}
    .share-cp {{ background: #64748b; }}
    
    /* Product Detail Specifics */
    .detail-view {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: start; }}
    
    /* Legal Page Formatting */
    .legal-text h1 {{ font-size: 3rem; margin-bottom: 2rem; }}
    .legal-text h3 {{ margin-top: 2rem; font-size: 1.5rem; }}

    {anim_css}
    
    /* MOBILE OPTIMIZATIONS */
    @media (max-width: 768px) {{
        .nav-links {{ display: none; }}
        .hero {{ min-height: 70vh; }}
        .detail-view {{ grid-template-columns: 1fr; gap: 2rem; }}
        /* FIX: Forces About Section to Stack properly on mobile */
        .about-grid {{ grid-template-columns: 1fr !important; gap: 2rem; text-align: left; }}
        .about-grid img {{ order: 2; margin-top: 1rem; }}
        .about-grid div {{ order: 1; }}
    }}
    """

def gen_nav():
    logo_display = f'<img src="{logo_url}" height="40">' if logo_url else f'<span style="font-weight:900; font-size:1.5rem; color:var(--p)">{biz_name}</span>'
    return f"""
    <nav><div class="container nav-flex">
        <a href="index.html" style="text-decoration:none">{logo_display}</a>
        <div class="nav-links">
            <a href="index.html">Home</a>
            {'<a href="index.html#features">Features</a>' if show_features else ''}
            {'<a href="index.html#inventory">Products</a>' if show_inventory else ''}
            <a href="about.html">About</a>
            <a href="contact.html">Contact</a>
            <a href="tel:{biz_phone}" class="btn-accent" style="padding:0.6rem 1.5rem; margin-left:1.5rem; border-radius:50px; color:white !important;">Call Now</a>
        </div>
    </div></nav>
    """

def gen_hero():
    return f"""
    <section class="hero"><div class="container reveal">
        <h1>{hero_h}</h1>
        <p>{hero_sub}</p>
        <div style="display:flex; gap:1rem; justify-content:center; flex-wrap:wrap;">
            <a href="#inventory" class="btn btn-accent">Explore Now</a>
            <a href="contact.html" class="btn" style="background:rgba(255,255,255,0.2); backdrop-filter:blur(10px); color:white;">Contact Us</a>
        </div>
    </div></section>
    """

def gen_features():
    cards = ""
    for line in feat_data.split('\n'):
        if "|" in line:
            title, desc = line.split('|')
            cards += f"""
            <div class="card reveal">
                <h3 style="color:var(--s); font-size:1.2rem; text-transform:uppercase; letter-spacing:1px;">{title.strip()}</h3>
                <p style="opacity:0.8;">{desc.strip()}</p>
            </div>"""
    return f"""
    <section id="features"><div class="container">
        <div class="section-head reveal"><h2>{f_title}</h2></div>
        <div class="grid-3">{cards}</div>
    </div></section>
    """

def gen_stats():
    return f"""
    <div style="background:var(--p); color:white; padding:3rem 0; text-align:center;">
        <div class="container grid-3">
            <div class="reveal">
                <h3 style="color:#ffffff; margin:0; font-size:3rem;">{stat_1}</h3>
                <p style="color:rgba(255,255,255,0.8); margin:0;">{label_1}</p>
            </div>
            <div class="reveal">
                <h3 style="color:#ffffff; margin:0; font-size:3rem;">{stat_2}</h3>
                <p style="color:rgba(255,255,255,0.8); margin:0;">{label_2}</p>
            </div>
            <div class="reveal">
                <h3 style="color:#ffffff; margin:0; font-size:3rem;">{stat_3}</h3>
                <p style="color:rgba(255,255,255,0.8); margin:0;">{label_3}</p>
            </div>
        </div>
    </div>
    """

def gen_inventory_js():
    return f"""
    <script>
    function parseCSVLine(str) {{
        const res = [];
        let cur = '';
        let inQuote = false;
        for (let i = 0; i < str.length; i++) {{
            const c = str[i];
            if (c === '"') {{
                if (inQuote && str[i+1] === '"') {{ cur += '"'; i++; }}
                else {{ inQuote = !inQuote; }}
            }} else if (c === ',' && !inQuote) {{
                res.push(cur.trim()); cur = '';
            }} else {{ cur += c; }}
        }}
        res.push(cur.trim());
        return res;
    }}

    async function loadInv() {{
        try {{
            const res = await fetch('{sheet_url}');
            const txt = await res.text();
            const lines = txt.split(/\\r\\n|\\n/);
            const box = document.getElementById('inv-grid');
            if(!box) return;
            box.innerHTML = '';
            
            for(let i=1; i<lines.length; i++) {{
                if(!lines[i].trim()) continue;
                const clean = parseCSVLine(lines[i]);
                
                let img = clean[3] && clean[3].length > 5 ? clean[3] : '{custom_feat}'; 
                if(clean[6] && clean[6].length > 5) img = clean[6];

                if(clean.length > 1) {{
                    const prodName = encodeURIComponent(clean[0]);
                    box.innerHTML += `
                    <div class="card reveal">
                        <img src="${{img}}" class="prod-img" onerror="this.src='{custom_feat}'">
                        <div style="flex-grow:1; display:flex; flex-direction:column; justify-content:space-between;">
                            <div>
                                <h3>${{clean[0]}}</h3>
                                <p style="font-weight:bold; color:var(--s); font-size:1.1rem;">${{clean[1]}}</p>
                                <p style="font-size:0.9rem; opacity:0.7; margin-bottom:1rem;">${{clean[2] ? clean[2].substring(0,60)+'...' : ''}}</p>
                            </div>
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem;">
                                <a href="product.html?item=${{prodName}}" class="btn" style="background:#e2e8f0; color:var(--primary); padding:0.8rem; font-size:0.8rem;">View Details</a>
                                <a href="https://wa.me/{wa_num}?text=I am interested in ${{prodName}}" target="_blank" class="btn-primary btn" style="padding:0.8rem; font-size:0.8rem;">WhatsApp</a>
                            </div>
                        </div>
                    </div>`;
                }}
            }}
        }} catch(e) {{ console.log(e); }}
    }}
    if(document.getElementById('inv-grid')) window.addEventListener('load', loadInv);
    </script>
    """

def gen_inventory():
    if not show_inventory: return ""
    return f"""
    <section id="inventory" style="background:rgba(0,0,0,0.02)"><div class="container">
        <div class="section-head reveal"><h2>Live Inventory</h2><p>Real-time availability directly from our warehouse.</p></div>
        <div id="inv-grid" class="grid-3"><div style="grid-column:1/-1; text-align:center; padding:4rem; color:var(--s);">Loading Database...</div></div>
    </div></section>
    {gen_inventory_js() if sheet_url else ''}
    """

def gen_about_section():
    # USES SHORT TEXT FOR HOME
    formatted_about = format_text(about_short)
    return f"""
    <section id="about"><div class="container">
        <div class="about-grid">
            <div class="reveal">
                <h2 style="font-size:2.5rem; margin-bottom:1.5rem;">{about_h}</h2>
                <div style="font-size:1.1rem; opacity:0.8; margin-bottom:2rem;">{formatted_about}</div>
                <a href="about.html" class="btn btn-primary" style="padding: 0.8rem 2rem; font-size:0.9rem;">Read Our Full Story</a>
            </div>
            <img src="{about_img}" class="reveal" style="width:100%; border-radius:var(--radius); box-shadow:0 20px 50px -20px rgba(0,0,0,0.2); aspect-ratio:4/3; object-fit:cover;">
        </div>
    </div></section>
    """

def gen_faq_section():
    items = ""
    for line in faq_data.split('\n'):
        if "?" in line and not line.strip() == "":
            parts = line.split('?', 1)
            if len(parts) == 2:
                q = parts[0].strip() + "?"
                a = parts[1].replace("?", "").strip()
                items += f"<details class='reveal'><summary>{q}</summary><p>{a}</p></details>"
    
    return f"""
    <section id="faq" style="background:#f8fafc"><div class="container" style="max-width:800px;">
        <div class="section-head reveal"><h2>Frequently Asked Questions</h2></div>
        {items}
    </div></section>
    """

def gen_footer():
    # FIX: SVG Icons for Socials
    icons = ""
    if fb_link: icons += f'<a href="{fb_link}" target="_blank"><svg class="social-icon" viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg></a>'
    if ig_link: icons += f'<a href="{ig_link}" target="_blank"><svg class="social-icon" viewBox="0 0 24 24"><path d="M16.98 0a6.9 6.9 0 0 1 5.08 1.98A6.94 6.94 0 0 1 24 7.02v9.96c0 2.08-.68 3.87-1.98 5.13A7.14 7.14 0 0 1 16.94 24H7.06a7.06 7.06 0 0 1-5.03-1.89A6.96 6.96 0 0 1 0 16.94V7.02C0 2.8 2.8 0 7.02 0h9.96zM7.17 2.1c-1.4 0-2.6.48-3.46 1.33c-.85.85-1.33 2.06-1.33 3.46v10.3c0 1.3.47 2.5 1.33 3.36c.86.85 2.06 1.33 3.46 1.33h9.66c1.4 0 2.6-.48 3.46-1.33c.85-.85 1.33-2.06 1.33-3.46V6.89c0-1.4-.47-2.6-1.33-3.46c-.86-.85-2.06-1.33-3.46-1.33H7.17zm11.97 3.33c.77 0 1.4.63 1.4 1.4c0 .77-.63 1.4-1.4 1.4c-.77 0-1.4-.63-1.4-1.4c0-.77.63-1.4 1.4-1.4zM12 5.76c3.39 0 6.14 2.75 6.14 6.14c0 3.39-2.75 6.14-6.14 6.14c-3.39 0-6.14-2.75-6.14-6.14c0-3.39 2.75-6.14 6.14-6.14zm0 2.1c-2.2 0-3.99 1.79-3.99 4.04c0 2.25 1.79 4.04 3.99 4.04c2.2 0 3.99-1.79 3.99-4.04c0-2.25-1.79-4.04-3.99-4.04z"/></svg></a>'
    if x_link: icons += f'<a href="{x_link}" target="_blank"><svg class="social-icon" viewBox="0 0 24 24"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584l-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"></path></svg></a>'
    if li_link: icons += f'<a href="{li_link}" target="_blank"><svg class="social-icon" viewBox="0 0 24 24"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2a2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2zM4 2a2 2 0 1 1-2 2a2 2 0 0 1 2-2z"></path></svg></a>'
    if yt_link: icons += f'<a href="{yt_link}" target="_blank"><svg class="social-icon" viewBox="0 0 24 24"><path d="M21.58 5.4c-.28-.81-1.12-1.4-2.23-1.4c-8.75 0-8.75 0-8.75 0s0 0-8.75 0c-1.11 0-1.95.59-2.23 1.4c-.28 1.11-.28 3.6-.28 3.6s0 2.49.28 3.6c.28.81 1.12 1.4 2.23 1.4c8.75 0 8.75 0 8.75 0s0 0 8.75 0c1.11 0 1.95-.59 2.23-1.4c.28-1.11.28-3.6.28-3.6s0-2.49-.28-3.6zM10 15V9l5.2 3L10 15z"></path></svg></a>'

    return f"""
    <footer><div class="container">
        <div class="footer-grid">
            <div>
                <h3 style="color:white; margin-bottom:1.5rem;">{biz_name}</h3>
                <p style="opacity:0.8; font-size:0.9rem;">{biz_addr}</p>
                <p style="opacity:0.8; font-size:0.9rem; margin-top:1rem;">{biz_email}</p>
                <div style="margin-top:1.5rem; display:flex; gap:1.2rem; align-items:center;">
                    {icons}
                </div>
            </div>
            <div>
                <h4 style="color:white; font-size:0.9rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:1.5rem;">Explore</h4>
                <a href="index.html">Home</a>
                <a href="about.html">About Us</a>
                <a href="contact.html">Contact</a>
            </div>
            <div>
                <h4 style="color:white; font-size:0.9rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:1.5rem;">Legal</h4>
                <a href="privacy.html">Privacy Policy</a>
                <a href="terms.html">Terms of Service</a>
            </div>
        </div>
        <div style="border-top:1px solid rgba(255,255,255,0.1); margin-top:3rem; padding-top:2rem; text-align:center; opacity:0.4; font-size:0.8rem;">
            &copy; <a href="https://www.kaydiemscriptlab.com/" target="_blank" style="display:inline; color:white;">Kaydiem Script Lab</a>. Powered by Titan Engine.
        </div>
    </div></footer>
    """

def gen_wa_widget():
    if not wa_num: return ""
    return f"""<a href="https://wa.me/{wa_num}" class="wa-float" target="_blank" style="position:fixed; bottom:30px; right:30px; background:#25d366; color:white; width:60px; height:60px; border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 10px 30px rgba(37,211,102,0.4); z-index:9999;"><svg style="width:32px;height:32px" viewBox="0 0 24 24"><path fill="currentColor" d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91c0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.24 8.23c-1.48 0-2.93-.39-4.19-1.15l-.3-.17l-3.12.82l.83-3.04l-.2-.32a8.188 8.188 0 0 1-1.26-4.38c.01-4.54 3.7-8.24 8.25-8.24m-3.53 3.16c-.13 0-.35.05-.54.26c-.19.2-.72.7-.72 1.72s.73 2.01.83 2.14c.1.13 1.44 2.19 3.48 3.07c.49.21.87.33 1.16.43c.49.16.94.13 1.29.08c.4-.06 1.21-.5 1.38-.98c.17-.48.17-.89.12-.98c-.05-.09-.18-.13-.37-.23c-.19-.1-.1.13-.1.13s-1.13-.56-1.32-.66c-.19-.1-.32-.15-.45.05c-.13.2-.51.65-.62.78c-.11.13-.23.15-.42.05c-.19-.1-.8-.3-1.53-.94c-.57-.5-1.02-1.12-1.21-1.45c-.11-.19-.01-.29.09-.38c.09-.08.19-.23.29-.34c.1-.11.13-.19.19-.32c.06-.13.03-.24-.01-.34c-.05-.1-.45-1.08-.62-1.48c-.16-.4-.36-.34-.51-.35c-.11-.01-.25-.01-.4-.01Z"/></svg></a>"""

def gen_scripts():
    return """
    <script>
    window.addEventListener('scroll', () => {
        var reveals = document.querySelectorAll('.reveal');
        for (var i = 0; i < reveals.length; i++) {
            var windowHeight = window.innerHeight;
            var elementTop = reveals[i].getBoundingClientRect().top;
            var elementVisible = 150;
            if (elementTop < windowHeight - elementVisible) { reveals[i].classList.add('active'); }
        }
    });
    window.dispatchEvent(new Event('scroll'));
    </script>
    """

def build_page(title, content, extra_js=""):
    css = get_theme_css()
    meta_tags = f'<meta name="description" content="{seo_d}">'
    if gsc_tag: meta_tags += f'\n<meta name="google-site-verification" content="{gsc_tag}">'
    if og_image: meta_tags += f'\n<meta property="og:image" content="{og_image}">'
    
    analytics = ""
    if ga_tag:
        analytics = f"""<script async src="https://www.googletagmanager.com/gtag/js?id={ga_tag}"></script>
        <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{ga_tag}');</script>"""

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} | {biz_name}</title>
        {meta_tags}
        <link href="https://fonts.googleapis.com/css2?family={h_font.replace(' ', '+')}:wght@400;700;900&family={b_font.replace(' ', '+')}:wght@300;400;600&display=swap" rel="stylesheet">
        <style>{css}</style>
        {analytics}
    </head>
    <body>
        {gen_nav()}
        {content}
        {gen_footer()}
        {gen_wa_widget()}
        {gen_scripts()}
        {extra_js}
    </body>
    </html>
    """

# --- NEW: GENERATE 404 PAGE ---
def gen_404_content():
    return f"""
    <section class="hero" style="min-height:70vh;">
        <div class="container">
            <h1 style="font-size:6rem; margin:0;">404</h1>
            <p>Page Not Found</p>
            <br>
            <a href="index.html" class="btn btn-accent">Return Home</a>
        </div>
    </section>
    """

# --- NEW: DYNAMIC PRODUCT PAGE (WITH SOCIAL SHARING) ---
def gen_product_page_content():
    return f"""
    <section style="padding-top:150px;">
        <div class="container">
            <div id="product-detail" class="detail-view">
                <div style="background:#eee; height:400px; border-radius:12px; display:flex; align-items:center; justify-content:center;">Loading...</div>
                <div>Loading...</div>
            </div>
        </div>
    </section>
    <script>
    function parseCSVLine(str) {{
        const res = [];
        let cur = '';
        let inQuote = false;
        for (let i = 0; i < str.length; i++) {{
            const c = str[i];
            if (c === '"') {{
                if (inQuote && str[i+1] === '"') {{ cur += '"'; i++; }}
                else {{ inQuote = !inQuote; }}
            }} else if (c === ',' && !inQuote) {{
                res.push(cur.trim()); cur = '';
            }} else {{ cur += c; }}
        }}
        res.push(cur.trim());
        return res;
    }}

    // Share Functions
    function shareFB(url) {{ window.open('https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(url), '_blank'); }}
    function shareWA(url, title) {{ window.open('https://wa.me/?text=' + encodeURIComponent(title + ' ' + url), '_blank'); }}
    function shareX(url, title) {{ window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(title) + '&url=' + encodeURIComponent(url), '_blank'); }}
    function shareLI(url) {{ window.open('https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(url), '_blank'); }}
    function copyLink(url) {{ navigator.clipboard.writeText(url); alert('Link copied!'); }}

    async function loadProduct() {{
        const params = new URLSearchParams(window.location.search);
        const targetName = params.get('item');
        const currentUrl = window.location.href;
        
        if(!targetName) {{
            document.getElementById('product-detail').innerHTML = '<h2>Product not found</h2>';
            return;
        }}

        try {{
            const res = await fetch('{sheet_url}');
            const txt = await res.text();
            const lines = txt.split(/\\r\\n|\\n/);
            
            let found = false;
            
            for(let i=1; i<lines.length; i++) {{
                const clean = parseCSVLine(lines[i]);
                if(clean.length > 0 && clean[0] === targetName) {{
                    found = true;
                    let img = clean[3] && clean[3].length > 5 ? clean[3] : '{custom_feat}'; 
                    if(clean[6] && clean[6].length > 5) img = clean[6];
                    
                    document.getElementById('product-detail').innerHTML = `
                        <img src="${{img}}" style="width:100%; height:auto; border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.1);">
                        <div>
                            <h1 style="font-size:3rem; line-height:1.1;">${{clean[0]}}</h1>
                            <p style="font-size:1.5rem; color:var(--s); font-weight:bold; margin-bottom:1.5rem;">${{clean[1]}}</p>
                            <p style="line-height:1.8; opacity:0.8; margin-bottom:2rem;">${{clean[2]}}</p>
                            
                            <a href="https://wa.me/{wa_num}?text=I am interested in ${{encodeURIComponent(clean[0])}}" target="_blank" class="btn btn-primary" style="width:100%;">Order on WhatsApp</a>
                            
                            <div style="margin-top:2rem;">
                                <p style="font-size:0.9rem; font-weight:bold; opacity:0.7;">SHARE THIS:</p>
                                <div style="display:flex; gap:0.8rem;">
                                    <button onclick="shareWA('${{currentUrl}}', '${{clean[0]}}')" class="share-btn share-wa"><svg viewBox="0 0 24 24"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91c0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.24 8.23c-1.48 0-2.93-.39-4.19-1.15l-.3-.17l-3.12.82l.83-3.04l-.2-.32a8.188 8.188 0 0 1-1.26-4.38c.01-4.54 3.7-8.24 8.25-8.24m-3.53 3.16c-.13 0-.35.05-.54.26c-.19.2-.72.7-.72 1.72s.73 2.01.83 2.14c.1.13 1.44 2.19 3.48 3.07c.49.21.87.33 1.16.43c.49.16.94.13 1.29.08c.4-.06 1.21-.5 1.38-.98c.17-.48.17-.89.12-.98c-.05-.09-.18-.13-.37-.23c-.19-.1-.1.13-.1.13s-1.13-.56-1.32-.66c-.19-.1-.32-.15-.45.05c-.13.2-.51.65-.62.78c-.11.13-.23.15-.42.05c-.19-.1-.8-.3-1.53-.94c-.57-.5-1.02-1.12-1.21-1.45c-.11-.19-.01-.29.09-.38c.09-.08.19-.23.29-.34c.1-.11.13-.19.19-.32c.06-.13.03-.24-.01-.34c-.05-.1-.45-1.08-.62-1.48c-.16-.4-.36-.34-.51-.35c-.11-.01-.25-.01-.4-.01Z"/></svg></button>
                                    
                                    <button onclick="shareFB('${{currentUrl}}')" class="share-btn share-fb"><svg viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg></button>
                                    
                                    <button onclick="shareX('${{currentUrl}}', '${{clean[0]}}')" class="share-btn share-x"><svg viewBox="0 0 24 24"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584l-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"></path></svg></button>
                                    
                                    <button onclick="shareLI('${{currentUrl}}')" class="share-btn share-li"><svg viewBox="0 0 24 24"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2a2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2zM4 2a2 2 0 1 1-2 2a2 2 0 0 1 2-2z"></path></svg></button>
                                    
                                    <button onclick="copyLink('${{currentUrl}}')" class="share-btn share-cp"><svg viewBox="0 0 24 24"><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></button>
                                </div>
                            </div>

                            <br><br>
                            <a href="index.html#inventory" style="text-decoration:none; color:var(--txt); opacity:0.6;">&larr; Back to Shop</a>
                        </div>
                    `;
                    break;
                }}
            }}
            if(!found) document.getElementById('product-detail').innerHTML = '<h2>Product not found in database.</h2>';
            
        }} catch(e) {{ console.log(e); }}
    }}
    loadProduct();
    </script>
    """

# --- 6. PAGE CONTENT GENERATION ---
home_content = ""
if show_hero: home_content += gen_hero()
if show_stats: home_content += gen_stats()
if show_features: home_content += gen_features()
if show_inventory: home_content += gen_inventory()
if show_gallery: home_content += gen_about_section()
if show_testimonials: 
    t_cards = "".join([f'<div class="card reveal" style="text-align:center;"><i>"{x.split("|")[1]}"</i><br><br><b>- {x.split("|")[0]}</b></div>' for x in testi_data.split('\n') if "|" in x])
    home_content += f'<section style="background:#f8fafc"><div class="container"><div class="section-head reveal"><h2>Client Stories</h2></div><div class="grid-3">{t_cards}</div></div></section>'
if show_faq: home_content += gen_faq_section()
if show_cta: home_content += f'<section style="background:var(--s); color:white; text-align:center;"><div class="container reveal"><h2>Ready to Start?</h2><p style="margin-bottom:2rem;">Let us build your future today.</p><a href="contact.html" class="btn" style="background:white; color:var(--s);">Get a Quote</a></div></section>'

# --- 7. RENDER & DEPLOY ---
st.divider()
st.subheader("🚀 Launchpad")

preview_mode = st.radio("Preview Page:", ["Home", "About", "Contact", "Privacy", "Terms", "Product Detail (Demo)"], horizontal=True)

# Generate static contents for other pages with better formatting
# FIX: Uses about_long for the actual About Page
about_content = f'<section class="hero" style="min-height:50vh;"><div class="container"><h1>About Us</h1></div></section><section><div class="container legal-text">{format_text(about_long)}</div></section>'
contact_content = f'<section class="hero" style="min-height:50vh;"><div class="container"><h1>Contact Us</h1></div></section><section><div class="container" style="text-align:center;"><h2>{biz_phone}</h2><p>{biz_addr}</p><br>{map_iframe}</div></section>'
privacy_content = f'<section><div class="container legal-text"><h1>Privacy Policy</h1><br>{format_text(priv_txt)}</div></section>'
terms_content = f'<section><div class="container legal-text"><h1>Terms of Service</h1><br>{format_text(term_txt)}</div></section>'

c1, c2 = st.columns([3, 1])
with c1:
    if preview_mode == "Home":
        st.components.v1.html(build_page("Home", home_content), height=600, scrolling=True)
    elif preview_mode == "About":
        st.components.v1.html(build_page("About", about_content), height=600, scrolling=True)
    elif preview_mode == "Contact":
        st.components.v1.html(build_page("Contact", contact_content), height=600, scrolling=True)
    elif preview_mode == "Privacy":
        st.components.v1.html(build_page("Privacy", privacy_content), height=600, scrolling=True)
    elif preview_mode == "Terms":
        st.components.v1.html(build_page("Terms", terms_content), height=600, scrolling=True)
    elif preview_mode == "Product Detail (Demo)":
        st.warning("Preview only shows layout. Live data requires the downloaded file.")
        st.components.v1.html(build_page("Product Name", gen_product_page_content()), height=600, scrolling=True)

with c2:
    st.success("System Ready.")
    if st.button("DOWNLOAD WEBSITE ZIP", type="primary"):
        z_b = io.BytesIO()
        with zipfile.ZipFile(z_b, "a", zipfile.ZIP_DEFLATED, False) as zf:
            # 1. Main Pages
            zf.writestr("index.html", build_page("Home", home_content))
            zf.writestr("about.html", build_page("About", about_content))
            zf.writestr("contact.html", build_page("Contact", contact_content))
            zf.writestr("privacy.html", build_page("Privacy Policy", privacy_content))
            zf.writestr("terms.html", build_page("Terms of Service", terms_content))
            
            # 2. Product Detail Page
            zf.writestr("product.html", build_page("Product Details", gen_product_page_content()))

            # 3. 404 Page
            zf.writestr("404.html", build_page("404 Not Found", gen_404_content()))

            # 4. Robots.txt
            robots_txt = f"User-agent: *\nAllow: /\nSitemap: {prod_url}/sitemap.xml"
            zf.writestr("robots.txt", robots_txt)

            # 5. Sitemap.xml
            import datetime
            date_str = datetime.date.today().isoformat()
            sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url><loc>{prod_url}/</loc><lastmod>{date_str}</lastmod></url>
   <url><loc>{prod_url}/index.html</loc><lastmod>{date_str}</lastmod></url>
   <url><loc>{prod_url}/about.html</loc><lastmod>{date_str}</lastmod></url>
   <url><loc>{prod_url}/contact.html</loc><lastmod>{date_str}</lastmod></url>
   <url><loc>{prod_url}/privacy.html</loc><lastmod>{date_str}</lastmod></url>
   <url><loc>{prod_url}/terms.html</loc><lastmod>{date_str}</lastmod></url>
</urlset>"""
            zf.writestr("sitemap.xml", sitemap_xml)
            
        st.download_button("📥 Click to Save", z_b.getvalue(), f"{biz_name.lower().replace(' ','_')}_site.zip", "application/zip")
