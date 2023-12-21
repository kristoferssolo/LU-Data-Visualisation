import matplotlib.pyplot as plt

from data.read import base_path, read_file


# function that visualizes the data in the form of a bar chart
def visualize():
    # read the data from the file
    path = base_path().joinpath("data", "vejaAtrumsFaktiskais.xlsx")
    data = read_file(path)
    # create a list of the years
    years = [year for year in data.keys()]
    # create a list of the number of movies per year
    num_movies = [len(data[year]) for year in data.keys()]
    # create a bar chart
    plt.bar(years, num_movies)
    # set the title of the bar chart
    plt.title("Number of Movies per Year")
    # set the x-axis label
    plt.xlabel("Year")
    # set the y-axis label
    plt.ylabel("Number of Movies")
    # show the bar chart
    plt.show()
