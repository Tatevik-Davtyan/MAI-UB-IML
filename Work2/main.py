import argparse
import pathlib

from parser import get_data
from kNN import kNN, DistanceType


curr_dir = pathlib.Path(__file__).parent

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "-d", "--dataset",
        type=str,
        default="adult",
        help="Name of the dataset to process, adult on default."
    )
    parser.add_argument(
        "-p", "--path",
        type=pathlib.Path,
        default=curr_dir / "datasets",
        help="Path to the data directory."
    )
    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=10,
        help="Limit to how many datasets to load"
    )
    
    # Parse the command line arguments
    args = parser.parse_args()

    data_dir = args.path / args.dataset
    if not data_dir.is_dir():
        raise argparse.ArgumentTypeError(f"The dataset directory {data_dir} could not be found.")
    
    training_fns = []
    testing_fns = []
    for fn in data_dir.iterdir():
        if not fn.is_file():
            continue
        if int(fn.suffixes[1][1:]) > args.limit:
            break
        if '.train' in fn.suffixes:
            training_fns.append(fn)
        elif '.test' in fn.suffixes:
            testing_fns.append(fn)

    train_input, train_output, test_input, test_output = get_data(training_fns, testing_fns)

    knn = kNN(k=1, distance_metric=DistanceType.EUCLIDEAN)
    knn.fit(train_input[0], train_output[0])
    predictions = knn.predict(test_input[0])

    # TODO: compare predictions to test_output


if __name__ == "__main__":
    main()