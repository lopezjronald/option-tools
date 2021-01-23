from django.shortcuts import render


def calculator_entry(request):
    return render(request, 'calculator-entry.html', {})


def calculate_margin(request):
    multiplier = 100
    quantity = int(request.POST['quantity'])
    margin = float(request.POST['margin'])
    stock_price = float(request.POST['stock-price'])
    option_price = float(request.POST['option-price'])
    strike_price = float(request.POST['strike-price'])
    option_type = request.POST['option-type']
    option_description = request.POST['option-description']
    open_interest = int(request.POST['open-interest'])
    option_bid = request.POST['option-bid']
    option_ask = request.POST['option-ask']
    option_volume = request.POST['option-volume']
    option_change = request.POST['option-change']
    option_mid_iv = request.POST['option-mid-iv']
    option_delta = request.POST['option-delta']
    option_gamma = request.POST['option-gamma']
    option_theta = request.POST['option-theta']
    option_vega = request.POST['option-vega']
    option_rho = request.POST['option-rho']

    stock_description = request.POST['option-description']
    stock_bid = request.POST['stock-bid']
    stock_ask = request.POST['stock-ask']
    stock_volume = request.POST['stock-volume']
    stock_change = request.POST['stock-change']

    option_trade = 'Out of the Money'
    margin_call_a = ''
    margin_call_b = ''
    margin_call_c = ''
    # determining whether it's a Call or Put & In the Money or Out of the Money
    if option_type == 'C':
        option_type = "Call"
        if strike_price < stock_price:
            option_trade = 'In The Money'
            margin_call = multiplier * quantity * stock_price * margin
        else:
            margin_call_a = ((stock_price * margin) - stock_price) * quantity * multiplier
            margin_call_b = ((stock_price * 0.10) + option_price) * quantity * multiplier
            margin_call_c = 50.0 + option_price
            margin_call = max(margin_call_a, margin_call_b, margin_call_c)

    else:
        option_type = "Put"
        if strike_price > stock_price:
            option_trade = 'In The Money'
            margin_call = multiplier * quantity * stock_price * margin
        else:
            margin_call_a = ((stock_price * margin) - stock_price) * quantity * multiplier
            margin_call_b = ((strike_price * 0.10) + option_price) * quantity * multiplier
            margin_call_c = 50.0 + option_price
            margin_call = max(margin_call_a, margin_call_b, margin_call_c)

    proceeds = multiplier * quantity * option_price
    margin_requirements = margin_call + proceeds

    return render(request, 'results.html', {'option_trade': option_trade,
                                            'margin_call': margin_call,
                                            'proceeds': proceeds,
                                            'margin_requirements': margin_requirements,
                                            'quantity': quantity,
                                            'margin': margin,
                                            'stock_price': stock_price,
                                            'option_price': option_price,
                                            'strike_price': strike_price,
                                            'open_interest': open_interest,
                                            'option_type': option_type,
                                            'margin_call_a': margin_call_a,
                                            'margin_call_b': margin_call_b,
                                            'margin_call_c': margin_call_c,
                                            'option_description': option_description,
                                            'option_bid': option_bid,
                                            'option_ask': option_ask,
                                            'option_volume': option_volume,
                                            'option_change': option_change,
                                            'option_mid_iv': option_mid_iv,
                                            'option_delta': option_delta,
                                            'option_gamma': option_gamma,
                                            'option_theta': option_theta,
                                            'option_vega': option_vega,
                                            'option_rho': option_rho,
                                            'stock_description': stock_description,
                                            'stock_bid': stock_bid,
                                            'stock_ask': stock_ask,
                                            'stock_volume': stock_volume,
                                            'stock_change': stock_change})


def options(request):
    if request.method == 'POST':
        import requests
        option = request.POST['option']
        option_copy = option[:]
        parsed_option_copy = option_copy.split("=")[1].split(".")[0].split(" ")
        underlying = parsed_option_copy[0].upper()
        date_type_price = parsed_option_copy[1].split(".")[0]
        if "C" in date_type_price:
            option_type_index = date_type_price.find("C")
        elif "c" in date_type_price:
            option_type_index = date_type_price.find("c")
        elif "P" in date_type_price:
            option_type_index = date_type_price.find("P")
        elif "p" in date_type_price:
            option_type_index = date_type_price.find("p")
        option_type = date_type_price[option_type_index].upper()
        option_strike_price = int(date_type_price[option_type_index + 1:])
        option_strike_price = str(f"{option_strike_price:08d}")
        option_expiration_date = date_type_price[:option_type_index]
        parsed_option_copy = underlying + option_expiration_date + option_type + option_strike_price
        quote_request = requests.get('https://api.tradier.com/v1/markets/quotes',
                                     params={'symbols': f'{underlying},{parsed_option_copy}', 'greeks': 'true'},
                                     headers={'Authorization': 'Bearer FSZnAyUIm4sW21bRstkOAXqXxeeu',
                                              'Accept': 'application/json'})
        print(quote_request)
        quote = quote_request.json()

        return render(request, 'options.html', {'option': option,
                                                'extra': parsed_option_copy,
                                                'quote': quote,
                                                'underlying': underlying,
                                                'option_type': option_type}, )
    else:
        return render(request, 'options.html', {})
