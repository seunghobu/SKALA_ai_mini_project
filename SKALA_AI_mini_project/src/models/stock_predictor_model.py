import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Transformer 모델 정의
class TransformerModel(nn.Module):
    def __init__(self, input_dim, model_dim=64, num_heads=4, num_layers=2):
        super().__init__()
        self.embedding = nn.Linear(input_dim, model_dim)
        encoder_layer = nn.TransformerEncoderLayer(d_model=model_dim, nhead=num_heads, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.decoder = nn.Linear(model_dim, 1)

    def forward(self, src):
        embedded = self.embedding(src)
        output = self.transformer(embedded)
        return self.decoder(output)

# 데이터 전처리 및 학습 데이터 구성
def prepare_data(df: pd.DataFrame, window_size: int = 30):
    if "Close" not in df.columns:
        raise ValueError(f"데이터프레임에 'Close' 컬럼이 없습니다. 현재 컬럼: {df.columns.tolist()}")
    prices = df["Close"].values.reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(prices)

    x, y = [], []
    for i in range(len(scaled) - window_size):
        x.append(scaled[i:i+window_size])
        y.append(scaled[i+window_size])

    x = torch.tensor(x, dtype=torch.float32)  # shape: [samples, window_size, 1]
    y = torch.tensor(y, dtype=torch.float32)  # shape: [samples, 1]
    return x, y, scaler

# 예측 함수 (미래 30일)
def predict_future(model, last_sequence, steps=30):
    model.eval()
    preds = []
    seq = last_sequence.clone().detach()  # shape: [window_size, 1]
    for _ in range(steps):
        with torch.no_grad():
            inp = seq.unsqueeze(0)  # [1, window_size, 1]
            out = model(inp)  # [1, window_size, 1]
            pred = out[:, -1, 0]  # 마지막 time step 예측값
            preds.append(pred.item())
            # 슬라이딩 윈도우 업데이트
            seq = torch.cat([seq[1:], pred.unsqueeze(-1)], dim=0)
    return preds

# 전체 파이프라인: 모델 학습 및 예측
def transformer_forecast(df: pd.DataFrame, window_size: int = 30, epochs: int = 5):
    """
    Transformer 모델을 사용하여 주가를 예측합니다.

    Args:
        df (pd.DataFrame): 주가 데이터프레임
        window_size (int): 슬라이딩 윈도우 크기
        epochs (int): 학습 에폭 수

    Returns:
        np.ndarray: 예측된 주가 배열
    """
    x, y, scaler = prepare_data(df, window_size)
    model = TransformerModel(input_dim=1)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.MSELoss()

    for epoch in range(epochs):
        model.train()
        output = model(x)
        loss = criterion(output[:, -1, 0], y[:, 0])
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 학습 상태 출력
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item()}")

    # 예측 수행
    last_sequence = x[-1]  # [window_size, 1]
    predictions = predict_future(model, last_sequence)
    predictions = np.array(predictions).reshape(-1, 1)
    predicted_prices = scaler.inverse_transform(predictions).flatten()
    return predicted_prices  # shape: (30,)