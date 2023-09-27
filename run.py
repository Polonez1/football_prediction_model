import argparse
import main
import req
import logging


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="get data visualisation by weeks name and time periods"
    )
    parser.add_argument(
        "--get_fixtures",
        action="store_true",
        help="see all comming matches",
    )

    parser.add_argument(
        "--predict",
        action="store_true",
        help="predict match",
    )

    parser.add_argument(
        "--predict_all",
        action="store_true",
        help="predict all matches",
    )

    # ------Args and actions----------#
    parser.add_argument("--match", type=str, help="match name from fixtures")

    args = parser.parse_args()

    if args.get_fixtures:
        req.show_fixtures()
    elif args.predict:
        matches = args.match
        json_data = req.get_fixtures_match(match_name=matches)
        pred = req.get_prediction(json_data=json_data)
        print(pred)
    elif args.predict_all:
        req.get_all_fixtures_prediction()

    else:
        print("Wrong command")

# python run.py --get_fixtures
