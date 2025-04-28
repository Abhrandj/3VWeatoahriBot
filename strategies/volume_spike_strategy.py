def volume_spike_strategy(df):
  tags = []
  volume = df['volume'].iloc[-1]
  prev_volume = df['volume'].iloc[-5:-1].mean()
  rsi = df['rsi'].iloc[-1]

  if volume > prev_volume * 2:
      if df['close'].iloc[-1] > df['open'].iloc[-1] and rsi < 50:
          tags.append("VOL_SPIKE_BUY")
      elif df['close'].iloc[-1] < df['open'].iloc[-1] and rsi > 50:
          tags.append("VOL_SPIKE_SELL")
  return tags