import os
import pandas as pd


class Olist:
    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'sellers', 'orders', 'order_items' etc...
        Its values should be pandas.DataFrames loaded from csv files
        """
        # Hints 1: Build csv_path as "absolute path" in order to call this method from anywhere.
            # Do not hardcode your path as it only works on your machine ('Users/username/code...')
            # Use __file__ instead as an absolute path anchor independant of your usename
            # Make extensive use of `breakpoint()` to investigate what `__file__` variable is really
        # Hint 2: Use os.path library to construct path independent of Mac vs. Unix vs. Windows specificities
        csv_path='/home/alanoud/code/Alanoudniaf/04-Decision-Science/01-Project-Setup/data-context-and-setup/data/csv'

        patt_data = os.path.dirname(os.path.dirname(__file__))
        file_name= os.path.join(csv_path, "csv" ,"data.csv")


        pd.read_csv(os.path.join(csv_path, 'olist_sellers_dataset.csv')).head()
        file_names = [file for file in os.listdir('/home/alanoud/code/Alanoudniaf/04-Decision-Science/01-Project-Setup/data-context-and-setup/data/csv') if file.endswith('.csv')]


        key_names=[]
        for file in file_names:
          file=file.replace(".csv","")
          file=file.replace("_dataset","")
          file=file.replace("olist_","")
          key_names.append(file)
        data={}
        for key,file_name in zip (key_names,file_names):
           df = pd.read_csv(os.path.join(csv_path,file_name))
           data[key] = df
        return data







    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")
