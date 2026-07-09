"""
14 diverse GenerationConfig classes for web-design-bench (10 Static v1, 4 Animation v2).

Each config encodes a complete, distinctive DesignSpec: specific brand identity,
color palette, typography, page structure, and design directives. The generator
uses these directly to produce unique, non-generic websites.

Archetypes span dark/light, warm/cool, minimal/rich, serif/sans-serif to ensure
SSIM/pHash comparisons are meaningful across the full difficulty spectrum.

Every config produces 5 pages with a shared style.css — no JavaScript allowed.

── Difficulty Tiers & Definitions ─────────────────────────────────────────────

NOTE: Tiers reflect structural design complexity (density, advanced CSS styling,
and animation choreography), not empirical agent performance. They do not imply
that agents will achieve higher rewards on "easy" tasks; agents often excel at
dense layouts while struggling with subtle alignment or temporal constraints.

Part 1: Static Tasks (v1)
  • Easy:   Clean, standard layouts (e.g., single column, basic grids), standard
            typography, minimal decorative elements or complex background meshes.
  • Medium: Richer layouts (asymmetrical sections, overlapping cards), curated
            color palettes, custom UI components (pricing tables, calculators).
  • Hard:   Dense, highly complex interfaces (e.g., SaaS dashboards, crypto exchanges),
            advanced CSS styling (glassmorphism, neon glows, complex gradient meshes).

Part 2: Animation Tasks (v2)
  • Medium: Clean, elegant animations (fade-ins, slide-ups) with moderate stagger
            delays (0.1s–0.5s). Tests basic temporal property adherence.
  • Hard:   Multi-phase keyframes (e.g., fade → slide → glow/pulse) and complex
            choreography with large stagger delays (0.5s–1.5s+), requiring precise
            intermediate state matching across extended time windows (0–1800ms).
"""


from recipe.configs import register_config


# ── Base defaults shared by all configs ──────────────────────────────────────

class _Base:
    RECIPE_VERSION     = "v1"
    VIEWPORTS          = ["desktop"]
    VIEWPORT_SIZES     = {"desktop": {"width": 1280, "height": 800}}
    FULL_PAGE          = True
    DEVICE_PIXEL_RATIO = 1
    SCREENSHOT_FMT     = "png"
    SSIM_WEIGHT        = 0.6
    PHASH_WEIGHT       = 0.4
    DOM_IOU_WEIGHT     = 0.0
    MAX_RETRIES        = 3
    SEED               = 42
    HINT_SCROLL_HEIGHT = True
    HINT_FONTS         = True
    HINT_COLORS        = True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1 · AI Startup — NexaAI · Neon Dark · Hard
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register_config("ai_startup_neon_hard")
class AiStartupNeonHardConfig(_Base):
    ARCHETYPE    = "ai_startup"
    VISUAL_STYLE = "neon_dark"
    DIFFICULTY   = "hard"
    BRAND_NAME   = "NexaAI"
    BRAND_TAGLINE = "Intelligence that scales with you"
    COLORS = {
        "background":    "#0b0b1a",
        "surface":       "#13132b",
        "border":        "#2d2d5e",
        "primary":       "#7c3aed",
        "accent":        "#06b6d4",
        "text_primary":  "#f0f0ff",
        "text_secondary":"#8888bb",
        "cta":           "#7c3aed",
    }
    FONTS = ["Space Grotesk", "system-ui", "sans-serif"]
    PAGES = [
        {"name": "page_home",     "file": "index.html",    "label": "Home",
         "description": "Full-viewport hero with deep dark gradient bg, oversized headline "
                        "'Intelligence that scales with you' with neon purple glow text effect, "
                        "dual CTAs (Get Started / See Demo); animated-look particle grid section "
                        "(CSS dots/lines pattern); 3-column AI capability cards (NLP, Vision, "
                        "Prediction) with icon placeholders and glowing borders; integration "
                        "partners strip (8 tech company names); metrics bar (1M+ API calls/day, "
                        "99.99% uptime, 200ms avg latency, 500+ enterprise clients); testimonial "
                        "carousel-like strip (3 quotes from CTOs); bottom CTA banner with gradient"},
        {"name": "page_platform", "file": "platform.html", "label": "Platform",
         "description": "Platform overview hero; 6-feature deep-dive alternating left/right layout "
                        "(Model Training, Data Pipeline, Auto-Scaling, Monitoring, A/B Testing, "
                        "Edge Deployment) each with diagram placeholder and 4-line description; "
                        "architecture diagram section (CSS-only layered boxes showing data flow); "
                        "SDK/API code snippet section with dark code blocks showing Python examples; "
                        "benchmark comparison table (NexaAI vs AWS SageMaker vs Google Vertex)"},
        {"name": "page_solutions","file": "solutions.html","label": "Solutions",
         "description": "Industry solutions hero; 4 industry verticals as large cards (Healthcare, "
                        "Finance, Retail, Manufacturing) each with neon-bordered icon placeholder, "
                        "use-case description, and key metric; case study spotlight with large quote "
                        "and company logo placeholder; ROI calculator section (static visual with "
                        "labeled inputs and output display); partner ecosystem grid (12 logos as "
                        "colored tiles)"},
        {"name": "page_pricing",  "file": "pricing.html",  "label": "Pricing",
         "description": "Pricing hero with toggle-like visual (Monthly/Annual); 3-tier pricing "
                        "cards (Starter $99/mo, Scale $499/mo, Enterprise Custom) each with feature "
                        "list of 8 items, middle card highlighted with purple glow; feature "
                        "comparison matrix table (15 rows × 3 columns with checkmarks); FAQ "
                        "accordion-style section (10 questions); volume discount table; enterprise "
                        "contact CTA"},
        {"name": "page_contact",  "file": "contact.html",  "label": "Contact",
         "description": "Contact hero with gradient mesh background (CSS); two-column layout: "
                        "left has multi-step-looking form (name, company, email, use case dropdown, "
                        "monthly API calls, message, submit); right has sales team cards (3 reps "
                        "with photo placeholder, name, region, email); office locations section "
                        "(San Francisco, London, Singapore, Tokyo with addresses); status page "
                        "link and community Discord CTA"},
    ]
    DESIGN_DIRECTIVES = (
        "Ultra-dark navy background (#0b0b1a). Neon purple (#7c3aed) as the primary brand "
        "color with cyan (#06b6d4) as the secondary accent. Use CSS gradients and subtle "
        "glow effects (box-shadow with purple/cyan) extensively. Navigation: glassmorphism "
        "style (semi-transparent bg with backdrop-filter blur). Hero headline: very large "
        "(clamp 3rem–5.5rem), with text-shadow glow. Section backgrounds alternate between "
        "#0b0b1a and #13132b. Cards: dark surface, 1px border #2d2d5e, hover glow effect, "
        "border-radius 16px. Buttons: purple gradient (purple→blue) primary, cyan outlined "
        "secondary. Code blocks: #0a0a18 with cyan syntax highlights. Typography: Space "
        "Grotesk; geometric and modern. Footer: #07071a with neon accent divider, 4 columns."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2 · Luxury Fashion — Maison Élégance · Minimalist Serif · Medium
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register_config("luxury_fashion_serif_medium")
class LuxuryFashionSerifMediumConfig(_Base):
    ARCHETYPE    = "luxury_fashion"
    VISUAL_STYLE = "minimalist_serif"
    DIFFICULTY   = "medium"
    BRAND_NAME   = "Maison Élégance"
    BRAND_TAGLINE = "Timeless craftsmanship, modern sensibility"
    COLORS = {
        "background":    "#faf8f5",
        "surface":       "#f0ede8",
        "border":        "#d4cfc7",
        "primary":       "#1a1a1a",
        "accent":        "#c4a265",
        "text_primary":  "#1a1a1a",
        "text_secondary":"#6b6560",
        "cta":           "#1a1a1a",
    }
    FONTS = ["Playfair Display", "Georgia", "serif"]
    PAGES = [
        {"name": "page_home",        "file": "index.html",       "label": "Home",
         "description": "Full-bleed editorial hero with large serif headline 'Timeless "
                        "Craftsmanship' in elegant italic, thin gold horizontal rule, and "
                        "'Explore Collection' CTA; 3-column category feature (Haute Couture, "
                        "Prêt-à-Porter, Accessories) with tall image placeholders and serif "
                        "labels; editorial quote strip in large italic ('Fashion fades, only "
                        "style remains'); new season preview: 4 product cards in a row with "
                        "name and price; atelier story teaser with left image placeholder and "
                        "right text; newsletter signup with gold accent input"},
        {"name": "page_collection", "file": "collection.html", "label": "Collection",
         "description": "Collection header with season name (Automne-Hiver 2025); filter bar "
                        "(All, Dresses, Coats, Accessories, Shoes) with underline active state; "
                        "3-column product grid (12 items) each with tall image placeholder, "
                        "product name in serif, price, and 'View' link; subtle hover overlay "
                        "with gold border"},
        {"name": "page_atelier",    "file": "atelier.html",    "label": "Atelier",
         "description": "Brand story page: large cinematic image placeholder top; founding "
                        "narrative in two-column serif text; craftsmanship timeline (1987, 1995, "
                        "2003, 2015, 2024) with descriptions; materials section showcasing 4 "
                        "fabric types with placeholders and descriptions; artisan portraits "
                        "section (3 circular placeholders with names and specialties)"},
        {"name": "page_journal",    "file": "journal.html",    "label": "Journal",
         "description": "Fashion journal/editorial page: featured article with full-width image "
                        "placeholder and large serif headline; 2-column article grid (6 posts) "
                        "each with image placeholder, date, category tag, headline, and 2-line "
                        "excerpt; sidebar with 'Editor's Picks' list; bottom: fashion week "
                        "calendar section"},
        {"name": "page_contact",    "file": "contact.html",    "label": "Contact",
         "description": "Minimal elegant contact: centered 'Maison Élégance' in large display "
                        "serif; two-column: left has appointment booking form (name, email, "
                        "phone, preferred date, interest dropdown, message) with thin borders; "
                        "right has boutique locations (Paris 8ème, Milan, New York, Tokyo) with "
                        "addresses and hours; thin gold decorative rules throughout"},
    ]
    DESIGN_DIRECTIVES = (
        "Warm cream background (#faf8f5). All typography is serif (Playfair Display / Georgia). "
        "Use extraordinarily generous whitespace — large padding (80px+ sections), wide margins. "
        "Gold (#c4a265) for thin decorative rules, underlines, and hover accents only. "
        "Navigation: centered logo in display serif, links evenly spaced below, thin gold "
        "bottom border. Product cards: no borders, no shadows — just image + text with "
        "letter-spacing. Buttons: thin black 1px outlined, uppercase, letter-spacing 0.25em, "
        "no fill, hover fills black with white text. All headings: italic serif, never bold. "
        "Footer: cream background, single centered column with links, gold rule above."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3 · Indie Game Studio — PixelForge · Retro Vibrant · Medium
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register_config("indie_game_retro_medium")
class IndieGameRetroMediumConfig(_Base):
    ARCHETYPE    = "indie_game_studio"
    VISUAL_STYLE = "retro_vibrant"
    DIFFICULTY   = "medium"
    BRAND_NAME   = "PixelForge"
    BRAND_TAGLINE = "Crafting worlds, one pixel at a time"
    COLORS = {
        "background":    "#1a1a2e",
        "surface":       "#16213e",
        "border":        "#0f3460",
        "primary":       "#e94560",
        "accent":        "#0f3460",
        "text_primary":  "#eeeeff",
        "text_secondary":"#8888aa",
        "cta":           "#e94560",
    }
    FONTS = ["Press Start 2P", "Courier New", "monospace"]
    PAGES = [
        {"name": "page_home",   "file": "index.html",  "label": "Home",
         "description": "Retro-styled hero with pixel-art-inspired CSS border patterns, large "
                        "pixelated headline 'PIXELFORGE' in monospace, subtitle in smaller type, "
                        "and 'Play Our Games' CTA button styled like a retro game button; featured "
                        "game showcase: 3 large game cards (Stellar Drift, Neon Dungeon, Byte "
                        "Kingdom) each with colored placeholder, genre tag, platform badges, and "
                        "description; studio news ticker strip with 4 updates; community stats "
                        "(50K players, 15 games, 8 awards); press logos strip"},
        {"name": "page_games",  "file": "games.html",  "label": "Games",
         "description": "Games catalog hero; filter tabs (All / Action / RPG / Puzzle / Strategy); "
                        "game grid (8 cards) each with image placeholder, title in monospace, "
                        "genre badge, platform icons (PC/Console/Mobile as text), release year, "
                        "and 'Learn More' button; coming soon section with 2 teaser cards; "
                        "retro-styled pagination"},
        {"name": "page_about",  "file": "about.html",  "label": "About",
         "description": "Studio story in retro terminal style: founding story (Est. 2019) with "
                        "blinking-cursor-look accent; team section with 6 members (pixel-art-style "
                        "colored square placeholders, name, role); studio values in 4 columns "
                        "(Passion, Innovation, Community, Quality) with pixelated icons; timeline "
                        "of major releases; job openings section with 3 positions"},
        {"name": "page_community","file":"community.html","label": "Community",
         "description": "Community hub: Discord-style activity feed (static, 5 items); fan art "
                        "gallery grid (9 colored placeholders); leaderboard table (top 10 players "
                        "with rank, username, score, game); community events section (3 upcoming "
                        "events); modding resources section; newsletter signup with retro styling"},
        {"name": "page_contact","file": "contact.html","label": "Contact",
         "description": "Retro terminal-styled contact page: form with pixel-border inputs "
                        "(name, email, subject dropdown: Business/Press/Support/Fan Mail, "
                        "message, submit button styled as game button); business inquiries "
                        "section; press kit download section; social links (Twitter, Discord, "
                        "YouTube, Twitch) with retro button styling"},
    ]
    DESIGN_DIRECTIVES = (
        "Dark navy background (#1a1a2e). Hot pink (#e94560) as the primary action color. "
        "Deep blue (#0f3460) for borders and secondary surfaces. Typography: pixel/monospace "
        "(Press Start 2P for headings, Courier New for body) — all uppercase headings. "
        "Navigation: dark surface bar, hot pink active/hover state, pixelated logo text. "
        "Cards: dark surface (#16213e), 2px solid borders, 0 border-radius (sharp corners). "
        "Buttons: hot pink fill, sharp corners, text-transform uppercase, pixel-font. "
        "Decorative: use CSS box-shadow to create pixelated/stepped border effects. "
        "Genre badges: small colored pills. Footer: dark #0d0d20, hot pink accents, "
        "4 columns with retro aesthetic."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4 · Wellness Spa — Serene Bloom · Organic Warm · Easy
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register_config("wellness_spa_organic_easy")
class WellnessSpaOrganicEasyConfig(_Base):
    ARCHETYPE    = "wellness_spa"
    VISUAL_STYLE = "organic_warm"
    DIFFICULTY   = "easy"
    BRAND_NAME   = "Serene Bloom"
    BRAND_TAGLINE = "Restore your inner balance"
    COLORS = {
        "background":    "#f5f0eb",
        "surface":       "#ebe4db",
        "border":        "#d2c4b4",
        "primary":       "#5b7553",
        "accent":        "#d4a574",
        "text_primary":  "#2c2c2c",
        "text_secondary":"#706658",
        "cta":           "#5b7553",
    }
    FONTS = ["Lora", "Georgia", "serif"]
    PAGES = [
        {"name": "page_home",      "file": "index.html",     "label": "Home",
         "description": "Serene hero with warm linen background, large serif headline "
                        "'Restore Your Inner Balance', soft green CTA 'Book a Treatment'; "
                        "3-column service highlights (Massage, Facial, Wellness) with leaf-like "
                        "decorative elements; philosophy section with centered italic quote "
                        "about natural healing; opening hours card with warm background; "
                        "testimonial section with 2 client quotes"},
        {"name": "page_treatments","file": "treatments.html","label": "Treatments",
         "description": "Treatment menu: category sections (Massage Therapies, Skin Care, "
                        "Body Treatments, Wellness Rituals) each with 3-4 treatments listed "
                        "as name + duration + price + 1-line description; package deals section "
                        "with 3 packages (Day Retreat $150, Half-Day $95, Express $55); booking "
                        "reminder CTA at bottom"},
        {"name": "page_about",     "file": "about.html",     "label": "About",
         "description": "Our story section with warm image placeholder and founder bio text; "
                        "values section (Natural Ingredients, Holistic Approach, Sustainable "
                        "Practice) in 3 columns; our team: 4 therapist cards with circular "
                        "placeholder, name, specialty, and certifications; spa environment "
                        "section with description of facilities"},
        {"name": "page_gallery",   "file": "gallery.html",   "label": "Gallery",
         "description": "Simple photo gallery: 3-column grid of 9 image placeholders with "
                        "warm-toned backgrounds; category labels (Spa Interior, Treatments, "
                        "Products); Instagram follow CTA at bottom"},
        {"name": "page_booking",   "file": "booking.html",   "label": "Book Now",
         "description": "Booking form: service selection dropdown, preferred therapist, date, "
                        "time slot, name, email, phone, special requests textarea, submit button; "
                        "cancellation policy note; gift certificate section; contact info with "
                        "phone, email, and address"},
    ]
    DESIGN_DIRECTIVES = (
        "Warm linen background (#f5f0eb). Sage green (#5b7553) for primary text, nav, and "
        "CTAs. Sandy accent (#d4a574) for decorative borders and highlights. Typography: "
        "Lora/Georgia serif throughout — warm and readable. Large padding (60px+ sections). "
        "Navigation: cream background, green text, gold underline on active. Buttons: sage "
        "green fill, rounded 8px, no uppercase. Cards: warm surface (#ebe4db), no hard "
        "borders, subtle warm shadow. Decorative: thin gold (#d4a574) horizontal rules "
        "between sections. Footer: sage green background, cream text, simple centered layout."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5 · Crypto Exchange — VaultX · Cyberpunk · Hard
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register_config("crypto_exchange_cyberpunk_hard")
class CryptoExchangeCyberpunkHardConfig(_Base):
    ARCHETYPE    = "crypto_exchange"
    VISUAL_STYLE = "cyberpunk"
    DIFFICULTY   = "hard"
    BRAND_NAME   = "VaultX"
    BRAND_TAGLINE = "Trade the future, own the edge"
    COLORS = {
        "background":    "#0a0a0a",
        "surface":       "#111111",
        "border":        "#1e1e1e",
        "primary":       "#00ff88",
        "accent":        "#ff006e",
        "text_primary":  "#e0e0e0",
        "text_secondary":"#666666",
        "cta":           "#00ff88",
    }
    FONTS = ["JetBrains Mono", "Fira Code", "monospace"]
    PAGES = [
        {"name": "page_home",     "file": "index.html",    "label": "Home",
         "description": "Aggressive cyberpunk hero: pure black bg, massive green monospace "
                        "headline 'TRADE THE FUTURE', live-market-style ticker strip showing "
                        "BTC $67,432 ETH $3,891 SOL $178 (static); trading volume stat "
                        "($12.4B 24h volume); dual CTAs (Start Trading / View Markets) with "
                        "neon glow; 4-column feature cards (Spot Trading, Derivatives, Staking, "
                        "DeFi Bridge) with green wireframe icons; security section with 3 badges "
                        "(Cold Storage, 2FA, Insurance Fund); partner exchange logos; leaderboard "
                        "preview table (top 5 traders)"},
        {"name": "page_markets",  "file": "markets.html",  "label": "Markets",
         "description": "Markets dashboard: search bar; market tabs (Spot / Futures / Options); "
                        "market table with 20 rows (Pair, Price, 24h Change %, 24h Volume, "
                        "Market Cap, sparkline-placeholder, Trade button) — prices in green/red; "
                        "gainers/losers mini tables (top 5 each); market overview stats"},
        {"name": "page_security", "file": "security.html", "label": "Security",
         "description": "Security center: trust hero with green shield icon (CSS); security "
                        "architecture: 4 layered sections (Network, Application, Wallet, Audit) "
                        "each with technical description; proof of reserves section with fake "
                        "wallet balance display; bug bounty program section; compliance badges "
                        "(SOC 2, ISO 27001, GDPR); security audit timeline"},
        {"name": "page_fees",     "file": "fees.html",     "label": "Fees",
         "description": "Fee schedule hero; tiered fee table: 6 VIP levels (VIP 0-5) × 4 "
                        "columns (30d Volume, Maker Fee, Taker Fee, Withdrawal); spot vs futures "
                        "fee comparison; deposit/withdrawal fee table for 15 assets; fee discount "
                        "section (VaultX Token holders); referral program details with earnings "
                        "calculator visual"},
        {"name": "page_contact",  "file": "contact.html",  "label": "Support",
         "description": "Support center: 3 support channels as cards (Live Chat 24/7, Email "
                        "Support, Ticket System); FAQ section with 12 questions organized in "
                        "categories (Account, Trading, Security, Withdrawals); API documentation "
                        "link section; community channels (Telegram, Discord, Twitter); legal "
                        "disclaimers and regulatory info"},
    ]
    DESIGN_DIRECTIVES = (
        "Pure black background (#0a0a0a). Neon green (#00ff88) as the primary color for "
        "positive values, CTAs, and brand elements. Hot pink (#ff006e) for negative values, "
        "alerts, and secondary accents. All typography: monospace (JetBrains Mono/Fira Code). "
        "Navigation: black bg, green logo/active state, sharp corners. Cards: #111111 surface, "
        "1px #1e1e1e border, sharp corners (0 border-radius). Tables: dense, monospace numbers, "
        "alternating row backgrounds (#0a0a0a / #111111), green/pink for +/- values. Buttons: "
        "green with black text primary, outlined green secondary. Neon glow: use box-shadow "
        "with green/pink for emphasis. Footer: #050505, green accent line, minimal."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6 · Travel Agency — Wanderlust · Bright Tropical · Medium
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register_config("travel_agency_tropical_medium")
class TravelAgencyTropicalMediumConfig(_Base):
    ARCHETYPE    = "travel_agency"
    VISUAL_STYLE = "bright_tropical"
    DIFFICULTY   = "medium"
    BRAND_NAME   = "Wanderlust"
    BRAND_TAGLINE = "Your journey begins here"
    COLORS = {
        "background":    "#ffffff",
        "surface":       "#f0f9ff",
        "border":        "#bae6fd",
        "primary":       "#0891b2",
        "accent":        "#f59e0b",
        "text_primary":  "#0f172a",
        "text_secondary":"#64748b",
        "cta":           "#0891b2",
    }
    FONTS = ["Poppins", "system-ui", "sans-serif"]
    PAGES = [
        {"name": "page_home",         "file": "index.html",        "label": "Home",
         "description": "Bright hero with ocean-blue gradient top, large friendly headline "
                        "'Your Journey Begins Here', search-bar-style CTA (Destination input, "
                        "Date, Travelers, Search button in amber); popular destinations: 4 "
                        "cards (Bali, Santorini, Kyoto, Patagonia) with colored placeholders "
                        "and price-from badge; travel types section: 3 columns (Adventure, "
                        "Luxury, Cultural) with descriptions; customer reviews: 3 cards with "
                        "star ratings; partner airlines strip; newsletter CTA"},
        {"name": "page_destinations", "file": "destinations.html", "label": "Destinations",
         "description": "Destinations page: search + filter bar (Region, Budget, Season, "
                        "Activity); 3-column destination grid (9 cards) each with image "
                        "placeholder, destination name, country flag emoji, rating, starting "
                        "price, and 'Explore' button; featured destination spotlight with large "
                        "image and itinerary preview; travel tips sidebar"},
        {"name": "page_packages",     "file": "packages.html",     "label": "Packages",
         "description": "Travel packages: 3 featured packages (Explorer 7-day $1,299, Premium "
                        "10-day $2,499, Ultimate 14-day $4,199) as large cards with inclusions "
                        "list (flights, hotels, guides, meals); seasonal deals section; group "
                        "travel section; custom package inquiry CTA"},
        {"name": "page_about",        "file": "about.html",        "label": "About",
         "description": "About page: founder story with image placeholder; company stats "
                        "(15 years, 50K+ travelers, 80+ countries, 98% satisfaction); team "
                        "section (4 travel experts with photo placeholders, names, specialties); "
                        "sustainability commitment section; awards and certifications"},
        {"name": "page_contact",      "file": "contact.html",      "label": "Contact",
         "description": "Contact page: inquiry form (name, email, phone, destination interest, "
                        "travel dates, group size, budget range, message); office locations "
                        "(Sydney, London, New York); emergency travel support hotline section; "
                        "social media links; FAQ section (6 common questions)"},
    ]
    DESIGN_DIRECTIVES = (
        "Clean white background (#ffffff). Teal (#0891b2) as the primary brand color — nav, "
        "headings, links. Amber (#f59e0b) as the warm accent for CTAs, badges, and stars. "
        "Navigation: white with teal text, amber 'Book Now' button, subtle shadow. Hero: "
        "gradient from teal to sky blue. Cards: white with light blue border (#bae6fd), "
        "12px border-radius, hover shadow lift. Buttons: teal fill rounded 8px primary, "
        "amber fill for booking CTAs. Price badges: amber background with dark text. "
        "Typography: Poppins — friendly and modern. Footer: teal background, white text, "
        "3 columns with newsletter signup."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7 · Law Firm — Sterling & Associates · Corporate Clean · Easy
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register_config("law_firm_corporate_easy")
class LawFirmCorporateEasyConfig(_Base):
    ARCHETYPE    = "law_firm"
    VISUAL_STYLE = "corporate_clean"
    DIFFICULTY   = "easy"
    BRAND_NAME   = "Sterling & Associates"
    BRAND_TAGLINE = "Trusted counsel for complex matters"
    COLORS = {
        "background":    "#ffffff",
        "surface":       "#f8f6f2",
        "border":        "#d4cec4",
        "primary":       "#1e3a5f",
        "accent":        "#8b6914",
        "text_primary":  "#1a1a1a",
        "text_secondary":"#5a5a5a",
        "cta":           "#1e3a5f",
    }
    FONTS = ["Merriweather", "Georgia", "serif"]
    PAGES = [
        {"name": "page_home",      "file": "index.html",      "label": "Home",
         "description": "Distinguished hero with navy gradient background, serif headline "
                        "'Trusted Counsel for Complex Matters', 'Schedule Consultation' CTA; "
                        "3-column practice areas preview (Corporate Law, Litigation, Real "
                        "Estate) with brief descriptions; firm stats: 40+ years, 200+ "
                        "attorneys, 95% success rate; recognition section with 4 award names; "
                        "client testimonial quote"},
        {"name": "page_practice",  "file": "practice.html",  "label": "Practice Areas",
         "description": "Practice areas page: 6 areas listed (Corporate & M&A, Litigation, "
                        "Real Estate, Employment, Intellectual Property, Tax) each with icon "
                        "placeholder, title, 3-line description, and key clients mention; "
                        "notable cases section with 3 case summaries"},
        {"name": "page_attorneys", "file": "attorneys.html", "label": "Attorneys",
         "description": "Attorney directory: 6 attorney cards (portrait placeholder, name, "
                        "title/partner level, practice area, bar admissions, education, email); "
                        "managing partner spotlight with larger card; diversity statement"},
        {"name": "page_about",     "file": "about.html",     "label": "About",
         "description": "Firm history section: founded 1982 narrative; values (Integrity, "
                        "Excellence, Client Focus, Teamwork) in 2×2 grid; office photo "
                        "placeholder; community involvement section; pro bono commitment; "
                        "diversity and inclusion statement"},
        {"name": "page_contact",   "file": "contact.html",   "label": "Contact",
         "description": "Contact page: consultation request form (name, company, email, phone, "
                        "practice area dropdown, brief description, preferred contact method, "
                        "submit); main office address with map placeholder; 3 branch offices; "
                        "confidentiality notice; office hours"},
    ]
    DESIGN_DIRECTIVES = (
        "White background (#ffffff). Navy (#1e3a5f) as the authoritative primary color for "
        "headers, nav, and CTAs. Dark gold (#8b6914) as the prestige accent for rules, "
        "highlights, and award markers. Typography: Merriweather/Georgia serif — traditional "
        "and trustworthy. Navigation: white background, navy text, thin gold bottom border, "
        "no flashy effects. Buttons: navy fill, 4px border-radius, uppercase letter-spacing. "
        "Cards: white with 1px border (#d4cec4), conservative 4px radius. No rounded corners "
        "greater than 6px. Section spacing: generous but traditional (40-60px padding). "
        "Footer: navy background, white/gold text, traditional 3-column layout."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8 · Music Streaming — SoundWave · Gradient Dark · Medium
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register_config("music_streaming_gradient_medium")
class MusicStreamingGradientMediumConfig(_Base):
    ARCHETYPE    = "music_streaming"
    VISUAL_STYLE = "gradient_dark"
    DIFFICULTY   = "medium"
    BRAND_NAME   = "SoundWave"
    BRAND_TAGLINE = "Feel every frequency"
    COLORS = {
        "background":    "#0f0f23",
        "surface":       "#1a1a35",
        "border":        "#2d2d55",
        "primary":       "#e040fb",
        "accent":        "#00e5ff",
        "text_primary":  "#ffffff",
        "text_secondary":"#9999cc",
        "cta":           "#e040fb",
    }
    FONTS = ["Outfit", "system-ui", "sans-serif"]
    PAGES = [
        {"name": "page_home",      "file": "index.html",     "label": "Home",
         "description": "Vibrant hero with purple-to-cyan gradient background, large headline "
                        "'Feel Every Frequency', 'Start Listening Free' CTA; featured playlists: "
                        "4 cards with gradient-colored placeholders (Chill Vibes, Workout Energy, "
                        "Focus Flow, Late Night); trending section: 6 album/track cards with "
                        "cover art placeholder, artist name, track title; genre clouds section "
                        "(8 genre pills: Pop, Hip-Hop, Electronic, Rock, Jazz, Classical, Latin, "
                        "K-Pop); stats strip (80M tracks, 4B playlists, 600M listeners)"},
        {"name": "page_discover",  "file": "discover.html",  "label": "Discover",
         "description": "Discover page: curated sections — 'New Releases' (6 album cards), "
                        "'Charts' (3 chart cards: Global Top 50, Viral, Rising), 'Podcasts' "
                        "(4 podcast cards); genre browser: 12 genre tiles in 4×3 grid with "
                        "gradient backgrounds and genre names; mood-based playlists section"},
        {"name": "page_pricing",   "file": "pricing.html",   "label": "Premium",
         "description": "Premium plans page: 3 tiers (Free $0, Premium $9.99/mo, Family "
                        "$14.99/mo) as cards with feature lists; comparison table (8 features "
                        "× 3 plans); student discount section; free trial CTA; FAQ (6 questions)"},
        {"name": "page_artists",   "file": "artists.html",   "label": "Artists",
         "description": "Artists hub: featured artist spotlight with large placeholder and bio; "
                        "top artists grid (8 circular placeholders with names and genre); "
                        "'For Artists' section explaining SoundWave for Artists program; "
                        "upload stats and earnings info; artist registration CTA"},
        {"name": "page_contact",   "file": "contact.html",   "label": "Support",
         "description": "Support page: 3 help categories (Account, Playback, Payments) with "
                        "icon and description; search-bar-styled help lookup; community forum "
                        "link; contact form (email, subject, category dropdown, description); "
                        "social media links; app download links section"},
    ]
    DESIGN_DIRECTIVES = (
        "Deep indigo background (#0f0f23). Magenta/pink (#e040fb) as the primary brand color "
        "for CTAs, active states, and gradients. Electric cyan (#00e5ff) as the secondary "
        "accent for highlights and hover effects. Use CSS gradients extensively: purple↔cyan "
        "for hero, magenta↔blue for cards. Navigation: dark transparent with magenta active "
        "state and pill-shaped active indicator. Cards: dark surface (#1a1a35), 12px radius, "
        "gradient border on hover. Playlist/album cards: 8px radius, cover art placeholder "
        "with gradient overlays. Buttons: magenta gradient fill primary, cyan outlined "
        "secondary. Typography: Outfit — geometric and modern. Genre pills: gradient "
        "backgrounds with white text. Footer: #0a0a1a with gradient accent line."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 9 · Food Delivery — BiteBuzz · Playful Modern · Medium
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register_config("food_delivery_playful_medium")
class FoodDeliveryPlayfulMediumConfig(_Base):
    ARCHETYPE    = "food_delivery"
    VISUAL_STYLE = "playful_modern"
    DIFFICULTY   = "medium"
    BRAND_NAME   = "BiteBuzz"
    BRAND_TAGLINE = "Delicious, delivered in minutes"
    COLORS = {
        "background":    "#ffffff",
        "surface":       "#fff5f0",
        "border":        "#ffd6c4",
        "primary":       "#ff5722",
        "accent":        "#4caf50",
        "text_primary":  "#1a1a1a",
        "text_secondary":"#666666",
        "cta":           "#ff5722",
    }
    FONTS = ["Nunito", "system-ui", "sans-serif"]
    PAGES = [
        {"name": "page_home",        "file": "index.html",       "label": "Home",
         "description": "Fun, energetic hero with white bg and large playful illustration-style "
                        "colored shapes (CSS circles/blobs), large bold headline 'Delicious, "
                        "Delivered in Minutes', address input bar with 'Find Food' orange button; "
                        "cuisine carousel-style strip (8 cuisine circles: Pizza, Sushi, Burger, "
                        "Thai, Indian, Mexican, Salad, Dessert) with emoji-style labels; popular "
                        "restaurants: 4 cards (name, cuisine type, delivery time, rating stars, "
                        "delivery fee); how it works: 3 steps (Browse, Order, Enjoy) with numbered "
                        "circles; download app section; partner restaurant CTA"},
        {"name": "page_restaurants", "file": "restaurants.html", "label": "Restaurants",
         "description": "Restaurant listing: filter bar (Cuisine, Rating, Delivery Time, Price "
                        "Range, Dietary: Vegan/Halal/Gluten-Free); restaurant grid (9 cards) each "
                        "with image placeholder, name, cuisine tags, rating, delivery time, min "
                        "order, 'Order Now' button; sort options (Recommended, Rating, Delivery "
                        "Time, Price); map-view toggle visual"},
        {"name": "page_deals",       "file": "deals.html",       "label": "Deals",
         "description": "Deals & promotions: hero banner 'Save Big This Week'; featured deal "
                        "card (50% off first order); 3-column deal cards (6 deals) each with "
                        "restaurant, discount amount, valid dates, and claim CTA; loyalty program "
                        "section explaining BiteBuzz Points; referral program section"},
        {"name": "page_partner",     "file": "partner.html",     "label": "Partner",
         "description": "Partner with us page: two-column hero (benefits text + restaurant "
                        "illustration placeholder); stats (10K+ restaurants, 50 cities, 2M "
                        "orders/month); partnership tiers (Basic, Premium, Enterprise) with "
                        "features; success stories (3 restaurant testimonials); partner signup "
                        "form (restaurant name, owner name, email, phone, cuisine, location)"},
        {"name": "page_contact",     "file": "contact.html",     "label": "Help",
         "description": "Help center: 3 quick action cards (Track Order, Refund Request, Report "
                        "Issue); FAQ accordion (8 questions in categories: Orders, Payments, "
                        "Account); contact form (order number, email, issue type, description); "
                        "live chat CTA; social media links; app download badges"},
    ]
    DESIGN_DIRECTIVES = (
        "Clean white background (#ffffff). Vibrant orange (#ff5722) as the primary action color "
        "— CTAs, ratings, brand elements. Green (#4caf50) as the positive/success accent for "
        "delivery badges, confirmations, and secondary buttons. Navigation: white with shadow, "
        "orange logo and active state, rounded 'Order Now' button. Cards: white with subtle "
        "warm shadow, 16px border-radius, playful and rounded. Buttons: orange fill, 24px "
        "border-radius (pill-shaped) primary; green for success actions. Cuisine circles: "
        "colored background circles with emoji text. Typography: Nunito — rounded and friendly. "
        "Decorative: use CSS circles and rounded shapes as background elements. Rating stars: "
        "orange. Footer: warm #fff5f0, 4 columns, fun and approachable."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 10 · Architecture Studio — Forma Studio · Monochrome · Hard
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register_config("architecture_studio_mono_hard")
class ArchitectureStudioMonoHardConfig(_Base):
    ARCHETYPE    = "architecture_studio"
    VISUAL_STYLE = "monochrome"
    DIFFICULTY   = "hard"
    BRAND_NAME   = "Forma Studio"
    BRAND_TAGLINE = "Where structure meets imagination"
    COLORS = {
        "background":    "#ffffff",
        "surface":       "#f5f5f5",
        "border":        "#e0e0e0",
        "primary":       "#1a1a1a",
        "accent":        "#666666",
        "text_primary":  "#1a1a1a",
        "text_secondary":"#888888",
        "cta":           "#1a1a1a",
    }
    FONTS = ["Archivo", "Helvetica Neue", "Arial", "sans-serif"]
    PAGES = [
        {"name": "page_home",     "file": "index.html",    "label": "Home",
         "description": "Dramatic monochrome hero: full-width image placeholder (architectural "
                        "render), overlaid with large sans-serif headline 'WHERE STRUCTURE MEETS "
                        "IMAGINATION' in tracking-wide uppercase; selected projects section: "
                        "4 projects in a 2×2 asymmetric grid with varied image placeholder sizes, "
                        "project name, location, year; studio philosophy: large centered statement "
                        "in thin weight; project categories strip (Residential, Commercial, "
                        "Cultural, Urban); awards ticker (AIA Honor Award, Dezeen Award, Pritzker "
                        "Nominee); press mentions section"},
        {"name": "page_projects", "file": "projects.html", "label": "Projects",
         "description": "Projects archive: filter by typology (All / Residential / Commercial / "
                        "Cultural / Urban / Interior); projects in alternating full-width and "
                        "half-width layout (10 projects) each with large image placeholder, "
                        "project name in uppercase, location, year, brief (1 line), and area "
                        "(sqm); hover reveals 'View Project' overlay; project counter showing "
                        "'Showing 10 of 47 projects'"},
        {"name": "page_approach", "file": "approach.html", "label": "Approach",
         "description": "Design philosophy page: manifesto section with large justified text; "
                        "4-phase process (Research, Concept, Development, Realization) each as "
                        "a full-width horizontal band with phase number, title, description, "
                        "and methodology detail; sustainability section with 6 principles in "
                        "2×3 grid; materials palette section showcasing 8 materials (name and "
                        "description); technology section about BIM/parametric design"},
        {"name": "page_studio",   "file": "studio.html",   "label": "Studio",
         "description": "Studio page: large office photo placeholder; about text in two columns; "
                        "team grid: 8 people (photo placeholder, name, role, joined year) in "
                        "4-column layout; timeline: founding 2008 to present (6 milestones); "
                        "publications section (4 books/papers); internship and careers section; "
                        "collaborators/consultants list"},
        {"name": "page_contact",  "file": "contact.html",  "label": "Contact",
         "description": "Minimal contact: large 'Get in Touch' in thin uppercase sans-serif; "
                        "two-column: left has inquiry form (name, company, email, project type "
                        "dropdown: Residential/Commercial/Competition/Consultation, project "
                        "location, budget range, timeline, brief description); right has studio "
                        "address, working hours, map placeholder, press contact, and career "
                        "inquiries email; bottom: Instagram grid placeholder (6 squares)"},
    ]
    DESIGN_DIRECTIVES = (
        "Pure white background (#ffffff). Pure monochrome palette — only black (#1a1a1a), "
        "white, and grays (#666666, #888888, #e0e0e0, #f5f5f5). No color accents at all. "
        "Typography: Archivo/Helvetica Neue — clean geometric sans-serif. Headings: uppercase, "
        "letter-spacing 0.1-0.3em, thin weight (300-400). Navigation: white background, black "
        "text, no decoration — extremely minimal. Layout: use CSS grid with sophisticated "
        "asymmetric columns and varied row heights for project grids. Full-bleed images and "
        "generous whitespace. No border-radius — all sharp corners. Buttons: black fill with "
        "white text or outlined black, no radius. Thin 1px rules (#e0e0e0) for section "
        "separators. Footer: white with thin black top border, minimal single row."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 11 · Portfolio Animation · Studio Lumina · Elegant Minimal · Medium
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register_config("portfolio_animation_medium")
class PortfolioAnimationMediumConfig(_Base):
    RECIPE_VERSION = "v2"
    ARCHETYPE    = "portfolio_animation"
    VISUAL_STYLE = "elegant_minimal"
    DIFFICULTY   = "medium"
    BRAND_NAME   = "Studio Lumina"
    BRAND_TAGLINE = "Living design through motion"
    ANIMATION_FRAMES_MS = [0, 500, 1200]
    STATIC_WEIGHT = 0.6
    ANIMATION_WEIGHT = 0.4
    COLORS = {
        "background":    "#0f0f12",
        "surface":       "#1a1a20",
        "border":        "#33333d",
        "primary":       "#ffffff",
        "accent":        "#ff5533",
        "text_primary":  "#f0f0f5",
        "text_secondary":"#9999a3",
        "cta":           "#ff5533",
    }
    FONTS = ["Inter", "system-ui", "sans-serif"]
    PAGES = [
        {"name": "page_home",     "file": "index.html",    "label": "Home",
         "description": "Hero section with large headline 'Living design through motion' that fades in and slides up; "
                        "portfolio grid of 6 project cards that fade in with a staggered animation delay (0.1s to 0.6s); "
                        "about section with sliding text overlay; footer with glowing accent bar."},
        {"name": "page_projects", "file": "projects.html", "label": "Projects",
         "description": "Projects gallery with 12 items; each row of projects slides in from the bottom with a smooth "
                        "cubic-bezier easing; category filter bar with animated bottom border on active item."},
        {"name": "page_process",  "file": "process.html",  "label": "Process",
         "description": "4-step process timeline (Discovery, Strategy, Design, Motion); each step card animates in "
                        "sequentially as if scrolling into view; large typography numbers (01, 02, 03, 04) with pulse animation."},
        {"name": "page_about",    "file": "about.html",    "label": "About",
         "description": "About page with large hero image placeholder that scales up smoothly from 0.95 to 1.0 scale; "
                        "team grid of 4 profiles with staggered fade-in; values list with sliding underline animations."},
        {"name": "page_contact",  "file": "contact.html",  "label": "Contact",
         "description": "Contact form with animated input borders that expand on focus; large heading 'Let's create together' "
                        "with subtle floating animation; social media links with bouncy hover animations."}
    ]
    DESIGN_DIRECTIVES = (
        "Dark theme (#0f0f12) with vibrant coral accent (#ff5533). CRITICAL ANIMATION REQUIREMENT: "
        "Use CSS `@keyframes` and `animation` properties extensively. All major sections (hero, project cards, "
        "timeline steps) MUST start in an initial hidden state (e.g., `opacity: 0; transform: translateY(30px);`) "
        "and animate to `opacity: 1; transform: translateY(0);` over 0.8s to 1.2s using smooth easing (`cubic-bezier(0.16, 1, 0.3, 1)`). "
        "Use staggered `animation-delay` (e.g., `0.1s`, `0.2s`, `0.3s`) for grid items so they appear sequentially. "
        "Ensure `animation-fill-mode: forwards` is set so elements stay visible after animating."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 12 · SaaS Animation · FlowSync · Modern Tech · Hard
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register_config("saas_animation_hard")
class SaaSAnimationHardConfig(_Base):
    RECIPE_VERSION = "v2"
    ARCHETYPE    = "saas_animation"
    VISUAL_STYLE = "modern_tech"
    DIFFICULTY   = "hard"
    BRAND_NAME   = "FlowSync"
    BRAND_TAGLINE = "Automate your workflow at the speed of thought"
    ANIMATION_FRAMES_MS = [0, 500, 1200]
    STATIC_WEIGHT = 0.6
    ANIMATION_WEIGHT = 0.4
    COLORS = {
        "background":    "#ffffff",
        "surface":       "#f8fafc",
        "border":        "#e2e8f0",
        "primary":       "#0f172a",
        "accent":        "#3b82f6",
        "text_primary":  "#1e293b",
        "text_secondary":"#64748b",
        "cta":           "#3b82f6",
    }
    FONTS = ["Roboto", "system-ui", "sans-serif"]
    PAGES = [
        {"name": "page_home",     "file": "index.html",    "label": "Home",
         "description": "SaaS landing hero with headline 'Automate your workflow at the speed of thought' sliding in from left; "
                        "hero dashboard mockup placeholder sliding in from right; 3 feature cards with staggered fade-in; "
                        "live metrics counter simulation with pulse animation; client logos strip with infinite scroll animation."},
        {"name": "page_features", "file": "features.html", "label": "Features",
         "description": "Deep-dive features page; 6 alternating left/right sections; each text block slides in from the side "
                        "while the corresponding diagram placeholder fades in; interactive-looking comparison table with hover row highlights."},
        {"name": "page_pricing",  "file": "pricing.html",  "label": "Pricing",
         "description": "3 pricing tiers (Starter, Pro, Enterprise); Pro tier card is highlighted and animates with a subtle "
                        "scale-up and glowing blue border; FAQ section with animated expand/collapse arrows."},
        {"name": "page_docs",     "file": "docs.html",     "label": "Documentation",
         "description": "Documentation layout with left sidebar and right content area; sidebar links slide in from left; "
                        "code snippet boxes with animated copy button tooltips; step-by-step quickstart guide with staggered fade-in."},
        {"name": "page_contact",  "file": "contact.html",  "label": "Contact",
         "description": "Contact sales form with smooth slide-up animation; office locations grid with bouncing pin icon placeholders; "
                        "support ticket CTA banner with gradient background animation."}
    ]
    DESIGN_DIRECTIVES = (
        "Clean modern SaaS light theme (#ffffff) with bright blue accent (#3b82f6). CRITICAL ANIMATION REQUIREMENT: "
        "Implement sophisticated CSS animations for all page entrances. Use `@keyframes slideInLeft`, `@keyframes slideInRight`, "
        "and `@keyframes fadeInUp`. Elements must be hidden initially (`opacity: 0`) and use `animation-fill-mode: forwards`. "
        "For grid and list elements, apply staggered delays (`animation-delay: 0.1s`, `0.2s`, etc.) to create a dynamic, "
        "premium feel. Use `cubic-bezier(0.22, 1, 0.36, 1)` for snappy, professional motion."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 13 · Creative Agency Animation · Prism Studio · Bold Gradient · Medium
#     SLOW animations: 1.5–2.0s durations, large stagger delays (0.3–1.0s)
#     to ensure t=500 and t=1200 look distinctly different.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register_config("agency_animation_medium")
class AgencyAnimationMediumConfig(_Base):
    RECIPE_VERSION = "v2"
    ARCHETYPE    = "agency_animation"
    VISUAL_STYLE = "bold_gradient"
    DIFFICULTY   = "medium"
    BRAND_NAME   = "Prism Studio"
    BRAND_TAGLINE = "Where ideas take shape"
    ANIMATION_FRAMES_MS = [0, 500, 1200]
    STATIC_WEIGHT = 0.6
    ANIMATION_WEIGHT = 0.4
    COLORS = {
        "background":    "#0a0a0f",
        "surface":       "#151520",
        "border":        "#2a2a3a",
        "primary":       "#ffffff",
        "accent":        "#a855f7",
        "accent_warm":   "#ec4899",
        "text_primary":  "#f5f5ff",
        "text_secondary":"#8888aa",
        "cta":           "#a855f7",
    }
    FONTS = ["Outfit", "system-ui", "sans-serif"]
    PAGES = [
        {"name": "page_home",     "file": "index.html",    "label": "Home",
         "description": "Hero with headline 'Where ideas take shape' — each word appears one at a time with a "
                        "2.0s `@keyframes wordReveal` animation using `animation-delay: 0s, 0.4s, 0.8s, 1.2s` for each word. "
                        "Words start invisible (`opacity: 0; transform: translateY(40px)`) and slide up. "
                        "Below the hero: 3 large service cards (Strategy, Design, Build) that each have a 1.5s fade-in "
                        "with stagger delays of `0.3s, 0.6s, 0.9s` — at t=500ms only the first card should be partially visible. "
                        "Bottom: client logo bar with a slow 1.8s opacity fade."},
        {"name": "page_work",     "file": "work.html",     "label": "Work",
         "description": "Portfolio grid with 8 project cards arranged 2×4. Each card uses a 1.5s `@keyframes slideUp` "
                        "with stagger delays of `0.15s` between cards (0.15s, 0.30s, 0.45s, ... 1.20s). "
                        "At t=500ms, only the first 3 cards should be partially visible; at t=1200ms all 8 should be visible. "
                        "Each card slides up from `translateY(60px)` with `opacity: 0`. Category filters at top with a "
                        "separate 1.2s slide-down animation."},
        {"name": "page_services", "file": "services.html", "label": "Services",
         "description": "5 service sections stacked vertically, each with icon + title + description. "
                        "Each section uses a 2.0s `@keyframes expandIn` (starts at `scale(0.8); opacity: 0;` → `scale(1); opacity: 1;`). "
                        "Stagger delays: `0s, 0.5s, 1.0s, 1.5s, 2.0s`. At t=500ms only the first section is visible; "
                        "at t=1200ms the first 3 are visible; the last 2 are still hidden. "
                        "Purple-to-pink gradient accent line between sections with a 2.5s width animation from 0% to 100%."},
        {"name": "page_about",    "file": "about.html",    "label": "About",
         "description": "About page with a large team photo placeholder that uses a 2.0s `@keyframes clipReveal` — "
                        "starts with `clip-path: inset(0 100% 0 0)` and reveals to `clip-path: inset(0 0 0 0)`. "
                        "Below: 4 team member cards with 1.5s fade-in, staggered by 0.4s each (0.4s, 0.8s, 1.2s, 1.6s). "
                        "Stats counter section (150+, 50+, 12) with a 1.8s scale-up animation starting at delay 0.6s."},
        {"name": "page_contact",  "file": "contact.html",  "label": "Contact",
         "description": "Contact form where each input field slides in from the left with a 1.5s animation, "
                        "staggered by 0.3s per field (5 fields: 0.3s, 0.6s, 0.9s, 1.2s, 1.5s). "
                        "Submit button fades in last with a 1.0s delay of 1.8s. Map placeholder on the right "
                        "uses a 2.0s fade-in starting at 0.5s delay."}
    ]
    DESIGN_DIRECTIVES = (
        "Dark theme (#0a0a0f) with purple-to-pink gradient accents. CRITICAL ANIMATION REQUIREMENT: "
        "All animations MUST be SLOW — use durations of 1.5s to 2.5s (NOT 0.8s). This is essential. "
        "Use large `animation-delay` values to create heavy staggering: first element at 0s, second at 0.3s-0.5s, "
        "third at 0.6s-1.0s, etc. This ensures intermediate frames at t=500ms look VERY different from t=1200ms. "
        "Keyframes should use smooth easing: `cubic-bezier(0.25, 0.1, 0.25, 1.0)` (ease). "
        "All animated elements MUST start hidden (`opacity: 0; transform: translateY(40px);`) and MUST set "
        "`animation-fill-mode: forwards`. DO NOT use fast animations under 1.0s duration."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 14 · Fintech Dashboard Animation · Vault · Dark Precision · Hard
#     MULTI-PHASE animations: elements fade in, then slide, then glow.
#     Extra capture at t=1800ms for very slow stagger.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register_config("fintech_animation_hard")
class FintechAnimationHardConfig(_Base):
    RECIPE_VERSION = "v2"
    ARCHETYPE    = "fintech_animation"
    VISUAL_STYLE = "dark_precision"
    DIFFICULTY   = "hard"
    BRAND_NAME   = "Vault"
    BRAND_TAGLINE = "Your wealth, engineered"
    ANIMATION_FRAMES_MS = [0, 500, 1200, 1800]
    STATIC_WEIGHT = 0.5
    ANIMATION_WEIGHT = 0.5
    COLORS = {
        "background":    "#09090b",
        "surface":       "#18181b",
        "surface_alt":   "#27272a",
        "border":        "#3f3f46",
        "primary":       "#fafafa",
        "accent":        "#10b981",
        "accent_warm":   "#f59e0b",
        "danger":        "#ef4444",
        "text_primary":  "#fafafa",
        "text_secondary":"#a1a1aa",
        "cta":           "#10b981",
    }
    FONTS = ["Inter", "system-ui", "sans-serif"]
    PAGES = [
        {"name": "page_home",     "file": "index.html",    "label": "Home",
         "description": "Fintech landing with headline 'Your wealth, engineered' using a 2.5s multi-phase keyframe: "
                        "phase 1 (0%-40%): fade in from `opacity: 0` to `opacity: 1`; "
                        "phase 2 (40%-70%): slide up from `translateY(20px)` to `translateY(0)`; "
                        "phase 3 (70%-100%): text gets a subtle green glow `text-shadow: 0 0 20px #10b981`. "
                        "3 stats cards (AUM $2.4B, Users 50K+, Uptime 99.99%) each with a 2.0s animation, "
                        "staggered by 0.5s (delays: 0.5s, 1.0s, 1.5s). Dashboard preview mockup on right "
                        "slides in from right with a 2.0s animation starting at delay 0.8s."},
        {"name": "page_features", "file": "features.html", "label": "Features",
         "description": "6 feature cards in a 2×3 grid. Each card has a 2.0s multi-phase animation: "
                        "phase 1 (0%-50%): scale from `scale(0.85)` to `scale(1)` while fading in; "
                        "phase 2 (50%-100%): border changes from transparent to green `border-color: #10b981`. "
                        "Stagger delays: 0.2s, 0.4s, 0.6s, 0.8s, 1.0s, 1.2s — so at t=500ms only 2 cards are mid-animation, "
                        "at t=1200ms all 6 are visible but only 4 have completed their border color change."},
        {"name": "page_pricing",  "file": "pricing.html",  "label": "Pricing",
         "description": "3 pricing tiers side by side. Each tier card uses a 1.8s `@keyframes slideUpFade` "
                        "with delays of 0.3s, 0.7s, 1.1s. The middle 'Pro' card has an additional 2.5s "
                        "`@keyframes glowPulse` that starts AFTER the slide (delay 1.5s): "
                        "the border alternates between `#10b981` and `#10b981/50%` opacity. "
                        "At t=500ms only the first card is visible; at t=1200ms all 3 visible but Pro hasn't started glowing yet; "
                        "at t=1800ms the Pro card is actively glowing."},
        {"name": "page_security", "file": "security.html", "label": "Security",
         "description": "Security page with a large shield icon placeholder in the center that uses a 3.0s "
                        "`@keyframes shieldReveal`: phase 1 (0%-30%): fade in; phase 2 (30%-60%): scale from 0.7 to 1.0; "
                        "phase 3 (60%-100%): green glow appears around the shield. "
                        "Below: 4 security feature rows that slide in from alternating left/right sides, "
                        "each with 1.5s duration and stagger delays of 0.4s, 0.8s, 1.2s, 1.6s. "
                        "Compliance badges at bottom fade in with 2.0s animation starting at delay 1.8s."},
        {"name": "page_contact",  "file": "contact.html",  "label": "Contact",
         "description": "Contact form with a 2-column layout. Left column (company info) slides in from left "
                        "with 2.0s animation. Right column (form fields) — each of 6 fields slides up with 1.5s animation, "
                        "staggered by 0.25s (delays: 0.3s, 0.55s, 0.80s, 1.05s, 1.30s, 1.55s). "
                        "CTA button at bottom uses a 1.0s animation starting at delay 2.0s. "
                        "At t=500ms only the left column and first 1-2 fields are visible; "
                        "at t=1200ms most fields visible but button hidden; at t=1800ms everything visible."}
    ]
    DESIGN_DIRECTIVES = (
        "Ultra-dark fintech theme (#09090b) with emerald green accent (#10b981) and amber warning (#f59e0b). "
        "CRITICAL ANIMATION REQUIREMENT: Use MULTI-PHASE `@keyframes` with 3+ stages. Example: "
        "`@keyframes cardReveal { 0% { opacity: 0; transform: scale(0.85); border-color: transparent; } "
        "50% { opacity: 1; transform: scale(1); border-color: transparent; } "
        "100% { opacity: 1; transform: scale(1); border-color: #10b981; } }`. "
        "All durations MUST be 1.5s to 3.0s — NO fast animations under 1.0s. "
        "Use LARGE stagger delays (0.3s to 0.5s between items) so that at t=500ms only 1-2 elements are visible, "
        "at t=1200ms 4-5 elements are visible, and at t=1800ms everything is fully settled. "
        "All animated elements start hidden (`opacity: 0`) with `animation-fill-mode: forwards`. "
        "Use `cubic-bezier(0.33, 1, 0.68, 1)` for smooth deceleration."
    )

