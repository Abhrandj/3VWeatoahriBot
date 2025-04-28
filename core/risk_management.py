class RiskManager:
    def __init__(self, max_risk_per_trade=0.02, account_balance=100):
        self.max_risk_per_trade = max_risk_per_trade
        self.account_balance = account_balance

    def calculate_position_size(self, stop_loss_distance):
        if stop_loss_distance <= 0:
            raise ValueError("Stop loss distance must be positive.")

        risk_amount = self.account_balance * self.max_risk_per_trade
        position_size = risk_amount / stop_loss_distance
        return round(position_size, 2)

    def update_account_balance(self, new_balance):
        self.account_balance = new_balance

    def calculate_stop_loss(self, current_price, sl_percentage=0.05):
        """
        Menghitung Stop Loss berdasarkan harga saat ini dan persentase.
        :param current_price: Harga saat ini
        :param sl_percentage: Persentase untuk Stop Loss (default 5%)
        :return: Harga Stop Loss
        """
        stop_loss_price = current_price * (1 - sl_percentage)
        return round(stop_loss_price, 2)

    def calculate_take_profit(self, current_price, tp_percentage=0.05):
        """
        Menghitung Take Profit berdasarkan harga saat ini dan persentase.
        :param current_price: Harga saat ini
        :param tp_percentage: Persentase untuk Take Profit (default 5%)
        :return: Harga Take Profit
        """
        take_profit_price = current_price * (1 + tp_percentage)
        return round(take_profit_price, 2)