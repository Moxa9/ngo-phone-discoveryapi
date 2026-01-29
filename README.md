
📌 NGO Phone Discovery API

A production-ready FastAPI backend that automatically discovers publicly available office phone numbers of NGOs using web crawling and search-based domain discovery.
The system includes confidence scoring, structured logging, and batch CSV processing, and is deployed with live Swagger documentation.
📌Live API:
        https://ngo-phone-discoveryapi.onrender.com
🚀 Features

    🔍 Automatic discovery of NGO websites using search-based heuristics
    
    📞 Extraction of publicly available office phone numbers
    
    📊 Heuristic-based confidence scoring for reliability assessment
    
    🧾 Structured logging for observability and debugging
    
    📂 Batch processing support for large NGO CSV datasets
    
    📘 Interactive API documentation via Swagger UI
    
    ☁️ Cloud deployment with a public API endpoint

🧠 How It Works

    Accepts NGO name, location, and optional email
    
    Identifies the official NGO website
    
    Crawls public pages (home, contact, about)
    
    Extracts phone numbers using pattern matching
    
    Assigns a confidence score based on source and frequency
    
    Returns phone number, confidence score, and source URL

🛠️ Tech Stack

    Backend: FastAPI (Python)
    
    Web Crawling: Requests, BeautifulSoup
    
    Data Processing: Pandas
    
    Logging: Python logging module
    
    Deployment: Render
    
    Documentation: Swagger (OpenAPI)

📂 API Endpoints
      Health Check
      GET /health

Discover NGO Phone Number
      POST /discover-phone


Request

      {
        "ngo_name": "AL SHIFA Foundation",
        "location": "Telangana"
      }


Response

      {
        "ngo_name": "AL SHIFA Foundation",
        "phone": "+91XXXXXXXXXX",
        "confidence": 0.8,
        "source": "https://example.org/contact",
        "status": "found"
      }

📊 Batch CSV Processing

      Supports batch processing of NGO datasets using a client script that:
      
      Reads NGO details from a CSV file
      
      Calls the API for each NGO
      
      Stores results (phone, confidence, source, status) in a new CSV

⚠️ Important Notes
      
      Only publicly available information is extracted
      
      No private or personal phone numbers are accessed
      
      NGOs without public contact details may return not_found
      
      Results are designed to be assistive, not authoritative

📈 Use Cases

      NGO directories and platforms
      
      Donation and volunteering portals
      
      Data enrichment pipelines
      
      Academic and research projects

🧑‍💻 Author

    Moksha Rathos
    Computer Science & Engineering (Data Science)
    Backend & Data Engineering Enthusiast

📜 License

    This project is intended for educational and research purposes.
