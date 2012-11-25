from django.dispatch import Signal

partner_income_signal = Signal(providing_args=['user', 'amount', 'currency', 'description', 'period'])
partner_income_signal.__doc__ = """
Sent when new payment for an account is made in a system.
"""
