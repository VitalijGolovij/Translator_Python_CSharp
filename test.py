from statemachine import StateMachine, State

class OrderControl(StateMachine):
    waiting_for_payment = State("Waiting for payment", initial=True)#состояние 1
    processing = State("Processing")
    shipping = State("Shipping")
    completed = State("Completed", final=True)

    add_to_order = waiting_for_payment.to(waiting_for_payment)
    receive_payment = (
        waiting_for_payment.to(processing, cond="payments_enough")
        | waiting_for_payment.to(waiting_for_payment, unless="payments_enough")
    )
    process_order = processing.to(shipping, cond="payment_received")
    ship_order = shipping.to(completed)

    def __init__(self):
        self.order_total = 0
        self.payments = []
        self.payment_received = False
        super(OrderControl, self).__init__()

    def payments_enough(self, amount):
        return sum(self.payments) + amount >= self.order_total

    def before_add_to_order(self, amount):
        self.order_total += amount
        return self.order_total

    def before_receive_payment(self, amount):
        self.payments.append(amount)
        return self.payments

    def after_receive_payment(self):
        self.payment_received = True

    def on_enter_waiting_for_payment(self):
        self.payment_received = False

control = OrderControl()

control.add_to_order(5)
control.receive_payment(3)
print(control)