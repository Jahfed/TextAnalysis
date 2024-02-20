# loadingbar
def loader(x=True):
    l=0
    symbols = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
    if x:
        l = (l+1) % len(symbols)
        print(f'\n\033[K \033[92m {symbols[l]} loading and analyzing lyrics, please wait... \033[0m', end='', flush=True)

