import numpy as np

def shrink(x, x_lower, x_upper):
    return max( min(x, x_upper), x_lower )

def cal_token0_token1(pool_type, L, price, **kwargs):
    left_price = kwargs['left_price'] if 'left_price' in kwargs.keys() else None
    right_price = kwargs['right_price'] if 'right_price' in kwargs.keys() else None

    if pool_type == 'V2':
        token0 = L /  np.sqrt(price)
        token1 = L * np.sqrt(price)
    elif pool_type == 'V3':
        token0 = L * (1.0/np.sqrt( shrink(price, left_price, right_price) ) - 1.0/np.sqrt(right_price))
        token1 = L * (np.sqrt( shrink(price, left_price, right_price) ) - np.sqrt(left_price))
    else:
        raise ValueError('PoolType Error.')

    return token0, token1

def cal_P_L(pool_type, token0, token1, **kwargs):
    # input: token0, token1
    # either is OK:
    #   left_price, right_price: float
    #   left_percent, right_percent: int, e.g. -30, 30
    # output: P (price of token0 in format of token1), L
    left_price = kwargs['left_price'] if 'left_price' in kwargs.keys() else None
    right_price = kwargs['right_price'] if 'right_price' in kwargs.keys() else None
    price = kwargs['price'] if 'price' in kwargs.keys() else None
    left_percent = kwargs['left_percent'] if 'left_percent' in kwargs.keys() else None
    right_percent = kwargs['right_percent'] if 'right_percent' in kwargs.keys() else None

    if pool_type == 'V2':
        P = token1 / token0
        L = np.sqrt( token0 * token1 )
    elif pool_type == 'V3':
        if left_price is not None and right_price is not None:
            a = token0
            b = token1 / np.sqrt(right_price) - token0 * np.sqrt(left_price)
            c = -token1

            sqrt_price = (-b + np.sqrt(b*b-4*a*c)) / a / 2
            P = sqrt_price * sqrt_price

            a = token0 * token1
            b = np.sqrt(left_price)*token0 + token1 / np.sqrt(right_price)
            c = np.sqrt(left_price / right_price) - 1

            L_1 = (-b + np.sqrt(b*b-4*a*c)) / a / 2
            L = 1.0 / L_1
        elif left_percent is not None and right_percent is not None:
            b = 1 - 1.0 / np.sqrt( 1 + right_percent / 100)
            a = 1 - np.sqrt( 1 + left_percent / 100)
            P = token1 * b / token0 / a

            L = token1 / np.sqrt(P) / a
        else:
            raise ValueError("Either 'left/right price' or 'left/right price percent' should be given.")
    else:
        raise ValueError('PoolType Error.')

    return P, L



# Uniswap V3 Find price
def log_base(base, p):
    return np.log(p) / np.log(base)

def find_bounder(price_0 = None, price_1 = None, precision_0 = 6, precision_1 = 18, tick_space = 60):
    # use price of token 0 (price_0) firstly
    # use price_1 only when price_0 is not given
    USE_PRICE_0 = True
    if price_0 is None:
        if price_1 is None:
            ValueError('No price is given.')
        else:
            USE_PRICE_0 = False
            price_0 =  1/price_1

    precision_multiplier = 10**(int(precision_1-precision_0))
    price = price_0 * precision_multiplier

    base = 1.0001
    log_p = log_base(base, price)
    i_lower = np.floor(log_p / tick_space) * tick_space
    i_upper = i_lower+tick_space
    p_lower = np.power(base, i_lower) / precision_multiplier
    p_upper = np.power(base, i_upper) / precision_multiplier

    if not USE_PRICE_0:
        tmp = 1 / p_upper
        p_upper = 1 / p_lower
        p_lower = tmp

    return (p_lower, p_upper)


if __name__ == '__main__':
    price_0 = 0.0054765388811177 * 1.4
        # 0.005337934895898792935177374148 * 1.4
    print('price_0:%.20f' % (price_0))
    (p_lower, p_upper) = find_bounder(price_0=price_0, precision_0=18, precision_1=18, tick_space=60)
    print('p_lower:%.10f, p_upper:%.10f' % (p_lower, p_upper))
    print('price_0 - p_lower:%.10f, p_upper - price_0:%.10f' % (price_0 - p_lower, p_upper-price_0))
    # (p_lower, p_upper) = find_bounder(price_1=1018)
    # print('p_lower:%f, p_upper:%f' % (p_lower, p_upper))