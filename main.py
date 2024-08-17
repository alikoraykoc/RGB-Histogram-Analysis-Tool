import pandas as pd
from pathlib import Path
from chardet import detect


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


output_name = []
output_mean = []
directory = "histogram_data"
files = Path(directory).glob('*')
mx_value = int(input("Please enter the maximum value that you want to include to mean calculation: "))
for file in files:
    if "/." in file.name or file.name[0] == ".":
        continue
    with open(file, "rb") as f:
        result = detect(f.read(10000))
        encoding = result["encoding"]
    df = pd.read_csv(file, delimiter="\t", encoding=encoding)
    try:
        mean = calculate_mean(df, mx_value)
    except KeyError:
        print(file.name)
    file = str(file)
    output_name.append(file[15:-4])
    output_mean.append(mean)

dictionary = {
    "individual": output_name,
    "color_mean": output_mean,
}
output_df = pd.DataFrame(dictionary)
output_df.sort_values(by="individual", inplace=True)
output_df.to_excel("results/output.xlsx")
print("Done! Note: Please move the output excel file to another directory before rerunning the script otherwise it may "
      "override the previous results.")
