import src.binance.vars as vars

def fill_long_short(amount, price, isLong):
    closing_amount = 0
    avg_entry_price = vars.avg_entry_price

    if isLong:
        if vars.long >= 0 and vars.short <= 0:
            total_cost = avg_entry_price * vars.long + price * amount
            vars.long += amount
            vars.avg_entry_price = total_cost / vars.long if vars.long != 0 else price
        elif vars.short > 0:
            closing_amount = min(amount, vars.short)
            vars.short -= closing_amount
            remaining_amount = amount - closing_amount
            if remaining_amount > 0:
                vars.long = remaining_amount
                vars.avg_entry_price = price
    else:
        if vars.short >= 0 and vars.long <= 0:
            total_cost = avg_entry_price * vars.short + price * amount
            vars.short += amount
            vars.avg_entry_price = total_cost / vars.short if vars.short != 0 else price
        elif vars.long > 0:
            closing_amount = min(amount, vars.long)
            vars.long -= closing_amount
            remaining_amount = amount - closing_amount
            if remaining_amount > 0:
                vars.short = remaining_amount
                vars.avg_entry_price = price

    if closing_amount > 0:
        pnl = (avg_entry_price - price if isLong else price - avg_entry_price) * closing_amount
        vars.usd_balance += pnl

    return closing_amount