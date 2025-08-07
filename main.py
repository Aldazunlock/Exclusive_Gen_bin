#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
LIVE CARD GENERATOR v1.0
Original Script Modified for ExclusiveUnlock
"""

import getopt
import time
import os
import sys
import datetime
from random import randint

# Configuración
VERSION = "1.0"
MAX_LIMIT = 1000

class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner():
    clear_screen()
    print(Color.PURPLE + """
              ███████╗██╗  ██╗ ██████╗██╗   ██╗███████╗
              ██╔════╝╚██╗██╔╝██╔════╝██║   ██║██╔════╝
              █████╗   ╚███╔╝ ██║     ██║   ██║█████╗  
              ██╔══╝   ██╔██╗ ██║     ██║   ██║██╔══╝  
              ███████╗██╔╝ ██╗╚██████╗╚██████╔╝███████╗
              ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
    """ + Color.CYAN + """
              ████████╗███████╗ █████╗ ███╗   ███╗
              ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
                 ██║   █████╗  ███████║██╔████╔██║
                 ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║
                 ██║   ███████╗██║  ██║██║ ╚═╝ ██║
                 ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
    """ + Color.BLUE + f"""
              ╔══════════════════════════════════════╗
              ║  LIVE CARD GENERATOR v{VERSION}        ║
              ╚══════════════════════════════════════╝
    """ + Color.END)
    time.sleep(1)

def usage():
    print(Color.CYAN + """
╔════════════════════════════════════════════════╗
║               HOW TO USE                       ║
╠════════════════════════════════════════════════╣
║                                                ║
║  python2 LiveGen.py -b [BIN] -u [AMOUNT]       ║
║                [-c] [-d] [-s]                  ║
║                                                ║
╠════════════════════════════════════════════════╣
║                OPTIONS                         ║
╠════════════════════════════════════════════════╣
║ -b, --bin       : BIN format (16 digits)       ║
║ -u, --amount    : Amount to generate (1-1000)  ║
║ -c, --ccv       : Generate random CCV          ║
║ -d, --date      : Generate expiration date     ║
║ -s, --save      : Save to file                 ║
║ -h, --help      : Show this help               ║
║                                                ║
╠════════════════════════════════════════════════╣
║                EXAMPLE                         ║
╠════════════════════════════════════════════════╣
║ python2 LiveGen.py -b 543210xxxxxxxxxx         ║
║ -u 50 -c -d -s                                 ║
║                                                ║
╚════════════════════════════════════════════════╝
""" + Color.END)

def validate_bin(bin_format):
    if len(bin_format) != 16:
        raise ValueError("BIN must be 16 digits")
    if not all(c in '0123456789xX' for c in bin_format):
        raise ValueError("BIN can only contain digits and x/X")

def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    
    return checksum % 10 == 0

def generate_card(bin_format):
    while True:
        temp_cc = []
        for c in bin_format:
            if c.lower() == 'x':
                temp_cc.append(str(randint(0, 9)))
            else:
                temp_cc.append(c)
        
        cc_number = ''.join(temp_cc)
        if luhn_checksum(cc_number):
            return cc_number

def generate_ccv():
    return f"{randint(0, 999):03d}"

def generate_exp_date():
    now = datetime.datetime.now()
    month = randint(1, 12)
    year = now.year + randint(1, 5)
    return f"{month:02d}|{year % 100:02d}"

def save_cards(cards):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_cards_{timestamp}.txt"
    with open(filename, 'w') as f:
        f.write("\n".join(cards))
    return filename

def main():
    try:
        show_banner()
        
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hb:u:cds", 
                                     ["help", "bin=", "amount=", "ccv", "date", "save"])
        except getopt.GetoptError:
            usage()
            sys.exit(2)
        
        bin_format = ""
        amount = 10
        gen_ccv = False
        gen_date = False
        save_file = False
        
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                usage()
                sys.exit()
            elif opt in ('-b', '--bin'):
                bin_format = arg.strip()
            elif opt in ('-u', '--amount'):
                try:
                    amount = int(arg)
                    if not 1 <= amount <= MAX_LIMIT:
                        print(Color.RED + f"Amount must be between 1-{MAX_LIMIT}" + Color.END)
                        sys.exit(1)
                except ValueError:
                    print(Color.RED + "Invalid amount number" + Color.END)
                    sys.exit(1)
            elif opt in ('-c', '--ccv'):
                gen_ccv = True
            elif opt in ('-d', '--date'):
                gen_date = True
            elif opt in ('-s', '--save'):
                save_file = True
        
        if not bin_format:
            print(Color.RED + "You must specify a BIN" + Color.END)
            usage()
            sys.exit(1)
        
        validate_bin(bin_format)
        
        print(Color.GREEN + f"\nGenerating {amount} cards with BIN: {bin_format[:6]}xxxxxx" + Color.END)
        
        generated = []
        for _ in range(amount):
            card = generate_card(bin_format)
            
            if gen_ccv:
                card += f"|{generate_ccv()}"
            if gen_date:
                card += f"|{generate_exp_date()}"
            
            generated.append(card)
            print(Color.BLUE + "[+] " + Color.END + card)
        
        print(Color.GREEN + f"\nSuccessfully generated {amount} valid cards" + Color.END)
        
        if save_file:
            filename = save_cards(generated)
            print(Color.GREEN + f"Saved to: {filename}" + Color.END)
        
        print(Color.YELLOW + "\nUse responsibly. For educational purposes only." + Color.END)
    
    except Exception as e:
        print(Color.RED + f"\nError: {str(e)}" + Color.END)
        sys.exit(1)

if __name__ == '__main__':
    main()
