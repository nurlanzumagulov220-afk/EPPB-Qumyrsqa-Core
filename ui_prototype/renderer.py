import json
import sys
import os
import webbrowser

# обавляем путь к стабам
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core_stubs')))
from egov_mock import fetch_egov_profile

ATOM_PATH = r"..\atoms_vault\leasing_v1.json"
OUTPUT_HTML = r"demo_leasing.html"

def build_ui(iin):
    print(f"🐜 [Qumyrsqa Engine] нициализация сессии для : {iin}")
    
    profile = fetch_egov_profile(iin)
    if "error" in profile:
        print("❌ шибка: ользователь не найден.")
        return

    # спользование utf-8-sig решает проблему BOM в Windows
    with open(ATOM_PATH, 'r', encoding='utf-8-sig') as f:
        atom = json.load(f)
    
    print(f"📦 [Vault] агружен том: {atom['service_name']} (v{atom['version']})")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>{atom['service_name']}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 40px; background: #eef2f7; color: #333; }}
            .card {{ background: white; padding: 35px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); max-width: 550px; margin: auto; border: 1px solid #d1d9e6; }}
            .field {{ margin-bottom: 18px; }}
            label {{ font-weight: 600; display: block; margin-bottom: 8px; font-size: 14px; color: #555; }}
            input, select {{ width: 100%; padding: 12px; border: 1px solid #ced4da; border-radius: 6px; box-sizing: border-box; transition: border-color .2s; }}
            input:focus {{ border-color: #0056b3; outline: none; }}
            .readonly {{ background: #f8f9fa; color: #6c757d; cursor: not-allowed; }}
            button {{ background: #002f6c; color: white; padding: 14px; border: none; border-radius: 6px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; margin-top: 10px; }}
            button:hover {{ background: #001f4d; }}
            .badge {{ display: inline-block; padding: 6px 12px; background: #d4edda; color: #155724; border-radius: 20px; font-size: 12px; margin-bottom: 25px; font-weight: bold; border: 1px solid #c3e6cb; }}
            h2 {{ margin-top: 0; color: #002f6c; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>{atom['service_name']}</h2>
            <div class="badge">✓ ерифицировано eGov IDP</div>
            <form>
    """

    for field_key, field_data in atom['data_schema'].items():
        label = field_data['label']
        is_readonly = not field_data['editable']
        
        value = ""
        if field_data.get('source') == "egov_idp_mock":
            if field_key == "applicant_iin_bin":
                value = f"{profile['name']} (: {iin})"
            elif field_key == "company_age_years":
                value = profile['company_age_years']

        readonly_attr = "readonly class='readonly'" if is_readonly else ""
        html_content += f"<div class='field'><label>{label}</label>"
        
        if field_data['type'] == 'enum':
            html_content += f"<select {readonly_attr}>"
            for opt in field_data['options']:
                html_content += f"<option value='{opt}'>{opt}</option>"
            html_content += "</select>"
        else:
            input_type = "number" if field_data['type'] == 'integer' else "text"
            html_content += f"<input type='{input_type}' value='{value}' {readonly_attr} />"
            
        html_content += "</div>"

    html_content += """
                <button type="button" onclick="alert('аявка принята! алидация выполнена на базе правил тома.')">тправить на рассмотрение</button>
            </form>
        </div>
    </body>
    </html>
    """

    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Успех! нтерфейс исправлен и сгенерирован.")
    webbrowser.open('file://' + os.path.realpath(OUTPUT_HTML))

if __name__ == "__main__":
    build_ui("123456789012")
