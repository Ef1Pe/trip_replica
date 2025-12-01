# Trip.com Replica

A medium-fidelity, production-ready replica of the Trip.com homepage built with semantic HTML, Tailwind CSS (CDN), handcrafted utility CSS, and a lightweight Flask backend for dynamic content injection.

## ✨ Highlights
- Pixel-aligned recreation of hero banner, fare search, coupon carousel, destination inspiration, recommendation grids, and dense footer.
- Five auxiliary section pages (`hotels.html`, `flights.html`, `trains.html`, `cars.html`, `tours.html`) that reuse the design language for vertical-specific storytelling.
- API-ready architecture with data attributes (`data-inject="*"`) that allow runtime card injection from the backend or client-side mock data (`data/mock-data.json`).
- Progressive enhancement via `js/main.js` for fare-tab switching and mock data hydration.

## 🗂️ Project Structure
```
workspace/
├── index.html                 # Homepage replica
├── hotels.html ... tours.html # Section pages
├── css/styles.css             # Custom styling on top of Tailwind
├── js/main.js                 # Tab logic + mock data injection
├── data/mock-data.json        # API-ready placeholder data
├── docs/site_analysis.yaml    # Color, typography, component inventory
├── server.py                  # Flask server with injection helpers
├── metadata.py                # Metadata schema describing injectable fields
├── entity.py                  # Convenience runner for the replica server
└── requirements.txt           # Flask dependency
```

## 🚀 Getting Started
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the development server**
   ```bash
   python server.py
   ```
   The site will be available at `http://localhost:5000`. Static HTML also opens directly in the browser if you prefer pure front-end review.

## 🔌 Dynamic Content Injection
- Each repeatable section exposes a `data-inject="slot-name"` attribute (e.g., `hero-deals`, `destination-grid`, `recommendation-grid`).
- POST arbitrary card data to `/api/inject` with a JSON body:
  ```json
  {
    "section": "index",
    "target": "destination-grid",
    "component": "destination",
    "title": "Lisbon",
    "subtitle": "Tiles, trams, and sunsets",
    "image": "https://example.com/lisbon.jpg",
    "badge": "New"
  }
  ```
- The backend injects the rendered markup before the closing tag of the corresponding container and keeps an in-memory log retrievable from `GET /api/content`.

## 🧱 Front-end Stack
- Tailwind CSS (via CDN) + bespoke CSS for Trip-specific tokens.
- Vanilla JavaScript for tabs, mock content hydration, and accessibility-friendly interactions.
- Responsive layout tested at 1440px (desktop reference) and collapses gracefully to tablet/mobile.

## 📱 Mock Data Layer
`js/main.js` fetches `/data/mock-data.json` to showcase runtime DOM updates with visual indicators (dashed borders + `Injected` badge) so you can see where API-fed content appears.

## ⚠️ Known Limitations
- Images use external Unsplash/CDN links and are not optimized for offline use.
- In-memory injection is non-persistent; restart the Flask server to clear inserted cards.
- Advanced Trip.com features (authentication, localization, loyalty balances) are outside this replica’s scope.

## 📄 License
This replica is for educational/demonstration purposes only and is not affiliated with Trip.com Group.
