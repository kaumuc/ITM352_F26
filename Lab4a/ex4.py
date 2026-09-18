# Try to append to a tuple. It wont Work.
# Name: Kaumu Clemente
# Date : Sept 16, 2026

survey_respondents_ids = (1012, 1035, 1021, 1053)
survey_respondents_.append(1054) #This will raise an attribute error since tuples are immutable

survey_respondents = survey_respondents + (1054,) #This will work since we are creating a new tuple and assigning it to the variable
print("Updated survey respondents:", survey_respondents)