import random 

MAX_LINES = 3
MAX_BET = 500
MIN_BET = 10

ROWS = 3
COLS = 5

symbol_count = {
    "A": 5,
    "B": 8,
    "C": 12,
    "D": 15
}

symbol_value = {
    "A": 10,
    "B": 8,
    "C": 6,
    "D": 4
}

bonus_prize = 100
jackpot_symbols = ["D", "D", "D", "D", "D"]

def check_winnings(columns, lines, bet, values):
    winnings = 0
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
    return winnings

def check_bonus_round():
    return random.randint(1, 10) == 1

def play_bonus_round():
    print("You have triggered the bonus round!")
    prize = random.randint(1, 10) * bonus_prize
    print(f"Congratulations! You have won ${prize}.")
    return prize

def check_jackpot(columns):
    for i in range(COLS - len(jackpot_symbols) + 1):
        if all([columns[i+j][0] == jackpot_symbols[j] for j in range(len(jackpot_symbols))]):
            return True
    return False

def play_jackpot():
    print("You have won the jackpot!")
    jackpot_prize = random.randint(10000, 100000)
    print(f"Congratulations! You have won ${jackpot_prize}.")
    return jackpot_prize

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        all_symbols += [symbol] * symbol_count
            
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
            
        columns.append(column)
        
    return columns

def print_slots_machine(columns):
    for row in range(len(columns[0])):
        for i,column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
                
        print()

def deposit():
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")
    return amount

def get_number_of_lines():
    while True:
        lines = input("Enter the number of lines to bet on (1-" + str(MAX_LINES) + "): ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Please enter a valid number of lines.")
        else:
            print("Please enter a number.")
    return lines

def get_bet(balance, lines):
    while True:
        bet = input(f"How much would you like to bet on each line (1-{MAX_BET})? ")
        if bet.isdigit():
            bet = int(bet)
            total_bet = bet * lines
            if bet < MIN_BET:
                print(f"The minimum bet is ${MIN_BET}.")
            elif total_bet > balance:
                print("You don't have enough balance for that bet.")
            else:
                return bet
        else:
            print("Please enter a valid number.")

def check_balance(balance, total_bet):
    return balance >= total_bet

def play_again():
    while True:
        response = input("Do you want to play again? (y/n): ")
        if response.lower() == "y":
            return True
        elif response.lower() == "n":
            return False
        else:
            print("Invalid input, please enter 'y' or 'n'")

def get_winning_lines(slots, lines):
    winning_lines = []
    for line in range(lines):
        symbol = slots[0][line]
        count = 1
        for col in range(1, COLS):
            if slots[col][line] == symbol:
                count += 1
            else:
                break
        if count == COLS:
            winning_amount = symbol_value[symbol] * bet
            winning_lines.append((line+1, winning_amount))
    return winning_lines

def print_winning_lines(winning_lines):
    if winning_lines:
        print("Congratulations! You won on the following lines:")
        for line, amount in winning_lines:
            print(f"Line {line}: ${amount}")
    else:
        print("Sorry, you didn't win on any lines.")

def update_balance(balance, total_winnings):
    balance += total_winnings
    return balance

  
balance = deposit()
while True:
        lines = get_number_of_lines()

        bet = get_bet(balance, lines)
        total_bet = bet * lines

        if not check_balance(balance, total_bet):
            print(f"You do not have enough to bet that amount, your current balance is: ${balance}")
            if not play_again():
                break
            continue

        slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
        print_slots_machine(slots)

        winning_lines = get_winning_lines(slots, lines)
        if winning_lines:
            print_winning_lines(winning_lines)
            total_winnings = sum([amount for line, amount in winning_lines])
            balance = update_balance(balance, total_winnings)
            print(f"You won ${total_winnings}. New balance is: ${balance}")
        else:
            print("Sorry, you did not win anything.")
            balance -= total_bet
            print(f"New balance is: ${balance}")

        if not play_again():
            break