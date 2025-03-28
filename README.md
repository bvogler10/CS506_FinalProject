# New Game +
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

## Running the Code

This project includes a **Next.js frontend** and a **Django backend** using **Pipenv** for the backend environment.

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
Download the Kaggle dataset as a zip file and insert ONLY the games.json file into a data folder:
```
new-game-plus-backend
|____newgameplus
      |_____data
            |____ games.json
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
