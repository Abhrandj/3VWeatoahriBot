def ema_bb_strategy(df, ai_signal):
  tags = []
  current_price = df['close'].iloc[-1]
  ema20 = df['ema_20'].iloc[-1]
  ema50 = df['ema_50'].iloc[-1]
  ma200 = df['ma_200'].iloc[-1]
  rsi = df['rsi'].iloc[-1]
  lower_bb = df['lower_bb'].iloc[-1]
  upper_bb = df['upper_bb'].iloc[-1]

  if (
      current_price < lower_bb and
      ema20 > ema50 and
      df['close'].iloc[-2] < ema20 and df['close'].iloc[-1] > ema20 and
      current_price > ma200 and
      rsi < 50 and ai_signal == "BUY"
  ):
      tags.append("EMA_BB_BUY")
  elif (
      current_price > upper_bb and
      ema20 < ema50 and
      df['close'].iloc[-2] > ema20 and df['close'].iloc[-1] < ema20 and
      current_price < ma200 and
      rsi > 50 and ai_signal == "SELL"
  ):
      tags.append("EMA_BB_SELL")
  return tags