# MiniGain Backtest App

Este é um aplicativo de backtest completo e leve, criado para rodar localmente (via Pydroid 3) ou em nuvem (via Hugging Face Spaces).

## ✅ Funcionalidades

- Processamento de arquivos `.zip` com histórico de ticks
- Conversão automática para candles M1 (OHLCV)
- Cálculo manual do ATR (Average True Range)
- Execução da estratégia com regras fixas de entrada/saída
- Cálculo de métricas de performance
- Visualização do gráfico de equity
- Armazenamento dos resultados no Supabase

## 🚀 Como usar

### Localmente (Pydroid 3)
1. Instale dependências via terminal: `pip install -r requirements.txt`
2. Edite `supabase_client.py` com sua URL e chave Supabase
3. Execute: `python app.py`
4. Use um cliente como o Postman para enviar uma requisição `POST` para `http://127.0.0.1:8000/run_backtest`

### Online (Hugging Face Spaces)
1. Crie um novo Space usando Gradio como SDK
2. Faça upload de todos os arquivos do projeto
3. Adicione suas chaves Supabase nas variáveis de ambiente:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
4. O app será executado automaticamente com interface interativa.

---

## 📂 Estrutura

backtest-app/ ├── README.md ├── requirements.txt ├── app.py ├── supabase_client.py ├── backtest_engine/ │   ├── init.py │   ├── runner.py │   ├── indicators.py │   ├── simulator.py │   ├── metrics.py │   ├── chart.py │   └── utils.py └── interface.py

---

## 🛠️ Tecnologias
- Python 3.10+
- FastAPI + Uvicorn (modo local)
- Gradio (modo web)
- Supabase (armazenamento de resultados)

## 📌 Estratégia Implementada

- **Compra:** quando preço cruza para cima o Stop ATR(20, 1.5x) e ATR > 50
- **Venda:** quando preço cruza para baixo o Stop ATR(20, 1.5x) e ATR > 50
- **Saída:** no cruzamento oposto da linha do Stop ATR
- **Stop Dinâmico:** baseado em ATR atualizado a cada candle

---

## 📬 Contato
Desenvolvido por [addannss](https://huggingface.co/addannss)
