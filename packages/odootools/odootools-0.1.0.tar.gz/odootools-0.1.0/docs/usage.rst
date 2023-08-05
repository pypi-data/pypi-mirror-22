=====
Usage
=====

To use Python Package for Odoo in a addons::

    from odootools import odootools

    contracts = self.env['hr.contract'].search([])
    for contract in contracts:
        date_start = Date(contract.date_start)
        # print the next day in the contract
        print date_start.next_day().value
        # print the last day in the month of the date_start
        print Date(contract.date_start).last_day_in_month().value
