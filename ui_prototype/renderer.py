import json
import sys
import os
import webbrowser

# Абсолютные пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ATOM_PATH = os.path.join(BASE_DIR, '..', 'atoms_vault', 'leasing_v1.json')
STUBS_PATH = os.path.join(BASE_DIR, '..', 'core_stubs')
OUTPUT_HTML = os.path.join(BASE_DIR, 'demo_leasing.html')

sys.path.append(STUBS_PATH)
from egov_mock import fetch_egov_profile

def build_ui(iin):
    print(f"🐜 [Qumyrsqa Engine] Инициализация сборки для ИИН: {iin}")
    profile = fetch_egov_profile(iin)
    
    # Читаем Атом с защитой от BOM
    with open(ATOM_PATH, 'r', encoding='utf-8-sig') as f:
        atom = json.load(f)
    
    # Собираем HTML по частям, чтобы избежать конфликта скобок
    html_parts = []
    html_parts.append(f"""<!DOCTYPE html>
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
        <div class="badge">✓ Верифицировано eGov IDP</div>
        <form id="leasingForm">
""")

    # Динамическая генерация полей из Атома
    for key, data in atom['data_schema'].items():
        val = ""
        if data.get('source') == "egov_idp_mock":
            val = profile['name'] if "iin_bin" in key else profile['company_age_years']
        
        readonly = "readonly class='readonly'" if not data['editable'] else ""
        html_parts.append(f"            <div class='field'><label>{data['label']}</label>\n")
        
        if data['type'] == 'enum':
            html_parts.append(f"            <select {readonly}>\n")
            for opt in data['options']: 
                html_parts.append(f"                <option>{opt}</option>\n")
            html_parts.append("            </select>\n")
        else:
            val_attr = f"value='{val}'" if val else f"value='{data.get('default', '')}'"
            html_parts.append(f"            <input type='text' {val_attr} {readonly}>\n")
        html_parts.append("            </div>\n")

    # Добавляем скрипт калькулятора
    html_parts.append("""            <button type="button" onclick="calculate()">Отправить на рассмотрение</button>
        </form>
    </div>
    <script>
        function calculate() {
            const count = document.querySelectorAll('input[type=text]')[1].value;
            const term = document.querySelectorAll('input[type=text]')[2].value;
            const rate = document.querySelectorAll('input[type=text]')[3].value;
            
            const p = 15000000 * count; 
            const r = (rate / 100) / 12;
            const n = term;
            const payment = Math.round(p * (r * Math.pow(1+r, n)) / (Math.pow(1+r, n) - 1));
            
            alert('Предварительный аннуитетный платеж: ' + payment.toLocaleString('ru-RU') + ' ₸/мес. Заявка отправлена в обработку!');
        }
    </script>
</body>
</html>""")

    html_content = "".join(html_parts)

    # Принудительная запись в чистом UTF-8
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Успех! Интерфейс собран из Атомов. Кодировка 100% чистая.")
    webbrowser.open('file://' + os.path.realpath(OUTPUT_HTML))

if __name__ == "__main__":
    build_ui("123456789012")