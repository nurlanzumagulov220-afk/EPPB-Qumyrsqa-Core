import json

def fetch_egov_profile(iin_bin):
    mock_db = {
        "123456789012": {
            "name": "ТОО 'Qumyrsqa Logistics'",
            "company_age_years": 3,
            "status": "Активное"
        },
        "987654321098": {
            "name": "ИП 'Синтетика Тестовна'",
            "company_age_years": 1,
            "status": "Активное"
        }
    }
    return mock_db.get(iin_bin, {"error": "Профиль не найден"})
