
import argparse

import familysysadmin.familysysadmin

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
    args = parser.parse_args()

    fsa = familysysadmin.familysysadmin.FamilySysAdmin(verbose=args.verbose)
    fsa.run()