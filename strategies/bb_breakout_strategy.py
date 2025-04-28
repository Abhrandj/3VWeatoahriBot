def bb_breakout_strategy(df):
  tags = []
  current_price = df['close'].iloc[-1]
  lower_bb = df['lower_bb'].iloc[-1]
  upper_bb = df['upper_bb'].iloc[-1]

  if current_price > upper_bb:
      tags.append("BB_BREAKOUT_UP")
  elif current_price < lower_bb:
      tags.append("BB_BREAKOUT_DOWN")
  return tags