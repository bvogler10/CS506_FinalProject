# CS506_FinalProject
**Description of the project. Clear goal(s) (e.g. Successfully predict the number of students attending lecture based on the weather report).**
- PLANT PALS (name is subject to change): A mobile app that helps people take care of their houseplants. The interface would use pixel art graphics and allow users to interactively track the health of their plants.
- Create a virtual version of their plant, give it a name, and log care activities (watering, light exposure)
- App will track plant health over time, update the appearance of the plant based on health, and provide AI-generated responses to issues
  
- **Reach goals**:
    - Gamifying the system to add achievements,
    - Allow users to take a photo of the plant as an alternative easier method to extract features. Uses image classification
    - Use user’s location to detect the weather (sunny or not)
      
**What data needs to be collected and how you will collect it (e.g. scraping xyz website or polling students).**
- We will need to collect data for classifying whether a plant is healthy or not. In order to do this, we can use some existing datasets on kaggle (https://www.kaggle.com/datasets/bhavyagoyal867/plant-health-dataset) and scrape websites like Reddit r/houseplants or plant care related websites
- Hardcoded database of common houseplants with details on watering needs, light preferences, etc
- Collection of common problems for that specific plant species for AI responses

**How you plan on modeling the data (e.g. clustering, fitting a linear model, decision trees, XGBoost, some sort of deep learning method, etc.).** 
- We plan on using Random Forest for a binary classification to determine if a plant is healthy or not healthy given the features of the plant

**How do you plan on visualizing the data? (e.g. interactive t-SNE plot, scatter plot of feature x vs. feature y).**
- Dashboard of plant health over time
- Correlation heatmap comparing features for plant healthiness
- Graphs comparing specific features like watering habits and plant health

**What is your test plan? (e.g. withhold 20% of data for testing, train on data collected in October and test on data collected in November, etc.).**
- We will train the data collected from web scraping and data sets from late February to March, but this data isn’t that reliant on time
- We will withhold 25% of the data collected for testing, and train the data on the other 75%
