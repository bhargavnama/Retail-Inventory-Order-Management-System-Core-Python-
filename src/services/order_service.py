from src.dao.order_dao import Order

class OrderError(Exception):
    pass

class Order_service:
    
    def __init__(self):
        self.order = Order()
        
    def place_order(self, cust_id: int, items: list[str]):
        