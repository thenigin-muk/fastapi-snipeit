# FastAPI-SnipeIT Integration & OpenAI Chatbot Project

## 🚀 Project Purpose

This project serves as:

- **Proof-of-concept** for integrating OpenAI chatbots with asset management platforms like **Snipe-IT**, while exploring similar integrations.
- A tool for **validating and cleaning data** from multiple carrier CSV files against Snipe-IT to ensure data accuracy and consistency.
- A testing ground to assess the effectiveness and value of conversational agents within our organization.

## 🛠️ Technologies Used

- **FastAPI**: RESTful API framework for Python
- **OpenAI API**: AI conversational assistance
- **Snipe-IT API**: Asset management system integration
- **Azure Bot Service & Teams**: Chatbot hosting and messaging integration
- **Python packages**: `requests`, `httpx`, `dotenv`, `pandas`

## 📁 Project File Structure

```bash
fastapi-snipeit/
├── app/
│   ├── azure_auth.py                 # Azure authentication
│   ├── chat.py                       # Chat endpoints & integrations
│   ├── config.py                     # Configuration utilities
│   ├── main.py                       # FastAPI application entrypoint
│   ├── normalize_carrier.py          # Data normalization from carrier CSV files
│   ├── openai_integration.py         # OpenAI query utilities
│   └── snipeit_api.py                # Snipe-IT API interactions
├── cleaned_data/                     # Debugging output data
│   └── cleaned_carrier_data.json
├── data/                             # Raw carrier CSV files
│   ├── att_devices.csv
│   ├── att_phones.csv
│   ├── tmobile.csv
│   └── verizon.csv
├── logs/                             # Logging for troubleshooting
├── old_py_safe_keeping/              # Old versions for reference
├── venv/                             # Python virtual environment
├── .env                              # Environment variables (API keys, sensitive info)
├── README.md                         # Project documentation
└── requirements.txt                  # Python package dependencies
```

## 🛎️ Installation & Setup

### Step-by-step setup:

1. Clone the repository.

2. Set up and activate the virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure `.env` file using placeholder variables:

```bash
SNIPE_IT_API_KEY=YOUR_SNIPEIT_API_KEY
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
AZURE_BOT_APP_ID=YOUR_AZURE_BOT_APP_ID
AZURE_BOT_APP_PASSWORD=YOUR_AZURE_BOT_APP_PASSWORD
DEBUG=True
```

5. Run the application: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

## 🔎 Current Project Status

### ✅ Completed:

- Initial setup of FastAPI, OpenAI integration, and Snipe-IT integration.
- Data normalization scripts for carrier CSVs.
- Basic chatbot functionality via Azure web test.

### 🚧 In Progress:

- Complete Teams integration and Azure Bot debugging.
- Fine-tuning and testing OpenAI chatbot responses.

### 🐞 Known Issues:

- OpenAI chatbot currently returning incorrect responses (troubleshooting required).
- Azure Bot Service not yet operational in Microsoft Teams.

## 🗺️ Next Steps & Roadmap

- [ ] Resolve Azure Teams integration issues.
- [ ] Validate chatbot accuracy and troubleshoot OpenAI queries.
- [ ] Expand chatbot capabilities to handle broader organizational queries.
- [ ] Explore Microsoft Graph API integration and additional data sources.

## 🎯 Objectives

1. **Proof-of-concept for ChatBot integrations with OpenAI:**
   - Snipe-IT as initial test integration.
   - Explore other potential data sources and APIs.
   - Evaluate conversational AI agents' potential benefits.

2. **Data Validation and Cleanup:**
   - Filtering and cleaning carrier CSV data.
   - Comparing cleaned data against Snipe-IT database.
   - Testing AI-driven data insights and error detection.

## ⚠️ Important Notes on Sensitive Data

Never include `.env` file or sensitive credentials in version control or external sharing. Always use placeholders and provide explicit instructions to securely configure these values for local development and deployments.

Ensure `.gitignore` explicitly excludes sensitive files:

```bash
.env
```

## 📞 Contact

Maintained by: Tim Henigin - City of Mukilteo

# FastAPI Snipe-IT Integration

A FastAPI application that integrates with Snipe-IT asset management system, providing a chatbot interface to query asset information.

## Changelog

### March 13, 2023

- Added integration with OpenAI API for natural language processing of asset queries
- Implemented API endpoints to fetch data from Snipe-IT
- Added support for carrier data normalization (Verizon, T-Mobile, AT&T)
- Enhanced logging system for better debugging capabilities
- Fixed circular import issues between modules
- Added functionality to query assets by tags, names, and assignments
- Improved error handling for API requests
- Configured environment variables for secure API key storage
- Added temporary file storage for debug data

## Setup

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/macOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with the following variables:
   ```
   SNIPE_IT_API_KEY=your_snipe_it_api_key
   OPENAI_API_KEY=your_openai_api_key
   AZURE_BOT_APP_ID=your_azure_bot_app_id
   AZURE_BOT_APP_PASSWORD=your_azure_bot_app_password
   DEBUG=True
   ```
6. Run the application: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

## Usage

The application exposes a `/chat` endpoint that accepts POST requests with natural language queries about Snipe-IT assets.

Example:
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"type":"message","text":"How many laptops do we have?"}'
```

## Debugging

When `DEBUG=True` in the `.env` file, the application will:
- Log detailed information to the logs directory
- Save debug data to the temporary directory
- Output additional console messages

Log files can be found at:
- `/logs/debug.log` - When DEBUG is True
- `/logs/app.log` - Production logs
