
import argparse

import familysysadmin.familysysadmin

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
    parser.add_argument("-t", "--test", action="store_true", help="test mode (sandbox)")
    parser.add_argument("-s", "--set", nargs=2, help="assign a value to a setting")
    args = parser.parse_args()

    fsa = familysysadmin.familysysadmin.FamilySysAdmin(test_mode=args.test, verbose=args.verbose)
    fsa.run()