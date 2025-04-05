import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()



    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """
        # Hint: Within this instance method, you have access to the instance of the class Order in the variable self, as well as all its attributes
        orders = self.data['orders']
        if is_delivered:
            orders = orders[orders['order_status'] == 'delivered']

        #orders['wait_time'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.total_seconds() / 86400
        #orders['expected_wait_time'] = (orders['order_estimated_delivery_date'] - orders['order_purchase_timestamp']).dt.total_seconds() / 86400

        #orders['delay_vs_expected'] = (orders['wait_time'] - orders['expected_wait_time']).clip(lower=0)
        #group_order= orders[['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']]
        #return group_order

        orders = self.data['orders'].copy()

        if is_delivered:
         orders = orders[orders['order_status'] == 'delivered']

        date_cols = ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']
        for col in date_cols:
         orders[col] = pd.to_datetime(orders[col], errors='coerce')


        orders['wait_time'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.total_seconds() / 86400
        orders['expected_wait_time'] = (orders['order_estimated_delivery_date'] - orders['order_purchase_timestamp']).dt.total_seconds() / 86400

        orders['delay_vs_expected'] = (orders['wait_time'] - orders['expected_wait_time']).clip(lower=0)

        group_order = orders[['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']]

        return group_order




    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        reviews = self.data['order_reviews']

        return reviews[['order_id', 'review_score']].assign(dim_is_five_star=(reviews['review_score'] == 5).astype(int),dim_is_one_star=(reviews['review_score'] == 1).astype(int))

    def get_number_items(self):
        """
        Returns a DataFrame with:
        order_id, number_of_items
        """
        order_items = self.data['order_items']
        number_items = order_items.groupby('order_id').size().reset_index(name='number_of_items')
        return number_items


    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        ""
        order_items = self.data['order_items']
        number_sellers = order_items.groupby('order_id')['seller_id'].nunique().reset_index(name='number_of_sellers')

        return number_sellers



    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        order_items = self.data['order_items']
        price_freight = order_items.groupby('order_id', as_index=False).agg({
        'price': 'sum',
        'freight_value': 'sum'
    })

        return price_freight



    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        pass  # YOUR CODE HERE

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_items', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        training_set = self.get_wait_time()\
            .merge(self.get_review_score(), on='order_id', how='left')\
            .merge(self.get_number_items(), on='order_id', how='left')\
            .merge(self.get_number_sellers(), on='order_id', how='left')\
            .merge(self.get_price_and_freight(), on='order_id', how='left')

        return training_set.dropna()[[
            'order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status',
            'dim_is_five_star', 'dim_is_one_star', 'review_score', 'number_of_items',
            'number_of_sellers', 'price', 'freight_value'
        ]]
