import ast
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from CateringApp.models import Order, Product_Master, Review

# def get_recommendations(user_id, ratings_matrix, item_similarity_matrix, top_n=5):
#     if user_id not in ratings_matrix.index:
#         print(user_id, "This is my userid.")
#         return []  # Return an empty list if user_id is not in the ratings_matrix index

#     user_ratings = ratings_matrix.loc[user_id]
#     user_unrated_items = user_ratings[user_ratings == 0].index

#     item_scores = []
#     for item_id in user_unrated_items:
#         item_similarity_scores = item_similarity_matrix[item_id]
#         item_rating_scores = ratings_matrix.loc[:, item_id]

#         weighted_ratings = 0
#         total_similarity = 0
#         for i, similarity_score in enumerate(item_similarity_scores):
#             if i < len(item_rating_scores):
#                 rating = item_rating_scores.iloc[i]
#                 weighted_ratings += similarity_score * rating
#                 total_similarity += similarity_score

#         if total_similarity != 0:
#             item_scores.append((item_id, weighted_ratings / total_similarity))

#     item_scores.sort(key=lambda x: x[1], reverse=True)
#     top_recommendations = [item[0] for item in item_scores[:top_n]]

#     return top_recommendations


# def get_recommendations_for_user(user_id):
#     # Load product data from Product_Master table
#     product_data = Product_Master.objects.all().values('id', 'name')

#     # Load order data from Order model
#     order_data = Order.objects.filter(user__user__id=user_id)

#     # Create a user-item matrix based on order data
#     ratings_data = []
#     id_mapping = {}  # Mapping of unique values in 'id' column to unique integer identifiers
#     unique_id = 1

#     for order in order_data:
#         rating = order.review_set.first().ranking if order.review_set.first() else 1
#         product_ids = ast.literal_eval(order.productid)  # Convert string representation of list to list
#         for product_id in product_ids:
#             if product_id not in id_mapping:
#                 id_mapping[product_id] = unique_id
#                 unique_id += 1

#             ratings_data.append({
#                 'user_id': user_id,
#                 'id': id_mapping[product_id],  # Use the unique integer identifier
#                 'rating': rating
#             })

#     ratings_data = pd.DataFrame(ratings_data)
#     # Remove duplicate entries
#     ratings_data = ratings_data.drop_duplicates()

#     # Convert 'id' column to int64 data type
#     ratings_data['id'] = ratings_data['id'].astype('int64')

#     # Merge product data with ratings data to get product names
#     ratings_data = pd.merge(ratings_data, pd.DataFrame(product_data), left_on='id', right_on='id')

#     # Remove duplicate entries from ratings_data
#     ratings_data = ratings_data.drop_duplicates(['user_id', 'id'])

#     # Perform aggregation if needed
#     ratings_matrix = ratings_data.pivot(index='user_id', columns='id', values='rating').fillna(0)

#     # Compute item-item similarity matrix using cosine similarity
#     item_similarity_matrix = cosine_similarity(ratings_matrix.T)
#     print(ratings_matrix, "Bhuwan",  item_similarity_matrix)
#     # Get top N recommended items for the user
#     top_recommendations = get_recommendations(user_id, ratings_matrix, item_similarity_matrix)

#     # Map product names to recommended items
#     recommended_products = [product_data[product_data['id'] == item]['name'].iloc[0] for item in top_recommendations]

#     return recommended_products

def get_recommendations_for_user(user_id, top_n=5):
    user_reviews = Review.objects.filter(user__user__id=user_id)  # Get reviews for the user

    # Collect the product IDs and ratings given by the user
    user_ratings = {}
    for review in user_reviews:
        product_id = review.product.id  # Assuming the product ID is stored in the 'id' field of the 'Product_Master' model
        rating = int(review.ranking)  # Assuming the rating is stored as an integer in the 'ranking' field

        user_ratings.setdefault(product_id, []).append(rating)

    # Filter out the products already rated by the user
    rated_products = set(user_ratings.keys())
    all_products = Product_Master.objects.all()
    unrated_products = [product for product in all_products if product.id not in rated_products]

    # Sort unrated products based on their average rating
    unrated_products.sort(key=lambda p: sum(user_ratings.get(p.id, [0])) / len(user_ratings.get(p.id, [0])), reverse=True)

    # Return the top N recommended products
    top_recommendations = [product.id for product in unrated_products[:top_n]]
    return top_recommendations


# Usage example:
# user_id = 123  # Replace with the actual user ID
# recommended_products = get_recommendations_for_user(user_id)

# # Print the recommended products
# print("Recommended Products:")
# for product_id in recommended_products:
#     print(product_id)


