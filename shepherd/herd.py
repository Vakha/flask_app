from sys import argv

from shepherd import parser, product_calculator


if __name__ == "__main__":
    if len(argv) < 3:
        print('_' * 40)
        print('Please provide filename and day number, e.g.:\n'
              '`python shepherd/herd.py herd.xml 14`')
        print('_' * 40)
        exit(1)
    filename = argv[1]
    day = int(argv[2])
    herd = parser.get_herd_from_file(filename)
    res = product_calculator.print_production_report(herd, day)
    print(res)