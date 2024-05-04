import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

all_data = []


# foreach csv file in ./results2
for filename in os.listdir("./results"):
    # if file ends with stats.csv
    if filename.endswith("stats.csv"):
        # read the file
        df = pd.read_csv(f"./results/{filename}")
        last_row = df.tail(1)
        # show all columns
        pd.set_option('display.max_columns', None)
        title = filename.split(")")[0].split("(")[1] + " " + filename.split("-users")[0].split(")-")[1]

        # Type,Name,Request Count,Failure Count,Median Response Time,Average Response Time,Min Response Time,Max Response Time,Average Content Size,Requests/s,Failures/s,50%,66%,75%,80%,90%,95%,98%,99%,99.9%,99.99%,100%
        print("-----------------")
        all_data.append({
            "title": title,
            "qnt_users": filename.split(")-")[1].split("-users")[0],
            "average_response_time": last_row["Average Response Time"].values[0],
            "median_response_time": last_row["Median Response Time"].values[0],
            "min_response_time": last_row["Min Response Time"].values[0],
            "max_response_time": last_row["Max Response Time"].values[0],
            "percentile_50": last_row["50%"].values[0],
            "percentile_66": last_row["66%"].values[0],
            "percentile_75": last_row["75%"].values[0],
            "percentile_80": last_row["80%"].values[0],
            "percentile_90": last_row["90%"].values[0],
            "percentile_95": last_row["95%"].values[0],
            "percentile_98": last_row["98%"].values[0],
            "percentile_99": last_row["99%"].values[0],
            "percentile_999": last_row["99.9%"].values[0],
            "percentile_9999": last_row["99.99%"].values[0],
            "percentile_100": last_row["100%"].values[0],
        })
        print(title)
        print(last_row["Average Response Time"].values[0])
        print(last_row["90%"].values[0])
        print("-----------------")


# Convert collected data into a DataFrame
results_df = pd.DataFrame(all_data)


# create a function to format data for plotting
def format_data(data):
    # Create a new DataFrame with the desired columns
    return pd.DataFrame({
        "title": data["title"],
        "qnt_users": data["qnt_users"],
        "average_response_time": data["average_response_time"],
        "median_response_time": data["median_response_time"],
        "min_response_time": data["min_response_time"],
        "max_response_time": data["max_response_time"],
        "percentile_50": data["percentile_50"],
        "percentile_66": data["percentile_66"],
        "percentile_75": data["percentile_75"],
        "percentile_80": data["percentile_80"],
        "percentile_90": data["percentile_90"],
        "percentile_95": data["percentile_95"],
        "percentile_98": data["percentile_98"],
        "percentile_99": data["percentile_99"],
        "percentile_999": data["percentile_999"],
        "percentile_9999": data["percentile_9999"],
        "percentile_100": data["percentile_100"],
    })


rubyCache = format_data(results_df[results_df["title"].str.contains("ruby-cache")])
rubyNoCache = format_data(results_df[results_df["title"].str.contains("ruby-no-cache")])
pythonCache = format_data(results_df[results_df["title"].str.contains("python-cache")])
pythonNoCache = format_data(results_df[results_df["title"].str.contains("python-no-cache")])


sns.set_theme(style="whitegrid")
colors = ["#FF5733", "#5f72f8"]
colorsRed = ["#FF5733", "#FF5733"]
colorsGreen = ["#5f72f8", "#5f72f8"]



def plot_performance(dataFirst, dataSecond, x_col, y_col, labels, titles):
    print(dataSecond)
    """
    Parameters:
    - dataFirst: DataFrame containing the cached data.
    - dataSecond: DataFrame containing the non-cached data.
    - x_col: str, name of the column to be used as x-axis.
    - y_col: str, name of the column to be used as y-axis.
    - labels: dict, containing 'xlabel' and 'ylabel' for axis labels.
    - titles: dict, containing 'titleCache', 'titleNoCache', and 'titleComparison' for the plots.
    - colorsRed: color palette for the cached data plot.
    - colorsGreen: color palette for the non-cached data plot.
    - colors: list, colors for the comparison plot.
    """

    # Handle NaN values in the DataFrame
    dataFirst.fillna(0, inplace=True)
    dataSecond.fillna(0, inplace=True)

    # Create a single figure to hold all subplots
    plt.figure(figsize=(20, 6))

    # Plot for ruby cache
    plt.subplot(1, 3, 1)
    sns.barplot(data=dataFirst, x=x_col, y=y_col, palette=colorsRed)
    plt.title(titles['titleCache'])
    plt.xlabel(labels['xlabel'])
    plt.ylabel(labels['ylabel'])
    plt.ylim(0, dataFirst[y_col].max() + 10)
    sns.despine(left=True)

    # Plot for ruby no cache
    plt.subplot(1, 3, 2)
    sns.barplot(data=dataSecond, x=x_col, y=y_col, palette=colorsGreen)
    plt.title(titles['titleNoCache'])
    plt.xlabel(labels['xlabel'])
    plt.ylabel(labels['ylabel'])
    plt.ylim(0, dataSecond[y_col].max() + 10)
    sns.despine(left=True)

    # Combine the data with a new 'cache' column to distinguish groups
    combined_data = pd.concat([
        dataFirst.assign(cache=titles['titleFirst']),
        dataSecond.assign(cache=titles['titleSecond'])
    ])

    # Plot comparing ruby cache vs no cache
    plt.subplot(1, 3, 3)
    sns.barplot(data=combined_data, x=x_col, y=y_col, hue="cache", palette=colors)
    plt.title(titles['titleComparison'])
    plt.xlabel(labels['xlabel'])
    plt.ylabel(labels['ylabel'])
    plt.ylim(0, combined_data[y_col].max() + 10)
    sns.despine(left=True)

    # Show all plots
    plt.tight_layout()
    plt.show()



# All 3 metrics of Ruby Cache vs No Cache
# Compare the Average Response Time Ruby Cache vs No Cache
# titles = {'titleCache': "Ruby Cache", 'titleNoCache': "Ruby No Cache", 'titleComparison': "Ruby Cache vs No Cache", 'titleFirst': "Ruby Cache", 'titleSecond': "Ruby No Cache"}
# plot_performance(rubyCache, rubyNoCache, "qnt_users", "average_response_time", {'xlabel': "Number of Users", 'ylabel': "Average Response Time (ms)"}, titles)

# Compare the Median Response Time Ruby Cache vs No Cache
# titles = {'titleCache': "Ruby Cache", 'titleNoCache': "Ruby No Cache", 'titleComparison': "Ruby Cache vs No Cache", 'titleFirst': "Ruby Cache", 'titleSecond': "Ruby No Cache"}
# plot_performance(rubyCache, rubyNoCache, "qnt_users", "median_response_time", {'xlabel': "Number of Users", 'ylabel': "Median Response Time (ms)"}, titles)

# compare the percentile 90 Ruby Cache vs No Cache
# titles = {'titleCache': "Ruby Cache", 'titleNoCache': "Ruby No Cache", 'titleComparison': "Ruby Cache vs No Cache", 'titleFirst': "Ruby Cache", 'titleSecond': "Ruby No Cache"}
# plot_performance(rubyCache, rubyNoCache, "qnt_users", "percentile_90", {'xlabel': "Number of Users", 'ylabel': "Percentile 90 Response Time (ms)"}, titles)

# All 3 metrics of Python Cache vs No Cache
# Compare the Average Response Time Python Cache vs No Cache
# titles = {'titleCache': "Python Cache", 'titleNoCache': "Python No Cache", 'titleComparison': "Python Cache vs No Cache", 'titleFirst': "Python Cache", 'titleSecond': "Python No Cache"}
# plot_performance(pythonCache, pythonNoCache, "qnt_users", "average_response_time", {'xlabel': "Number of Users", 'ylabel': "Average Response Time (ms)"}, titles)

# Compare the Median Response Time Python Cache vs No Cache
# titles = {'titleCache': "Python Cache", 'titleNoCache': "Python No Cache", 'titleComparison': "Python Cache vs No Cache", 'titleFirst': "Python Cache", 'titleSecond': "Python No Cache"}
# plot_performance(pythonCache, pythonNoCache, "qnt_users", "median_response_time", {'xlabel': "Number of Users", 'ylabel': "Median Response Time (ms)"}, titles)

# compare the percentile 90 Python Cache vs No Cache
# titles = {'titleCache': "Python Cache", 'titleNoCache': "Python No Cache", 'titleComparison': "Python Cache vs No Cache", 'titleFirst': "Python Cache", 'titleSecond': "Python No Cache"}
# plot_performance(pythonCache, pythonNoCache, "qnt_users", "percentile_90", {'xlabel': "Number of Users", 'ylabel': "Percentile 90 Response Time (ms)"}, titles)

# All 3 metrics of Ruby Cache vs Python Cache
# Compare the Average Response Time Ruby Cache vs Python Cache
# titles = {'titleCache': "Ruby Cache", 'titleNoCache': "Python Cache", 'titleComparison': "Ruby Cache vs Python Cache", 'titleFirst': "Ruby Cache", 'titleSecond': "Python Cache"}
# plot_performance(rubyCache, pythonCache, "qnt_users", "average_response_time", {'xlabel': "Number of Users", 'ylabel': "Average Response Time (ms)"}, titles)

# Compare the Median Response Time Ruby Cache vs Python Cache
# titles = {'titleCache': "Ruby Cache", 'titleNoCache': "Python Cache", 'titleComparison': "Ruby Cache vs Python Cache", 'titleFirst': "Ruby Cache", 'titleSecond': "Python Cache"}
# plot_performance(rubyCache, pythonCache, "qnt_users", "median_response_time", {'xlabel': "Number of Users", 'ylabel': "Median Response Time (ms)"}, titles)

# compare the percentile 90 Ruby Cache vs Python Cache
# titles = {'titleCache': "Ruby Cache", 'titleNoCache': "Python Cache", 'titleComparison': "Ruby Cache vs Python Cache", 'titleFirst': "Ruby Cache", 'titleSecond': "Python Cache"}
# plot_performance(rubyCache, pythonCache, "qnt_users", "percentile_90", {'xlabel': "Number of Users", 'ylabel': "Percentile 90 Response Time (ms)"}, titles)

# All 3 metrics of Ruby No Cache vs Python No Cache
# Compare the Average Response Time Ruby No Cache vs Python No Cache
# titles = {'titleCache': "Ruby No Cache", 'titleNoCache': "Python No Cache", 'titleComparison': "Ruby No Cache vs Python No Cache", 'titleFirst': "Ruby No Cache", 'titleSecond': "Python No Cache"}
# plot_performance(rubyNoCache, pythonNoCache, "qnt_users", "average_response_time", {'xlabel': "Number of Users", 'ylabel': "Average Response Time (ms)"}, titles)