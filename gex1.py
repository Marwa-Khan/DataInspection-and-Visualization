import pandas as pd
import matplotlib.pyplot as plt

# Put all the logic in this class. Do not change the class name, as the test cases depend on it.
class DataInspection:
    # Initialize the DataFrame. Do not change this method.
    def __init__(self):
        self.df = None  

    
    def load_csv(self, file_path):
        """
        Put here the logic to a CSV file into a DataFrame.
        """
        self.df=pd.read_csv(file_path)
        print("Data loaded successfully.")
        print(self.df.head())
    
    def handle_missing_values(self, col):
        """
        Handle missing values by imputing or dropping columns with too many missing values.
        If more than 50% of values are missing in a column, drop the column.
        Otherwise, impute based on column type.
        """
        if self.df is None:
            print("No data loaded.")
            return
        
        for col in self.df.columns:
            print(f"the datatypes for {col} is:",self.df[col].dtypes)
            
            # get the missing val and calculate their percentage for imputing or dropping them
            missing_val = self.df[col].isnull().sum()
            print("missing val:",missing_val)
            total=len(self.df[col])
            print("total", total)
            missing_percentage= (missing_val/total)*100
            print(missing_percentage)
        
            if missing_percentage > 50:
                self.df.drop(columns=[col], inplace=True)
                print(f" Column '{col}' is dropped because it had more than 50% missing values.")
                print("updated dataframe",self.df)
                return False
            else:
            # Impute missing values based on column type
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    median_val = self.df[col].median()
                    self.df[col].fillna(median_val, inplace=True)
                else:
                    mode_series = self.df[col].mode()
                    mode_val = mode_series.iloc[0] if not mode_series.empty else None
                    self.df[col].fillna(mode_val, inplace=True)
                    # print(self.df['sex'])
                return True
                
        print(self.df)


    def check_data_types(self, col):
        """
        Check for incorrect data types and attempt to fix them.
        For example, convert numeric-looking strings to actual numeric types.
        """

        if self.df is None:
            print("No data loaded.")
            return
        # converting the column to numeric; if it fails, leave it as is.
        try:
            self.df[col] = pd.to_numeric(self.df[col], errors='ignore')
        except Exception as e:
            print(f"Conversion issue in column {col}: {e}")



    def classify_and_calculate(self, col):
        """
        Classifies the column's data type, calculates the central tendency like mean, median, and mode.
        """

        if self.df is None:
            print("No data loaded.")
            return
        
        
        # Step 1: Handle missing values
        if not self.handle_missing_values(col):
            # If the column is dropped, we stop processing.
            print(f"Column '{col}' dropped due to too many missing values.")
            return None

        # Step 2: Check and convert data types as needed
        self.check_data_types(col)

        # Step 3: Calculate total unique values in the column
        unique_count = self.df[col].nunique()

        # Step 4: Classify column based on its type and unique count
        if pd.api.types.is_numeric_dtype(self.df[col]):
            # For numeric columns, distinguish between ordinal and interval/ratio.
            if unique_count > 10:
                # Return mean for continuous numeric columns.
                result = self.df[col].mean()
                print(f"Column '{col}' classified as numeric interval/ratio with unique count {unique_count}. Mean: {result}")
                return result
            else:
                # Return median for ordinal numeric columns.
                result = self.df[col].median()
                print(f"Column '{col}' classified as numeric ordinal with unique count {unique_count}. Median: {result}")
                return result
        elif pd.api.types.is_object_dtype(self.df[col]):
            mode_series = self.df[col].mode()
            result = mode_series.iloc[0] if not mode_series.empty else None
            print(f"Column '{col}' classified as non-numeric. Mode: {result}")
            return result
        else:
            print(f"Column '{col}' could not be classified.")
            return None

    # Loop through each column in the DataFrame and apply classification and plotting
    def classify_columns(self):
        """Loop through each column in the DataFrame and apply classification and central tendency calculation functions."""

        if self.df is None:
            print("No data loaded.")
            return

        for col in self.df.columns:
            result = self.classify_and_calculate(col)
            # results[col]={"mean":mean, "median":median, "mode":mode}
        
        print(result)

    def ask_for_histogram(self):
        """
        Interactive histogram function that prompts the user to select a column to plot a histogram.
        """
        if self.df is None:
            print("No data loaded.")
            return
        
        print("\nAvailable columns:")
        print(self.df.columns.tolist())
        
        
        input_col=input("Enter the numeric dtype column to plot a histogram: ")
        # Plotting a basic histogram
        if input_col in self.df.columns and self.df[input_col].dtype in ['int64', 'float64']:
            self.df[input_col].hist(bins=30, edgecolor='black')
            plt.title(f"Histogram of {input_col} ")
            plt.xlabel(input_col)
            plt.ylabel("Frequency")
            plt.show()
        else:
            print("Invalid column or data type for histogram. Enter numeric type column")
    
    def ask_for_boxplot(self):
        
        """
        Interactive box plot function that prompts the user to select columns for the X and Y axes.
        The function then plots a box plot of the selected columns.
        """

        if self.df is None:
            print("No data loaded.")
            return
        
        print("\nAvailable columns:")
        print(self.df.columns.tolist())
        
        x_col=input("Enter the numeric dtype x-axis column for boxplot: ")
        y_col=input("Enter the numeric dtype y-axis column for boxplot: ")
        if self.df[y_col].dtype in ['int64', 'float64']:
            self.df.boxplot(column=y_col, by=x_col)
            plt.title(f"Box Plot of {y_col} by {x_col}")
            plt.suptitle("") 
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.show()
        else:
            print("Invalid column type for boxplot")
    

    def ask_for_barplot(self):
        
        """
        Interactive bar plot function that prompts the user to select a column to plot a bar plot.
        """

        if self.df is None:
            print("No data loaded.")
            return
        
        print("\nAvailable columns:")
        print(self.df.columns.tolist())
        
        col=input("Enter the categorical dtype column for barplot: ")
        print(self.df[col].dtype)
#         if pd.api.types.is_categorical_dtype(self.df[col]):
        if self.df[col].dtype == "object":
            count=self.df[col].value_counts()
            print(count)
#             self.df[col].value_counts().plot(kind="bar")
            plt.bar(count.index, count.values)
            plt.xlabel(col)
            plt.ylabel("count")
            plt.title(f"Bar plot of column {col} with its count")
            plt.show()
            
        else:
            print("Invalid column entered")

    def ask_for_scatterplot(self):
        """
        Interactive scatterplot function that prompts the user to select columns for the X and Y axes. 
        The function then plots a scatterplot of the selected columns.
        """
        
        if self.df is None:
            print("No data loaded.")
            return
        
        print("\nAvailable columns:")
        print(self.df.columns.tolist())
        x_col=input("Enter the numeric dtype x-axis column for scatterplot: ")
        y_col=input("Enter the numeric dtype y-axis column for scatterplot: ")
        if self.df[x_col].dtype in ['int64', 'float64'] and self.df[y_col].dtype in ['int64', 'float64']:
            plt.scatter(self.df[x_col],self.df[y_col])
            plt.title(f"Scatter plot between {x_col} and {y_col}")
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.show()
        else:
            print("Invalid dtypes columns entered")
        
# Main function
def main():
    
    """
    First create an object
    Then call the load_csv method
    Then call the classify_columns method
    Then call the ask_for_histogram method
    Then call the ask_for_boxplot method
    Then call the ask_for_barplot method
    Then call the ask_for_scatterplot method
    """

    data_inspector = DataInspection()
    data_inspector.load_csv("penguins.csv")
    data_inspector.classify_columns()
    data_inspector.ask_for_histogram()
    data_inspector.ask_for_boxplot()
    data_inspector.ask_for_barplot()
    data_inspector.ask_for_scatterplot()
    
# This is needed to run the main function when this script is run directly. Do not change this part. 
if __name__ == "__main__":
    main()
