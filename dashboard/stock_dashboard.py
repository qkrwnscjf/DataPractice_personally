import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# PostgreSQL 연결 설정
DB_CONFIG = {
    "dbname": "stock_db",
    "user": "user",
    "password": "password",
    "host": "localhost",
    "port": 5432
}

# DB에서 데이터 불러오는 함수
def load_data(symbol="AAPL"):
    conn = psycopg2.connect(**DB_CONFIG)
    query = f"""
    SELECT timestamp, symbol, close, volume 
    FROM stock_prices 
    WHERE symbol = '{symbol}'
    ORDER BY timestamp DESC
    LIMIT 100
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit UI
st.title("📈 실시간 주식 데이터 대시보드")

# 주식 종목 선택
symbol = st.selectbox("📌 종목 선택:", ["AAPL", "GOOGL", "TSLA", "MSFT"])

# 데이터 로드
df = load_data(symbol)

# 가격 변동 그래프
fig = px.line(df, x="timestamp", y="close", title=f"{symbol} 실시간 주가 변동")
st.plotly_chart(fig)

# 거래량 바 그래프
fig_vol = px.bar(df, x="timestamp", y="volume", title=f"{symbol} 거래량 변화")
st.plotly_chart(fig_vol)

# 데이터 테이블 출력
st.dataframe(df)
