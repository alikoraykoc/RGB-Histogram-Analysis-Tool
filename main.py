import pandas as pd
from pathlib import Path
from chardet import detect
import argparse
from os import mkdir, path


def remove_brights(data, max_value):
    data = data.drop(data[data["value"] > max_value].index)
    return data


def calculate_mean(dataframe, max_value):
    dataframe = remove_brights(dataframe, max_value)
    index = 0
    multiplied_value_ls = []
    counts = dataframe["count"].to_list()
    for value in counts:
        multiplied_value = value * index
        multiplied_value_ls.append(multiplied_value)
        index += 1
    sum_multiplies = sum(multiplied_value_ls)
    pixel_count = sum(counts)
    mean_value = sum_multiplies / pixel_count
    return mean_value


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="Input directory", type=str)
parser.add_argument("-o", "--output", required=False, help="Output directory", default="results", type=str)
parser.add_argument("-m", "--max-value", required=True, help="Maximum value that you want to include to the "
                                                             "calculations", type=int)
args = parser.parse_args()

if args.output == "results" and not path.exists("./results"):
    mkdir("./results")
    print("Results directory created at the working directory")

output_name = []
output_mean = []
directory = args.input
files = Path(directory).glob('*')
mx_value = args.max_value
for file in files:
    if "/." in file.name or file.name[0] == ".":
        continue
    with open(file, "rb") as f:
        result = detect(f.read(10000))
        encoding = result["encoding"]
    df = pd.read_csv(file, delimiter="\t", encoding=encoding)
    mean = calculate_mean(df, mx_value)
    file = str(file)
    output_name.append(file.split("/")[-1].split(".")[0])
    output_mean.append(mean)

dictionary = {
    "individual": output_name,
    "mean": output_mean,
}
output_df = pd.DataFrame(dictionary)
output_df.sort_values(by="individual", inplace=True)
output_directory = args.output
output_df.to_excel(f"{output_directory}/results.xlsx", index=False)
print("Done! Note: Please move the output excel file to another directory before rerunning the script otherwise it may "
      "override the previous results.")
