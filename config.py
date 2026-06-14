# Trusted medical sources 
TRUSTED_SOURCES = [
    "pubmed.ncbi.nlm.nih.gov",
    "nature.com",
    "who.int",
    "mayoclinic.org",
    "nih.gov",
    "medlineplus.gov",
    "cdc.gov",
    "nhs.uk",
    "nejm.org",
    "bmj.com",
]

# model
CLASSIFIER_MODEL = "llama-3.1-8b-instant"
# REFORMULATOR_MODEL = "qwen/qwen3-32b"
REFORMULATOR_MODEL = "llama-3.1-8b-instant"
GENERATION_MODEL = "gemini-3.5-flash"

# Tavily search settings
TAVILY_MAX_RESULTS = 5

# Bot identity
BOT_NAME = "AskPharmova"
BOT_TAGLINE = "Your trusted medical information assistant"
REDIRECT_MESSAGE = "I'm AskPharmova, a medical information assistant. I can only answer questions related to health, medicine, symptoms, treatments, or drugs. Please ask a medically relevant question."