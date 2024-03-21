import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, MinMaxScaler


def preprocessing_24_hour(data):

    #Clear Data
    final_df = data.drop(columns = ["hospital_admit_source","readmission_status", "pre_icu_los_days", "encounter_id", "patient_id", "hospital_id", "icu_stay_type", "icu_type", "icu_id", "apache_3j_bodysystem", "apache_2_bodysystem", "apache_4a_hospital_death_prob", "height", "weight", "aids", "lymphoma", "leukemia"])
    final_df = final_df[final_df["elective_surgery"] != 1]

    keywords = ["h1", "apache", "noninvasive"]
    columns_to_keep = [col for col in final_df.columns if not any(keyword in col for keyword in keywords)]

    final_df["gcs_eyes"] = data["gcs_eyes_apache"]
    final_df["gcs_motor"] = data["gcs_motor_apache"]
    final_df["gcs_verbal"] = data["gcs_verbal_apache"]
    final_df["ventilated"] = data["ventilated_apache"]

    final_df = final_df[columns_to_keep].drop(columns = ["elective_surgery"])

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
    nums_pre.drop(columns = ["diabetes_mellitus", "cirrhosis", "hepatic_failure", "immunosuppression", "solid_tumor_with_metastasis"], inplace = True)

    cats_pre = X.select_dtypes(exclude = np.number)
    cats_pre["diabetes_mellitus"] = X["diabetes_mellitus"]
    cats_pre["cirrhosis"] = X["cirrhosis"]
    cats_pre["hepatic_failure"] = X["hepatic_failure"]
    cats_pre["immunosuppression"] = X["immunosuppression"]
    cats_pre["solid_tumor_with_metastasis"] = X["solid_tumor_with_metastasis"]

    imputer_cats = SimpleImputer(strategy = "most_frequent")
    imputer_nums = SimpleImputer(strategy = "median")

    cats = imputer_cats.fit_transform(cats_pre)
    nums = imputer_nums.fit_transform(nums_pre)

    cats_post = pd.DataFrame(cats, columns = cats_pre.columns)
    nums_post = pd.DataFrame(nums, columns = nums_pre.columns)

    X_post = pd.concat([cats_post, nums_post], axis = 1, sort = False)


    #Encoding
    X_post_cats = X_post[["ethnicity", "gender", "icu_admit_source","diabetes_mellitus", "cirrhosis", "hepatic_failure", "immunosuppression", "solid_tumor_with_metastasis"]]
    X_post_nums = X_post.drop(columns = ["ethnicity", "gender", "diabetes_mellitus", "cirrhosis", "hepatic_failure", "immunosuppression", "solid_tumor_with_metastasis", "icu_admit_source"])

    ohe = OneHotEncoder(sparse_output=False, drop = "if_binary", handle_unknown="ignore")

    ohe.fit(X_post_cats[["ethnicity"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["ethnicity"]])
    X_post_cats.drop(columns = "ethnicity", inplace = True)

    ohe.fit(X_post_cats[["gender"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["gender"]])
    X_post_cats.drop(columns = "gender", inplace = True)

    ohe.fit(X_post_cats[["icu_admit_source"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["icu_admit_source"]])
    X_post_cats.drop(columns = "icu_admit_source", inplace = True)

    X_post = pd.concat([X_post_cats, X_post_nums], axis = 1, sort = False)


    #Scaling
    mm_scaler = MinMaxScaler()

    X_preprocessed = mm_scaler.fit_transform(X_post)
    X_preprocessed = pd.DataFrame(X_preprocessed, columns = X_post.columns)


    #Target Encoding
    label_encoder = LabelEncoder()

    y_binary_preprocessed = label_encoder.fit_transform(y)
    y_binary_preprocessed = pd.DataFrame(y_binary_preprocessed)

    y_cont_preprocessed = data["apache_4a_icu_death_prob"]
    y_cont_preprocessed = pd.DataFrame(y_cont_preprocessed)
    y_cont_preprocessed.rename(columns = {"apache_4a_icu_death_prob":"mortality_prob"}, inplace = True)


    #Feature Selection
    X_preprocessed.drop(columns = ["d1_bun_min", "d1_creatinine_min", "d1_hematocrit_max", "d1_hematocrit_min", "d1_hemaglobin_max", "d1_platelets_max"], inplace = True)

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
    columns_to_drop_3 = non_null_counts[non_null_counts < threshold].index.tolist()
    no_nulls = no_d1.drop(columns=columns_to_drop_3)


    # Remove columns
    d_features_to_drop = ["apache_4a_icu_death_prob","h1_sysbp_noninvasive_max","h1_sysbp_noninvasive_min","h1_mbp_noninvasive_max","h1_mbp_noninvasive_min","h1_diasbp_noninvasive_max", "h1_diasbp_noninvasive_min","height","icu_id","readmission_status","weight","encounter_id", "patient_id","hospital_admit_source", "icu_stay_type", "icu_type", "pre_icu_los_days", "leukemia", "aids", "lymphoma"]
    h1_data = no_nulls.drop(columns= d_features_to_drop)


    #Define X and ys
    y = h1_data["hospital_death"]
    X = h1_data.drop(columns = "hospital_death")


    #Impute Missing Data
    nums_pre = X.select_dtypes(include=[np.number])
    nums_pre.drop(columns = ["diabetes_mellitus", "cirrhosis", "hepatic_failure", "immunosuppression", "solid_tumor_with_metastasis"], inplace = True)

    cats_pre = X.select_dtypes(exclude = np.number)
    cats_pre["diabetes_mellitus"] = X["diabetes_mellitus"]
    cats_pre["cirrhosis"] = X["cirrhosis"]
    cats_pre["hepatic_failure"] = X["hepatic_failure"]
    cats_pre["immunosuppression"] = X["immunosuppression"]
    cats_pre["solid_tumor_with_metastasis"] = X["solid_tumor_with_metastasis"]

    imputer_cats = SimpleImputer(strategy = "most_frequent")
    imputer_nums = SimpleImputer(strategy = "median")

    cats = imputer_cats.fit_transform(cats_pre)
    nums = imputer_nums.fit_transform(nums_pre)

    cats_post = pd.DataFrame(cats, columns = cats_pre.columns)
    nums_post = pd.DataFrame(nums, columns = nums_pre.columns)

    X_post = pd.concat([cats_post, nums_post], axis = 1, sort = False)


    #Encoding
    X_post_cats = X_post[["ethnicity", "gender", "icu_admit_source","diabetes_mellitus", "cirrhosis", "hepatic_failure", "immunosuppression", "solid_tumor_with_metastasis"]]
    X_post_nums = X_post.drop(columns = ["ethnicity", "gender", "diabetes_mellitus", "cirrhosis", "hepatic_failure", "immunosuppression", "solid_tumor_with_metastasis", "icu_admit_source"])

    ohe = OneHotEncoder(sparse_output=False, drop = "if_binary", handle_unknown="ignore")

    ohe.fit(X_post_cats[["ethnicity"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["ethnicity"]])
    X_post_cats.drop(columns = "ethnicity", inplace = True)

    ohe.fit(X_post_cats[["gender"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["gender"]])
    X_post_cats.drop(columns = "gender", inplace = True)

    ohe.fit(X_post_cats[["icu_admit_source"]])
    X_post_cats[ohe.get_feature_names_out()] = ohe.transform(X_post_cats[["icu_admit_source"]])
    X_post_cats.drop(columns = "icu_admit_source", inplace = True)

    X_post = pd.concat([X_post_cats, X_post_nums], axis = 1, sort = False)


    #Scaling
    mm_scaler = MinMaxScaler()

    X_preprocessed = mm_scaler.fit_transform(X_post)
    X_preprocessed = pd.DataFrame(X_preprocessed, columns = X_post.columns)


    #Target Encoding
    label_encoder = LabelEncoder()

    y_binary_preprocessed = label_encoder.fit_transform(y)
    y_binary_preprocessed = pd.DataFrame(y_binary_preprocessed)

    y_cont_preprocessed = data["apache_4a_icu_death_prob"]
    y_cont_preprocessed = pd.DataFrame(y_cont_preprocessed)
    y_cont_preprocessed.rename(columns = {"apache_4a_icu_death_prob":"mortality_prob"}, inplace = True)

    return X_preprocessed, y_binary_preprocessed
