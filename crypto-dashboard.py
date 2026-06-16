"""
Crypto Dashboard - Muestra precios en tiempo real usando CoinGecko API.
No necesita API key.

Endpoint principal:
    GET / -> Dashboard HTML con las principales criptomonedas
    GET /api/crypto -> Datos en JSON
"""

from flask import Flask
import requests

app = Flask(__name__)

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"

CRYPTOS = [
    "bitcoin", "ethereum", "solana", "cardano", "dogecoin",
    "ripple", "polkadot", "litecoin", "chainlink", "avalanche-2"
]


def obtener_datos():
    """Obtiene datos de las principales criptos desde CoinGecko."""
    params = {
        "vs_currency": "usd",
        "ids": ",".join(CRYPTOS),
        "order": "market_cap_desc",
        "sparkline": False,
        "price_change_percentage": "24h"
    }
    resp = requests.get(COINGECKO_URL, params=params)
    resp.raise_for_status()
    return resp.json()


def generar_fila(crypto):
    """Genera una fila HTML para una criptomoneda."""
    cambio = crypto.get("price_change_percentage_24h") or 0
    color = "#2ecc71" if cambio >= 0 else "#e74c3c"
    flecha = "▲" if cambio >= 0 else "▼"
    precio = f"${crypto['current_price']:,.2f}"
    cap = f"${crypto['market_cap']:,.0f}"

    return f"""
    <tr>
        <td class="nombre">
            <img src="{crypto['image']}" width="24" height="24" style="vertical-align:middle; margin-right:8px;">
            {crypto['name']} <span class="symbol">{crypto['symbol'].upper()}</span>
        </td>
        <td class="precio">{precio}</td>
        <td style="color:{color}; font-weight:bold;">{flecha} {cambio:.2f}%</td>
        <td class="cap">{cap}</td>
        <td class="rank">#{crypto['market_cap_rank']}</td>
    </tr>
    """


def generar_html(datos):
    """Genera el dashboard HTML completo."""
    filas = "".join(generar_fila(c) for c in datos)

    return f"""
    <html>
    <head>
        <title>Crypto Dashboard</title>
        <meta charset="utf-8">
        <meta http-equiv="refresh" content="60">
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: #0d1117;
                color: #e6edf3;
                padding: 30px;
            }}
            h1 {{
                text-align: center;
                font-size: 2em;
                margin-bottom: 10px;
                color: #f0b90b;
            }}
            .subtitle {{
                text-align: center;
                color: #8b949e;
                margin-bottom: 30px;
                font-size: 0.9em;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: #161b22;
                border-radius: 12px;
                overflow: hidden;
            }}
            th {{
                background: #21262d;
                padding: 14px 16px;
                text-align: left;
                color: #8b949e;
                font-size: 0.85em;
                text-transform: uppercase;
            }}
            td {{
                padding: 14px 16px;
                border-bottom: 1px solid #21262d;
                font-size: 0.95em;
            }}
            tr:last-child td {{ border-bottom: none; }}
            tr:hover {{ background: #1c2128; }}
            .nombre {{ font-weight: bold; }}
            .symbol {{ color: #8b949e; font-size: 0.85em; margin-left: 4px; }}
            .precio {{ font-weight: bold; color: #f0b90b; }}
            .cap {{ color: #8b949e; }}
            .rank {{ color: #8b949e; text-align: center; }}
            .update {{ text-align:center; color:#8b949e; margin-top:16px; font-size:0.8em; }}
        </style>
    </head>
    <body>
        <h1>🚀 Crypto Dashboard</h1>
        <p class="subtitle">Precios en tiempo real · Se actualiza cada 60 segundos</p>
        <table>
            <tr>
                <th>Nombre</th>
                <th>Precio (USD)</th>
                <th>Cambio 24h</th>
                <th>Cap. de mercado</th>
                <th>Rank</th>
            </tr>
            {filas}
        </table>
        <p class="update">Datos proporcionados por CoinGecko API</p>
    </body>
    </html>
    """


@app.route("/")
def dashboard():
    try:
        datos = obtener_datos()
        return generar_html(datos)
    except Exception as e:
        return f"<h2>Error obteniendo datos: {e}</h2>", 500


@app.route("/api/crypto")
def api_crypto():
    try:
        datos = obtener_datos()
        return {"cryptos": datos}
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)