import argparse
import sys

tank_to_fish = {
    "tank_a": "shark, tuna, herring",
    "tank_b": "cod, flounder",
}

##   enters invalid arguments, argparse will display an error message and exit the program
class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(f'Error: {message}')
        self.print_help()
        sys.exit(2)
parser = CustomArgumentParser(description='Divide two numbers.')




parser = argparse.ArgumentParser(description="Description of your program")
parser = argparse.ArgumentParser(
    description='Convert temperatures between Celsius and Fahrenheit.',
    epilog='Enjoy using the temperature converter!',
    usage='%(prog)s [options] temperature')
parser.add_argument("tank", type=str)

# parser.add_argument("directory", help='Path to the input file')
parser.add_argument("--number", type=int, help="an integer number")
parser.add_argument(
    "--upper-case",
    default=False,
    action="store_true",
    help="Upper case the outputted fish.",
)
parser.add_argument('--mode',
                    choices=['backup', 'restore', 'delete'],
                    required=True,
                    help='Mode of operation.'
                    )


# Create sub-parsers
subparsers = parser.add_subparsers(dest='operation', help='Available operations')
# Create a sub-parser for the 'add' operation
add_parser = subparsers.add_parser('add', help='Addition')
add_parser.add_argument('numbers', nargs='+', type=int,
                        help='Numbers to add')

# Create a sub-parser for the 'subtract' operation
subtract_parser = subparsers.add_parser('subtract', help='Subtraction')
subtract_parser.add_argument('numbers', nargs='+', type=int,
                             help='Numbers to subtract')



args = parser.parse_args()

# Process the selected operation

if args.operation == 'add':
    result = sum(args.numbers)
elif args.operation == 'subtract':
    result = args.numbers[0] - sum(args.numbers[1:])

print(result)

fish = tank_to_fish.get(args.tank, "")
print(fish)

if args.mode == 'backup':
    print('Backing up data...')
    # Backup code here
elif args.mode == 'restore':
    print('Restoring data...')
    # Restore code here
elif args.mode == 'delete':
    print('Deleting data...')
    # Delete code here