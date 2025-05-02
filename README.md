

# New Game +

# Final Report
Data preprocessing and cleaning
Dropping Null/Empty values
There were unnamed games in our dataset, we saw that these were most likely mistakes or test/development games. So we dropped the null values in names because we thought it wouldn’t make sense to train the model on these unnamed games and have it recommend unnamed games.
Dropping Columns
We dropped columns that we deemed irrelevant or in a non numerical format  in which we could not use or were linearly dependent.
The list of features dropped includes
'name','tags','reviews', 'appid', 'detailed_description', 'about_the_game', 'short_description', 'header_image', 'website', 'support_url','support_email','metacritic_url','notes', 'packages', 'developers', 'publishers','screenshots', 'movies','user_score','score_rank','estimated_owners','positive','negative'
One Hot Encoding
For string features such as genre, categories and supported languages we implemented one hot encoding. 
We first obtained a list of every single unique value for each column utilizing a set. 
After then we turned each unique value into its own corresponding column where for each game, 1 indicated that the game contained the specific genre category or language and 0 indicates the game did not.
Removing correlated genre and category features
We utilized a heatmap to help locate correlations between features.
Any two features with a correlation above a 0.5 threshold, we picked one to remove
This helped improve model accuracy and reduces redundant information since similar features can potentially double their influence

Detailed description of data modeling methods used so far.
Features chosen
We realized that our 300 features was a bit too many for the model, so we had to tone it down a bit
The majority of these features were created from the one hot encoding of string features, so for now we just got rid of the features we believe wouldn’t impact the clusterings too much (i.e supported_languages & audio_languages)
This successfully dropped our features to around 90
We then used the heatmap corrlelation matrix to merge highly correlated features. This then further dropped our features to 66
However, clustering based on 66 features still felt like a lot, so we decided to create multiple clusters based on the features
Finding the right K for each clustering
We utilized the “elbow method” as discussed from lecture, where the optimal K is found through iterating over several values of k (in our case we did 1 - 20) until there was a low inertia AND a low number of clusters
Based on this, we found that around k=16 worked the best for genres, k=5 for pricing, and k=5 for peak concurrent users, k=39 for categories, and k=18 for the remaining columns
Kmeans++
We utilized the sci-kit learn library in order to initialize the k centroids and keep moving them until they converged. For each cluster, we used Kmeans++
Silhouette score
Also from sci-kit learn library, we were able to easily calculate the silhouette scores of our clusterings based on their average distance to other points in its cluster and average distance to points in their nearest neighbor cluster


Preliminary results. (e.g. we fit a linear model to the data and we achieve promising results, or we did some clustering and we notice a clear pattern in the data)
Silhouette score evaluation
According to the silhouette scores of 0.32, 0.03, 0.01 that we measured after clustering, our clustering seems to be okay/not too good, but with a lot of room for improvement (before feature engineering)
After feature engineering, we successfully increased the scores to 0.65, 0.54, and 0.21
Data pattern from cluster visualization
Genre cluster
These clusters offered lots of insights into what genres are typically paired with each others
For example, typically games that have genres of Indie, Action, and Adventure go well with each other
Another example, typically games that have genres of Indie and Casual go well with each other
This would then be a factor we can use to properly recommend a user a related game
Categories cluster
This cluster was very similar to the genre cluster, except for categories
Pricing distribution cluster
These clusters tell us the distribution of the pricing for the games
When recommending similar games, we can take into consideration whether the new game is inside the pricing cluster of the games the user has previously played
Although we realize that this feature alone isn’t the best, we will make sure to reduce its weight when recommending a game
Peak concurrent users cluster
These clusters group the games based on their concurrent user count, which can be another feature to consider when recommending a game. Someone who likes to play popular games might also like other similar popular games


Semantic Text-Based Clustering
Sentence Transformer
We used a transformer model to embed the “about_the_game” text field for each game
Tried this instead of TFIDF to try grouping games based on the semantic meanings of descriptions rather than by the individual words used in the descriptions
Transformed each description into a vector, added the length of the description as a normalized feature
Clusters
After generating the sentence embeddings, we ran KMeans clustering to get clusters based on how the games describe themselves
We then sampled games from each cluster to interpret their themes
Preliminary Conclusions
Clusters captured narrative-heavy single-player games, competitive multiplayer shooters, casual/co-op games, anime and niche indies, and more.
The cluster content differed from genre or tag clusters, offering a new perspective on how to group and recommend games.
Games with similar tone or gameplay feel, even with different tags, ended up in the same cluster.

Modeling Approach
We utilized separate feature sets for clustering. We clustered based on genre, category, price, peak player count, an all columns cluster and a remaining columns cluster (all features not in the first four). We tried different combinations of clusters for the final model before eventually utilizing the genre cluster, the category cluster and the remaining columns cluster. 
Our reasoning was that we felt that the model really utilized these descriptive tags of genre and category when recommending other games. Since we aimed to recommend games based on similar games in the user’s profile, it made sense that the model would utilize these features.

Frontend
Created a user friendly UI for entering their steam ID
Once their steam ID is entered, the frontend calls the backend to retrieve the list of recommended games and displays them based on how strong each one matches depending on the user’s top games
Built with React.js and TailwindCSS

Backend
Framework and Architecture:
Built using Django and Django REST Framework
Handles API requests from the frontend and communicates with Steam API
Uses preprocessed .pkl files containing clustered game data for efficient computation
Data Loading:
load_clustered_data() loads the full dataframe with genre encodings and cluster labels
load_clustered_metadata() loads a trimmed version of the dataset for frontend display
API Endpoint 1: /steam/get_owned_games/:
Accepts a steamid as a query parameter
Fetches all owned games from the Steam API
Filters and sorts the top 15 games by playtime
Enriches each game with additional metadata like price and genre
Returns JSON data with fields used by the frontend
API Endpoint 2: /steam/recommend_games/:
Fetches top 15 games by playtime
FIlters out games without sufficient info
Builds a user profile vector using features like price, genre, and clusters
Constructs a comparison matrix of valid games
Filters out obscure games
Normalizes numeric features
Computes weighted cosine similarity between the user vector and candidates
Excludes any games the user already owns
Returns top 15 most similar games
Helper Function fetch_game_metadata(appid):
Calls the Steam API
Extracts genres and price data
Handles failures/missing fields
Model Integration:
Aligned with the notebook’s clustering strategy
Uses genre_cluster, categories_cluster, and remaining_clusters
These clusters were selected based on silhouette score
Other features are baked into the “remaining” cluster to avoid any overfitting
Final Output:
JSON response for each recommendation which includes the title, description, store link, and other characteristics

  
# Final Report
https://docs.google.com/document/d/1XramLsVcYb4dYsfAzyRMKn--FUKf_o6VRioA4S6DU9A/edit?usp=sharing

**Link to Presentation:**
https://www.youtube.com/watch?v=DNrj3UnXUZo

### Preliminary visualizations of data
* Print outs
  * Head
    * This gave us a good idea of how each column contains when we were deciding whether to drop or merge them
  * Data types
    * We saw that the data had mostly numbers (one float and the rest were int), but there were several categorical/non-numerical variables such as name, release_date, detailed_description, about_the_game, short_description, reviews, header_image, website, support_url, support_email, windows, mac, linux, metacritic_url, notes, supported_languages, full_audio_languages, packages, etc.
  * Nulls
    * We were able to find the sum of null values for each column in order to better gauge what columns we should be dropping or filling
* Dataset Insights
  * Average Playtime by Price
    * This graph aims to explore whether there's a relationship between how much a game costs and how long people actually play it. The idea is to understand if higher priced games offer more value in terms of playtime, or if cheaper or free games still manage to keep users engaged for long periods. We might consider adding weight to playtime when recommending a game.
  * Platform Support
    * We wanted to find how important the platform support is. It was surprising as we found that 100% of games supported Windows, but only 18.4% for Mac and 13.3% for Linux. This means it could be important to consider what platform the user has, so we can make relevant recommendations.
* Feature Correlation heatmaps
  * We split up our features into 3 graphs: Genres, Categories, and “The Rest”
  * These correlation heatmaps let us know which features we should be merging. Features with high correlations with each other should be merged as one
  * Genres
    * The majority of the genres seem to be independent of each other
    * However, we still have some genres such as Documentary & Short, Episodic & 360 Video, Movie & 360 Video, Violent & Gore, etc showing high correlation. All of these make sense as to why they are so highly correlated
  * Game Categories
    * The majority of game categories seem to also be independent of each other
    * However, like the genres, we still have some game categories such as Remote Play on Phone & Remote Play on Tablet, Shared Split Screen vs Remote Play Together, Online Pvp & Pvp. All of these also make sense as to why they are so highly correlated
  * “The Rest” of the features
    * These are the features from our dataset that we did not one hot encode
    * There seems to be a bit of correlation between many of the last features, but otherwise mostly independent (i.e Recommendations & num_review, num_review & peak_count)





### Detailed description of data processing done so far
* Dropping Null/Empty values
  * There were unnamed games in our dataset, we saw that these were most likely mistakes or test/development games. So we dropped the null values in names because we thought it wouldn’t make sense to train the model on these unnamed games and have it recommend unnamed games.
Dropping Columns
  * We dropped columns that we deemed irrelevant or in a non numerical format  in which we could not use or were linearly dependent.
  * The list of features dropped includes
'name','tags','reviews', 'appid', 'detailed_description', 'about_the_game', 'short_description', 'header_image', 'website', 'support_url','support_email','metacritic_url','notes', 'packages', 'developers', 'publishers','screenshots', 'movies','user_score','score_rank','estimated_owners','positive','negative'
* One Hot Encoding
  * For string features such as genre, categories and supported languages we implemented one hot encoding. 
  * We first obtained a list of every single unique value for each column utilizing a set. 
  * After then we turned each unique value into its own corresponding column where for each game, 1 indicated that the game contained the specific genre category or language and 0 indicates the game did not.


### Detailed description of data modeling methods used so far
* Features chosen
  * We realized that our 300 features was a bit too many for the model, so we had to tone it down a bit
  * The majority of these features were created from the one hot encoding of string features, so for now we just got rid of the features we believe wouldn’t impact the clusterings too much (i.e supported_languages & audio_languages)
  * This successfully dropped our features to around 90
  * However, clustering based on 90 features still felt like a lot, so we decided to create multiple clusters based on the features
* Finding the right K for each clustering
  * We utilized the “elbow method” as discussed from lecture, where the optimal K is found through iterating over several values of k (in our case we did 1 - 20) until there was a low inertia AND a low number of clusters
  * Based on this, we found that around k=16 worked the best for genres, k=5 for pricing, and k=5 for peak concurrent users
* Kmeans++
  * We utilized the sci-kit learn library in order to initialize the k centroids and keep moving them until they converged. For each cluster, we used Kmeans++
* Silhouette score
  * Also from sci-kit learn library, we were able to easily calculate the silhouette scores of our clusterings based on their average distance to other points in its cluster and average distance to points in their nearest neighbor cluster


### Preliminary results
* Silhouette score evaluation
  * According to the silhouette scores of 0.32, 0.03, 0.01 that we measured after clustering, our clustering seems to be okay/not too good, but with a lot of room for improvement
  * We plan on improving this score through more feature engineering during the preprocessing part (i.e haven’t merged features with high correlation yet)
* Data pattern from cluster visualization
  * Genre cluster
    * These clusters offered lots of insights into what genres are typically paired with each others
    * For example, typically games that have genres of Indie, Action, and Adventure go well with each other
    * Another example, typically games that have genres of Indie and Casual go well with each other
  * This would then be a factor we can use to properly recommend a user a related game
* Pricing distribution cluster
  * These clusters tell us the distribution of the pricing for the games
  * When recommending similar games, we can take into consideration whether the new game is inside the pricing cluster of the games the user has previously played
  * Although we realize that this feature alone isn’t the best, we will make sure to reduce its weight when recommending a game
* Peak concurrent users cluster
  * These clusters group the games based on their concurrent user count, which can be another feature to consider when recommending a game. Someone who likes to play popular games might also like other similar popular games

**Semantic Text-Based Clustering**
* Sentence Transformer
  * We used a transformer model to embed the “about_the_game” text field for each game
  * Tried this instead of TFIDF to try grouping games based on the semantic meanings of descriptions rather than by the individual words used in the descriptions
  * Transformed each description into a vector, added the length of the description as a normalized feature
* Clusters
  * After generating the sentence embeddings, we ran KMeans clustering to get clusters based on how the games describe themselves
  * We then sampled games from each cluster to interpret their themes
* Preliminary Conclusions
  * Clusters captured narrative-heavy single-player games, competitive multiplayer shooters, casual/co-op games, anime and niche indies, and more.
  * The cluster content differed from genre or tag clusters, offering a new perspective on how to group and recommend games.
  * Games with similar tone or gameplay feel, even with different tags, ended up in the same cluster.


# Project Proposal
**Description of the project**
- New Game+ : A web app that helps gamers find new steam games based on their profile.
- Use steam dataset and api to recommend steam games to a user based on their past games played (factoring in hours played and perhaps user limitations/preferences)
- **Reach goals**:
    - Produce a list of recommended games based on the users’ owned games and play times
      
**What data needs to be collected and how you will collect it?**
- We will need to collect data for clustering related games with each other in order to recommend similar ones, we can use this existing datasets on kaggle: (https://www.kaggle.com/datasets/fronkongames/steam-games-dataset/data) 

**How you plan on modeling the data?** 
- We plan on using a Kmeans++ model in order to cluster common games with each other

**How do you plan on visualizing the data?.**
- We plan creating a heatmap of the features in order to show cluster relationships

**What is your test plan?**
- We can use silhouette scores to measure how well our clusters are
- We create the clusters using the model, and then verify our model by running through 50-100 manual tests to make sure we get recommended a game that makes sense

# 🔧 Running the Project

This project includes a **Next.js frontend** and a **Django backend** using **Pipenv** for the backend environment.

## 🖥️ Option 1: Manual Setup (Recommended for Development)

### Step 1: Clone the repository

```bash
git clone https://github.com/bvogler10/CS506_FinalProject.git
cd CS506_FinalProject
```

### Step 2: Backend (Django)
Open a terminal window
```bash
cd new-game-plus-backend
```

Activate Pipenv and install dependencies
```bash
pipenv shell
pipenv install
```

Create a `.env` file in the root backend directory (new-game-plus-backend/.env)

To use the Steam API, you’ll need a personal API key.

You can get it here:
👉 https://steamcommunity.com/dev/apikey

 - Login or create a Steam account.
 - **Note:** If you haven’t set up the Steam Mobile Authenticator, Steam will likely prompt you to do so before allowing API key access.
 - Fill in any required domain name (e.g., localhost is fine for local development).
 - Click "Register" and copy your key.

Once you have your key, add it to your .env file like this:

Add the following line:
```
STEAM_API_KEY=your_steam_api_key
```

Start the Django server
```bash
python manage.py runserver
```

The server should now be running at:
```bash
http://127.0.0.1:8000/
```

### Step 3: Frontend (Next.js)
Open a new terminal window
```bash
cd new-game-plus-frontend
```

Install frontend dependencies
```bash
npm install
```

Start the frontend development server
```bash
npm run dev
```

Open your browser and go to:
```bash
http://localhost:3000
```

## ⚙️ Option 2: Using Makefile (Docker-Based)

### Step 1: Clone the repository

```bash
git clone https://github.com/bvogler10/CS506_FinalProject.git
cd CS506_FinalProject
```

### Step 2: Add .env File to Backend
Open a terminal window
```bash
cd new-game-plus-backend
```

Create a `.env` file in the root backend directory (new-game-plus-backend/.env)

To use the Steam API, you’ll need a personal API key.

You can get it here:
👉 https://steamcommunity.com/dev/apikey

 - Login or create a Steam account.
 - **Note:** If you haven’t set up the Steam Mobile Authenticator, Steam will likely prompt you to do so before allowing API key access.
 - Fill in any required domain name (e.g., localhost is fine for local development).
 - Click "Register" and copy your key.

Once you have your key, add it to your .env file like this:

Add the following line:
```
STEAM_API_KEY=your_steam_api_key
```

### Step 3: Build Docker Containers

cd back into the root directory and run the following commands:

```bash
make build
```
```bash
make up
```

Once finished, open your browser and go to:
```bash
http://localhost:3000
```

⚠️ **Note**: This method doesn’t support interactive Jupyter notebook execution. However, the outputs are already saved in the notebook.  
> To re-run the notebook (which can take up to ~30 minutes), follow the **Manual Setup** instructions above.
