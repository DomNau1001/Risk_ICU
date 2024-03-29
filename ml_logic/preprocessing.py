import pandas as pd
import numpy as np
import pickle

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, MinMaxScaler


def preprocessing_24_hour(data):

    #Clear Data
    final_df = data.drop(columns = ["hospital_admit_source","readmission_status", "pre_icu_los_days", "encounter_id", "patient_id", "hospital_id", "icu_stay_type", "icu_type", "icu_id", "apache_3j_bodysystem", "apache_2_bodysystem", "apache_4a_hospital_death_prob", "height", "weight", "aids", "lymphoma", "leukemia", "ethnicity"])
    final_df = final_df[final_df["elective_surgery"] != 1]

    keywords = ["h1", "apache", "noninvasive"]
    columns_to_keep = [col for col in final_df.columns if not any(keyword in col for keyword in keywords)]

    final_df = final_df[columns_to_keep].drop(columns = ["elective_surgery"])

    final_df["gcs_eyes"] = data["gcs_eyes_apache"]
    final_df["gcs_motor"] = data["gcs_motor_apache"]
    final_df["gcs_verbal"] = data["gcs_verbal_apache"]
    final_df["ventilated"] = data["ventilated_apache"]

    boolean_mask = (final_df["d1_resprate_max"] < 70)
    final_df = final_df[boolean_mask]


    #Drop columns with >30% NA
    missing_data = final_df.isnull().sum().sort_values(ascending=False)/len(data)*100
    columns_to_drop = missing_data[missing_data > 30]
    final_df.drop(columns = list(columns_to_drop.keys()), inplace=True)


    #Define X and y
    y = final_df["hospital_death"]
    X = final_df.drop(columns = "hospital_death")


    #Impute Missing Data
    nums_pre = X.select_dtypes(include=[np.number])
    nums_pre.drop(columns = ["diabetes_mellitus", "cirrhosis", "hepatic_failure", "immunosuppression", "solid_tumor_with_metastasis", "ventilated"], inplace = True)

    cats_pre = X.select_dtypes(exclude = np.number)
    cats_pre["diabetes_mellitus"] = X["diabetes_mellitus"]
    cats_pre["cirrhosis"] = X["cirrhosis"]
    cats_pre["hepatic_failure"] = X["hepatic_failure"]
    cats_pre["immunosuppression"] = X["immunosuppression"]
    cats_pre["solid_tumor_with_metastasis"] = X["solid_tumor_with_metastasis"]
    cats_pre["ventilated"] = X["ventilated"]

    imputer_cats = SimpleImputer(strategy = "most_frequent")
    imputer_nums = SimpleImputer(strategy = "median")

    cats = imputer_cats.fit_transform(cats_pre)
    nums = imputer_nums.fit_transform(nums_pre)

    cats_post = pd.DataFrame(cats, columns = cats_pre.columns)
    nums_post = pd.DataFrame(nums, columns = nums_pre.columns)

    X_post = pd.concat([cats_post, nums_post], axis = 1, sort = False)


    #Encoding
    X_post_cats = X_post[["gender", "icu_admit_source","diabetes_mellitus", "cirrhosis", "hepatic_failure", "immunosuppression", "solid_tumor_with_metastasis", "ventilated"]]
    X_post_nums = X_post.drop(columns = ["gender", "diabetes_mellitus", "cirrhosis", "hepatic_failure", "immunosuppression", "solid_tumor_with_metastasis", "icu_admit_source", "ventilated"])

    ohe = OneHotEncoder(sparse_output=False, drop = "if_binary", handle_unknown="ignore")

    ohe.fit(X_post_cats[["gender"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["gender"]])
    X_post_cats.drop(columns = "gender", inplace = True)

    ohe.fit(X_post_cats[["icu_admit_source"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["icu_admit_source"]])
    X_post_cats.drop(columns = "icu_admit_source", inplace = True)

    ohe.fit(X_post_cats[["diabetes_mellitus"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["diabetes_mellitus"]])
    X_post_cats.drop(columns = "diabetes_mellitus", inplace = True)

    ohe.fit(X_post_cats[["cirrhosis"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["cirrhosis"]])
    X_post_cats.drop(columns = "cirrhosis", inplace = True)

    ohe.fit(X_post_cats[["hepatic_failure"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["hepatic_failure"]])
    X_post_cats.drop(columns = "hepatic_failure", inplace = True)

    ohe.fit(X_post_cats[["immunosuppression"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["immunosuppression"]])
    X_post_cats.drop(columns = "immunosuppression", inplace = True)

    ohe.fit(X_post_cats[["solid_tumor_with_metastasis"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["solid_tumor_with_metastasis"]])
    X_post_cats.drop(columns = "solid_tumor_with_metastasis", inplace = True)

    ohe.fit(X_post_cats[["ventilated"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["ventilated"]])
    X_post_cats.drop(columns = "ventilated", inplace = True)

    X_post = pd.concat([X_post_cats, X_post_nums], axis = 1, sort = False)
    X_post.drop(columns = ["icu_admit_source_Other Hospital", "icu_admit_source_Operating Room / Recovery", "icu_admit_source_Other ICU", "icu_admit_source_Floor"], inplace= True)
    X_post.rename(columns = {"icu_admit_source_Accident & Emergency":"icu_admit_source_Accident_Emergency"}, inplace = True)
    X_post.rename(columns = {"ventilated_1.0":"ventilated"}, inplace = True)

    X_post.sort_index(axis=1, inplace=True)


    #Feature Selection
    X_post.drop(columns = ["d1_bun_min", "d1_creatinine_min", "d1_hematocrit_max", "d1_hematocrit_min", "d1_hemaglobin_max", "d1_platelets_max"], inplace = True)

    even_more = ["immunosuppression_1.0", "gender_M", "d1_calcium_max", "d1_potassium_min", "cirrhosis_1.0", "d1_potassium_max", "hepatic_failure_1.0", "d1_diasbp_max", "d1_calcium_min", "diabetes_mellitus_1.0", "d1_glucose_max", "d1_mbp_max", "d1_spo2_max", "d1_diasbp_min", "solid_tumor_with_metastasis_1.0", "d1_hco3_min", "d1_sodium_max"]
    X_post.drop(columns = even_more, inplace = True)


    #Scaling
    mm_scaler = MinMaxScaler()

    X_preprocessed = mm_scaler.fit_transform(X_post)
    X_preprocessed = pd.DataFrame(X_preprocessed, columns = X_post.columns)

    file_name = "mm_scaler_24.pkl"
    pickle.dump(mm_scaler, open(file_name, "wb"))


    #Target Encoding
    label_encoder = LabelEncoder()

    y_binary_preprocessed = label_encoder.fit_transform(y)
    y_binary_preprocessed = pd.DataFrame(y_binary_preprocessed)

    y_cont_preprocessed = data["apache_4a_icu_death_prob"]
    y_cont_preprocessed = pd.DataFrame(y_cont_preprocessed)
    y_cont_preprocessed.rename(columns = {"apache_4a_icu_death_prob":"mortality_prob"}, inplace = True)

    return X_preprocessed, y_binary_preprocessed




def preprocessing_1_hour(data):

    # remove columns containing the word "apache"
    columns_to_drop = [col for col in data.columns if 'apache' in col and col != "apache_4a_icu_death_prob"]
    no_apache = data.drop(columns=columns_to_drop)


    # remove d1 data
    columns_to_drop_2 = [col for col in no_apache.columns if 'd1' in col]
    no_d1 = no_apache.drop(columns=columns_to_drop_2)


    # Remove columns where null data is over 30%
    threshold = 30000
    non_null_counts = no_d1.notnull().sum()
    columns_to_drop_3 = [col for col in non_null_counts.index if col != 'h1_lactate_max' and non_null_counts[col] < threshold]
    no_nulls = no_d1.drop(columns=columns_to_drop_3)


    # Remove features
    #initially
    d_features_to_drop = ["h1_sysbp_noninvasive_max","h1_sysbp_noninvasive_min","h1_mbp_noninvasive_max","h1_mbp_noninvasive_min","h1_diasbp_noninvasive_max", "h1_diasbp_noninvasive_min","height","icu_id","readmission_status","weight","encounter_id", "patient_id","hospital_admit_source", "icu_stay_type", "icu_type", "leukemia", "aids", "lymphoma"]
    h1_data = no_nulls.drop(columns= d_features_to_drop)
    #after SHAP evaluation
    more_to_drop = ['h1_heartrate_min',	"h1_mbp_max",'h1_sysbp_max', 'h1_resprate_max','h1_spo2_min', 'h1_temp_max', 'h1_glucose_max','h1_inr_max', 'h1_inr_min',"h1_diasbp_max","h1_diasbp_min","ethnicity","apache_4a_icu_death_prob","solid_tumor_with_metastasis","hepatic_failure","diabetes_mellitus","hospital_id"]
    h1_data_2 = h1_data.drop(columns= more_to_drop)


    #Define X and ys
    y = h1_data_2["hospital_death"]
    X = h1_data_2.drop(columns = "hospital_death")


    #Impute Missing Data
    nums_pre = X.select_dtypes(include=[np.number])
    nums_pre.drop(columns = ["cirrhosis", "immunosuppression"], inplace = True)

    cats_pre = X.select_dtypes(exclude = np.number)
    cats_pre["cirrhosis"] = X["cirrhosis"]
    cats_pre["immunosuppression"] = X["immunosuppression"]


    imputer_cats = SimpleImputer(strategy = "most_frequent")
    imputer_nums = SimpleImputer(strategy = "median")

    cats = imputer_cats.fit_transform(cats_pre)
    nums = imputer_nums.fit_transform(nums_pre)

    cats_post = pd.DataFrame(cats, columns = cats_pre.columns)
    nums_post = pd.DataFrame(nums, columns = nums_pre.columns)

    X_post = pd.concat([cats_post, nums_post], axis = 1, sort = False)


    #Encoding
    X_post_cats = X_post[["gender", "icu_admit_source","cirrhosis",  "immunosuppression"]]
    X_post_nums = X_post.drop(columns = ["gender", "cirrhosis","immunosuppression", "icu_admit_source"])

    ohe = OneHotEncoder(sparse_output=False, drop = "if_binary", handle_unknown="ignore")


    ohe.fit(X_post_cats[["gender"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["gender"]])
    X_post_cats.drop(columns = "gender", inplace = True)

    ohe.fit(X_post_cats[["icu_admit_source"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["icu_admit_source"]])
    X_post_cats.drop(columns = "icu_admit_source", inplace = True)

    ohe.fit(X_post_cats[["immunosuppression"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["immunosuppression"]])
    X_post_cats.drop(columns = "immunosuppression", inplace = True)

    ohe.fit(X_post_cats[["cirrhosis"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["cirrhosis"]])
    X_post_cats.drop(columns = "cirrhosis", inplace = True)


    X_post = pd.concat([X_post_cats, X_post_nums], axis = 1, sort = False)
    X_post.drop(columns = ["icu_admit_source_Other Hospital", "icu_admit_source_Operating Room / Recovery", "icu_admit_source_Other ICU", "icu_admit_source_Floor"], inplace= True)
    X_post.rename(columns = {"icu_admit_source_Accident & Emergency":"icu_admit_source_Accident_Emergency"}, inplace = True)
    X_post.rename(columns = {"cirrhosis_1.0":"cirrhosis"}, inplace = True)
    X_post.rename(columns = {"immunosuppression_1.0":"immunosuppression"}, inplace = True)

    X_post.sort_index(axis=1, inplace=True)

    #Scaling
    mm_scaler = MinMaxScaler()

    X_preprocessed = mm_scaler.fit_transform(X_post)
    X_preprocessed = pd.DataFrame(X_preprocessed, columns = X_post.columns)

    file_name = "mm_scaler_1.pkl"
    pickle.dump(mm_scaler, open(file_name, "wb"))


    #Target Encoding
    label_encoder = LabelEncoder()

    y_binary_preprocessed = label_encoder.fit_transform(y)
    y_binary_preprocessed = pd.DataFrame(y_binary_preprocessed)

    y_cont_preprocessed = data["apache_4a_icu_death_prob"]
    y_cont_preprocessed = pd.DataFrame(y_cont_preprocessed)
    y_cont_preprocessed.rename(columns = {"apache_4a_icu_death_prob":"mortality_prob"}, inplace = True)

    return X_preprocessed, y_binary_preprocessed
