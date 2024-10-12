
import numpy as np
import pandas as pd
from scipy.stats import chisquare
import matplotlib.pyplot as plt
import os

def analyze_lottery():
    # Step 1: Prompt user to enter the file path
    file_path = input("Please enter the path to your CSV file: ")

    # Modify the file path to correct format
    file_path = file_path.strip('"')  # Remove any leading/trailing quotes
    file_path = file_path.replace('\\', '\\\\')  # Replace single backslashes with double backslashes

    try:
        # Step 2: Load the CSV file with draw data (each row contains 1 draw with multiple numbers)
        data = pd.read_csv(file_path)

        # Step 3: Flatten the data into a single list (to count the occurrences of each number)
        all_numbers = data.values.flatten()

        # Step 4: Remove any NaN or empty values
        all_numbers = all_numbers[~np.isnan(all_numbers)]  # Removes NaN values

        # Step 5: Count the frequencies of each number (assumes numbers range from 1 to 42)
        observed_counts = np.zeros(42)  # Create an array for counting numbers from 1 to 42
        for number in all_numbers:
            if 1 <= number <= 42:
                observed_counts[number - 1] += 1  # Adjusting index (0-based index)

        # Step 6: Calculate the total number of draws and expected frequency
        total_numbers = np.sum(observed_counts)  # Ensure observed count total is correct
        expected_frequency = total_numbers / 42  # Uniform expected distribution across 42 numbers

        # Perform the chi-square test
        chi2_stat, p_value = chisquare(observed_counts, np.full(42, expected_frequency))

        # Calculate additional statistics
        std_dev = np.std(observed_counts)
        variance = np.var(observed_counts)

        # Directory for output
        output_directory = os.path.dirname(file_path)
        
        # Save the results to a text file in the same directory as the images
        output_txt_file = os.path.join(output_directory, 'lottery_analysis_output.txt')
        
        with open(output_txt_file, 'w') as f:
            f.write("Observed counts for each number (1 to 42):\n")
            f.write(np.array2string(observed_counts, separator=', ') + '\n\n')
            f.write(f"Total observed numbers: {total_numbers}\n")
            f.write(f"Expected frequency for each number: {expected_frequency:.2f}\n\n")
            f.write(f"Chi-square statistic: {chi2_stat:.4f}\n")
            f.write(f"p-value: {p_value:.6f}\n\n")
            f.write(f"Standard Deviation of observed counts: {std_dev:.4f}\n")
            f.write(f"Variance of observed counts: {variance:.4f}\n")
        
        print(f"Output saved to: {output_txt_file}")

        # Step 8: Plot the observed vs. expected frequencies
        plt.figure(figsize=(15, 8))  # Set figure size to a more manageable size
        numbers = np.arange(1, 43)  # Update range to 42 numbers
        plt.bar(numbers, observed_counts, alpha=0.6, label='Observed')
        plt.axhline(expected_frequency, color='red', linestyle='dashed', linewidth=2, label='Expected')
        plt.xlabel('Numbers')
        plt.ylabel('Frequency')
        plt.title('Observed vs. Expected Frequencies of Lottery Numbers')
        plt.legend()
        # Save the bar plot as an image
        bar_plot_file = os.path.join(output_directory, 'observed_vs_expected_frequencies.png')
        plt.savefig(bar_plot_file)
        plt.show()

        # Step 9: Plot frequency distribution (histogram) of observed counts
        plt.figure(figsize=(15, 8))  # Set figure size for the histogram
        plt.hist(observed_counts, bins=10, edgecolor='black', alpha=0.7)
        plt.title('Frequency Distribution of Observed Counts')
        plt.xlabel('Observed Counts')
        plt.ylabel('Frequency')
        # Save the histogram as an image
        histogram_file = os.path.join(output_directory, 'frequency_distribution_of_observed_counts.png')
        plt.savefig(histogram_file)
        plt.show()

        print(f"Bar plot saved to: {bar_plot_file}")
        print(f"Histogram saved to: {histogram_file}")

        # Check if any further statistics are necessary
        if p_value < 0.05:
            print("\nThe result is statistically significant. The numbers do not seem to follow a uniform distribution.")
        else:
            print("\nThe result is not statistically significant. The numbers seem to follow a uniform distribution.")

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found. Please check the path and try again.")

# Run the program
analyze_lottery()
