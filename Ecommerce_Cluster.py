import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# First we need to load data, you can edit the path to the file
data = pd.read_csv(r'C:\\Users\\Green\\Dropbox\\PC (2)\\Downloads\\Compressed\\sales_data.csv', encoding='latin1')

# Here we remove leading and trailing whitespaces from column names
data.columns = data.columns.str.strip()

# Here we need to clean the data by removing currency symbols and converting to float
data['Sales'] = data['Sales'].replace('[\$,]', '', regex=True).astype(float)
data['Profit'] = data['Profit'].replace('[\$,]', '', regex=True).astype(float)
data['Shipping Cost'] = data['Shipping Cost'].replace('[\$,]', '', regex=True).astype(float)

# Here we need to select relevant columns
data_subset = data[['Ship Mode', 'Product Category', 'Sales', 'Quantity', 'Discount', 'Profit', 'Shipping Cost', 'Order Priority', 'Segment']]

# And here we need to check for missing values
print(data_subset.isnull().sum())

# Here we can separate numeric and categorical columns
numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit', 'Shipping Cost']
categorical_cols = ['Ship Mode', 'Product Category', 'Order Priority', 'Segment']

# And then we can fill missing values
data_subset[numeric_cols] = data_subset[numeric_cols].fillna(data_subset[numeric_cols].mean())
data_subset[categorical_cols] = data_subset[categorical_cols].fillna(data_subset[categorical_cols].mode().iloc[0])

# Here we need to encode categorical variables
data_encoded = pd.get_dummies(data_subset, drop_first=True)

# And here we scale the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data_encoded)

# Here we can determine the optimal number of clusters using the Elbow method
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(scaled_data)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

# Here we need to perform K-means clustering with the optimal number of clusters
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(scaled_data)

# Here we can add cluster labels to the data
data_subset['Cluster'] = kmeans.labels_

# Here we can make it more beautiful by visualizing the clusters using Plotly for interactive charts
fig = px.scatter(data_subset, x='Sales', y='Profit', color='Cluster', title='Customer Segments based on Sales and Profit')
fig.show()

# Here we can add additional visualizations
sns.countplot(data=data_subset, x='Ship Mode', hue='Cluster')
plt.title('Distribution of Ship Mode across Clusters')
plt.show()

sns.countplot(data=data_subset, x='Product Category', hue='Cluster')
plt.title('Distribution of Product Category across Clusters')
plt.show()

sns.countplot(data=data_subset, x='Order Priority', hue='Cluster')
plt.title('Distribution of Order Priority across Clusters')
plt.show()

sns.countplot(data=data_subset, x='Segment', hue='Cluster')
plt.title('Distribution of Customer Segment across Clusters')
plt.show()
