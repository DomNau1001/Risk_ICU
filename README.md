# Risk ICU

Risk_ICU is a tool to assess the mortality risk of patients on the Intensive Care Unit (ICU). It can be used either for a quick initial risk stratification at the first patient encounter or with more laboratory values and further clinical assessment as an advanced risk stratification device.

During the two project weeks we trained and deployed two machine learning models:

The initial risk assessment model is intended to be used by medical personnel as a quick first assessment for patients that have just entered the ICU. The data points used to train the model were minimum, simulating only those parameters 24/7 available for risk assessments in all ICUs independently of the hospital´s level of care. To predict the risk, we used a XGBoost model, which was optimized using random search after extensive data preprocessing.
The advanced risk assessment model was trained with more complex values that e.g. require clinical laboratories. We opted against the usage of parameters that require a specific technical infrastructure to make the application available to as many hospitals as possible. For this task we built a machine learning structure optimized via random search consisting of a Decision Tree model with Adaptive Boosting combined through stacking with a XGBoost model.
To train and test our models we used patient data gathered either during the first hour or the first 24 hours of an ICU stay, as made available by MIT's GOSSIS community initiative with privacy certification from the Harvard Privacy Lab. This dataset contains around 180 features for more than 130,000 patients from multiple countries, spanning a one-year timeframe.

Please use the navigation bar on the left to get to the models.

Authors: Julia Decker, William Brudenell, Francisco Chaves, Dominik Naumann.

Feel free to check out the project.

https://riskicu.streamlit.app/#welcome-to-risk-icu
