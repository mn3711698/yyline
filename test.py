
if __name__ == '__main__':
    enter_price = 4049.39
    short_win_price = 3988.649149
    print(enter_price * 0.985, short_win_price)
    short_trigger_price = 4016.99487
    print(enter_price * (1 - 0.008), short_trigger_price)
    short_loss_price = 4089.8839
    print(enter_price * (1 + 0.01), short_loss_price)
