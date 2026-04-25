import json
import os

# 1. справляем том (JSON) без BOM
atom_data = {
    "tamga_id": "018f15a2-8b3d-7c2a-9e4f-556677889900",
    "service_name": "риобретение вагонов в лизинг (с расчетом)",
    "version": "1.1",
    "data_schema": {
        "applicant_iin_bin": { "type": "string", "label": " заявителя", "source": "egov_idp_mock", "editable": False },
        "wagon_type": { "type": "enum", "label": "Тип вагона", "options": ["олувагон", "Цистерна", "ерновоз"], "editable": True },
        "wagon_count": { "type": "integer", "label": "оличество единиц", "editable": True },
        "lease_term_months": { "type": "integer", "label": "Срок лизинга (мес)", "editable": True, "default": 60 },
        "interest_rate": { "type": "float", "label": "Ставка (%)", "editable": False, "default": 14.5 }
    }
}

with open('atoms_vault/leasing_v1.json', 'w', encoding='utf-8') as f:
    json.dump(atom_data, f, ensure_ascii=False, indent=2)

# 2. справляем ендерер (устойчивость к BOM)
renderer_script = """
import json
import sys
import os
import webbrowser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ATOM_PATH = os.path.join(BASE_DIR, '..', 'atoms_vault', 'leasing_v1.json')
STUBS_PATH = os.path.join(BASE_DIR, '..', 'core_stubs')
OUTPUT_HTML = os.path.join(BASE_DIR, 'demo_leasing.html')

sys.path.append(STUBS_PATH)
from egov_mock import fetch_egov_profile

def build_ui(iin):
    print(f"🐜 [Qumyrsqa Engine] справление интерфейса для : {iin}")
    profile = fetch_egov_profile(iin)
    
    # итаем с utf-8-sig на случай, если Windows опять добавит BOM
    with open(ATOM_PATH, 'r', encoding='utf-8-sig') as f:
        atom = json.load(f)
    
    html_content = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{atom['service_name']}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; padding: 40px; background: #eef2f7; }}
        .card {{ background: white; padding: 30px; border-radius: 12px; max-width: 500px; margin: auto; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }}
        .field {{ margin-bottom: 15px; }}
        label {{ font-weight: bold; display: block; margin-bottom: 5px; color: #444; }}
        input, select {{ width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }}
        .readonly {{ background: #f0f0f0; color: #777; pointer-events: none; }}
        button {{ background: #002f6c; color: white; padding: 15px; border: none; border-radius: 6px; width: 100%; cursor: pointer; font-weight: bold; margin-top: 10px; }}
        .badge {{ background: #d4edda; color: #155724; padding: 5px 10px; border-radius: 5px; font-size: 12px; margin-bottom: 20px; display: inline-block; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="card">
        <h2>{atom['service_name']}</h2>
        <div class="badge">✓ ерифицировано eGov IDP</div>
        <form id="leasingForm">
'''
    for key, data in atom['data_schema'].items():
        val = ""
        if data.get('source') == "egov_idp_mock":
            val = profile['name'] if "iin_bin" in key else profile['company_age_years']
        
        readonly = "readonly class='readonly'" if not data['editable'] else ""
        html_content += f"            <div class='field'><label>{{data['label']}}</label>"
        
        if data['type'] == 'enum':
            html_content += f"<select {{readonly}}>"
            for opt in data['options']: html_content += f"<option>{{opt}}</option>"
            html_content += "</select>"
        else:
            val_attr = f"value='{{val}}'" if val else f"value='{{data.get('default', '')}}'"
            html_content += f"<input type='text' {{val_attr}} {{readonly}}>"
        html_content += "</div>\\n"

    html_content += '''            <button type="button" onclick="alert('аявка отправлена в ой!')">тправить на рассмотрение</button>
        </form>
    </div>
</body>
</html>'''

    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Успех! нтерфейс сгенерирован без ошибок кодировки.")
    webbrowser.open('file://' + os.path.realpath(OUTPUT_HTML))

if __name__ == "__main__":
    build_ui("123456789012")
"""

with open('ui_prototype/renderer.py', 'w', encoding='utf-8') as f:
    f.write(renderer_script)

print("🐜 [Qumyrsqa Fixer] Файлы переписаны с чистой кодировкой.")
