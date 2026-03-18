import json, random, re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPICS_FILE = ROOT / "topics.json"
BLOG_DIR = ROOT / "blog"
MANIFEST_FILE = BLOG_DIR / "manifest.json"
USED_FILE = ROOT / "scripts" / "used_topics.json"

STORE_NAME = "Smoke 4 Less"
CITY = "Martin City Kansas City, MO"
ADDRESS = "13608 Washington St, Kansas City, MO 64145"
PHONE = "(816) 216-1111"
GBP = "https://share.google/iJc83uCYrp9FU4gzd"

IMAGE_MAP = {
    "Vapes & Disposables": "../images/vapes.png",
    "Cigars & Wraps": "../images/cigars.png",
    "Hookah & Shisha": "../images/hookah.png",
    "Kratom": "../images/kratom.png",
    "THCA Flower": "../images/thca.png",
    "Gummies": "../images/gummies.png",
    "Detox Products": "../images/detox.png",
    "Grinders": "../images/grinders.png",
    "Glass": "../images/glass.png",
    "Rolling Papers": "../images/papers.png",
    "Accessories": "../images/accessories.png",
    "Vaporizers": "../images/vaporizer.png"
}

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return re.sub(r"-+", "-", text)

def load_json(path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default

def save_json(path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

def pick_topic():
    topics = load_json(TOPICS_FILE, {"topics": []})["topics"]
    used = load_json(USED_FILE, [])
    used_ids = set(used)
    available = [t for t in topics if t["id"] not in used_ids]
    if not available:
        used = []
        available = topics
    topic = random.choice(available)
    used.append(topic["id"])
    save_json(USED_FILE, used)
    return topic

def build_post(topic):
    title = topic["title"]
    excerpt = f"{title} - visit Smoke 4 Less, a smoke shop in Martin City Kansas City, MO, at 13608 Washington St, Kansas City, MO 64145."
    image = IMAGE_MAP.get(topic["category"], "../images/logo.png")
    content_html = f'''
    <img class="blog-featured-image" src="{image}" alt="{title}">
    <p>If you are looking for a <strong>smoke shop in Martin City Kansas City</strong>, Smoke 4 Less offers a convenient local place to browse {topic["category"].lower()}, new arrivals, and everyday smoke shop essentials.</p>
    <h2>Why local shoppers search for {topic["category"]}</h2>
    <p>People searching for a <strong>smoke shop Kansas City</strong> or a <strong>vape shop Kansas City</strong> often want a clean store, good selection, helpful staff, and products they can see in person before they buy. Local shopping guides help customers compare options and make faster decisions.</p>
    <h2>What to look for before buying</h2>
    <p>When shopping for {topic["category"].lower()}, it helps to compare product style, build quality, size, design, and accessories. Many customers also want to know what is popular right now, what fits their budget, and what works well for beginners versus regular shoppers.</p>
    <h2>Visit Smoke 4 Less in Martin City Kansas City</h2>
    <p>Smoke 4 Less is located at <strong>{ADDRESS}</strong>. If you are searching for a <strong>Martin City smoke shop</strong> or a <strong>smoke shop near 64145</strong>, stop by to browse products in person. You can also call <strong>{PHONE}</strong> before visiting.</p>
    <h2>Find directions and store details</h2>
    <p>For directions, search Smoke 4 Less in Google Maps or visit our Google Business listing. Our store serves shoppers looking for a smoke shop, vape shop, glass, wraps, hookah, gummies, vaporizers, and accessories in Kansas City, MO.</p>
    <p>This post is part of our daily local content series for Martin City Kansas City, MO.</p>
    '''
    return title, excerpt, content_html, image

def build_html(title, excerpt, content_html, filename, image):
    image_absolute = image.replace("../", "https://smoke4lesskc.com/")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | Smoke 4 Less</title>
  <meta name="description" content="{excerpt}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://smoke4lesskc.com/blog/{filename}" />
  <link rel="stylesheet" href="../styles.css" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{title}",
    "description": "{excerpt}",
    "image": "{image_absolute}",
    "author": {{
      "@type": "Organization",
      "name": "{STORE_NAME}"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "{STORE_NAME}",
      "logo": {{
        "@type": "ImageObject",
        "url": "https://smoke4lesskc.com/images/logo.png"
      }}
    }},
    "mainEntityOfPage": "https://smoke4lesskc.com/blog/{filename}"
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://smoke4lesskc.com/index.html"
      }},
      {{
        "@type": "ListItem",
        "position": 2,
        "name": "Blog",
        "item": "https://smoke4lesskc.com/blog.html"
      }},
      {{
        "@type": "ListItem",
        "position": 3,
        "name": "{title}",
        "item": "https://smoke4lesskc.com/blog/{filename}"
      }}
    ]
  }}
  </script>
</head>
<body>
  <header class="site-header">
    <div class="container nav-bar">
      <div class="brand">
        <img src="../images/logo.png" alt="Smoke 4 Less Logo" class="logo" />
        <div><h1>Smoke 4 Less</h1><p class="tagline">Martin City Kansas City Smoke Shop</p></div>
      </div>
      <nav class="nav-links">
        <a href="../index.html#products">Products</a>
        <a href="../blog.html" class="call-btn">Blog</a>
        <a href="https://www.google.com/maps/dir/?api=1&destination=13608+Washington+St+Kansas+City+MO+64145" target="_blank" rel="noopener noreferrer">Directions</a>
        <a href="tel:18162161111" class="call-btn">Call Now</a>
      </nav>
    </div>
  </header>
  <main>
    <section class="hero blog-hero compact-blog-hero">
      <div class="container">
        <span class="badge">Daily Blog</span>
        <h2>{title}</h2>
        <p>{excerpt}</p>
      </div>
    </section>
    <section class="products-section">
      <div class="container">
        <article class="hero-info-card blog-article">
          {content_html}
          <p><strong>Store:</strong> {STORE_NAME}</p>
          <p><strong>Address:</strong> {ADDRESS}</p>
          <p><strong>Phone:</strong> <a class="review-link" href="tel:18162161111">{PHONE}</a></p>
          <p><strong>Google Business:</strong> <a class="review-link" href="{GBP}" target="_blank" rel="noopener noreferrer">View us on Google</a></p>
        </article>
      </div>
    </section>
  </main>
  <footer class="site-footer">
    <div class="container footer-grid">
      <div><h3>Smoke 4 Less</h3><p>Smoke Shop Kansas City | Vape Shop Kansas City</p></div>
      <div><h4>Store Info</h4><p>{ADDRESS}</p><p>{PHONE}</p></div>
      <div><h4>Popular Searches</h4><p>Smoke Shop Kansas City</p><p>Vape Shop Kansas City</p><p>Kratom Kansas City</p></div>
    </div>
    <div class="footer-bottom"><p>&copy; 2026 Smoke 4 Less</p></div>
  </footer>
</body>
</html>'''

def prune_posts(posts):
    cutoff = datetime.now(timezone.utc) - timedelta(days=60)
    keep = []
    for post in posts:
        dt = datetime.fromisoformat(post["created_at"])
        fp = BLOG_DIR / post["filename"]
        if dt >= cutoff:
            keep.append(post)
        elif fp.exists():
            fp.unlink()
    return keep

def main():
    BLOG_DIR.mkdir(exist_ok=True)
    topic = pick_topic()
    title, excerpt, content_html, image = build_post(topic)
    now = datetime.now(timezone.utc)
    filename = slugify(now.strftime("%Y-%m-%d") + "-" + title) + ".html"
    html = build_html(title, excerpt, content_html, filename, image)
    (BLOG_DIR / filename).write_text(html, encoding="utf-8")

    posts = load_json(MANIFEST_FILE, [])
    posts = prune_posts(posts)
    posts.insert(0, {
        "title": title,
        "excerpt": excerpt,
        "filename": filename,
        "date": now.strftime("%b %d, %Y"),
        "created_at": now.isoformat(),
        "image": image.replace("../", "")
    })
    posts = posts[:60]
    save_json(MANIFEST_FILE, posts)

if __name__ == "__main__":
    main()
