# Base URL
BASE_URL = "https://www.healthmug.com"

# Category Labels
HOMEOPATHY = "homeopathy"
AYURVEDA = "ayurveda"
UNANI = "unani"
NUTRITION = "nutrition"
PERSONALCARE = "personalcare"
BABYCARE = "babycare"
FITNESS = "fitness"

# Category Info
CATEGORIES = {
    HOMEOPATHY: {
        "id": 1,
        "url": "/products/homeopathy/1"
    },
    AYURVEDA: {
        "id": 9,
        "url": "/products/ayurveda/9",
    },
    UNANI: {
        "id": 163,
        "url": "/products/unani/163",
    },
    NUTRITION: {
        "id": 122,
        "url": "/products/nutrition-and-supplements/122"
    },
    PERSONALCARE: {
        "id": 82,
        "url": "/products/beauty-and-personal-care/82"
    },
    BABYCARE: {
        "id": 20,
        "url": "/products/baby-care/20"
    },
    FITNESS: {
        "id": 41,
        "url": "/health-aid-and-fitness/41"
    }
}

# Product List API endpoints
URL_PRODUCTLIST = BASE_URL + "/productlist/filterresult?id={category_id}&pgno={pgno}&sortby=1&pagetype=list"

# Log Levels
INFO, DEBUG = "INFO", "DEBUG"
