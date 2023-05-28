#convert data in matrix form and training model
reader=Reader(rating_scale=(0.5,5))
data=Dataset.load_from_df(rating[['userId','movieId','rating']],reader)
train,test=train_test_split(data,test_size=0.2)
cFilter=SVD()
cFilter.fit(train)

#model evaluation
predict=cFilter.test(test)
accuracy.rmse(predict)
accuracy.mae(predict)
#creating dataFrame with unique users and movies
uUsers=rating['userId'].unique()
uMovies=rating['movieId'].unique()
user_movies=pd.DataFrame(index=uUsers,columns=uMovies)
user_movies.fillna(0,inplace=True)
user_movies.isnull().sum()
#filling data frame
userId=3
userRating={3:4.0,8:5.0,20:4.5,10:2.5}
for movieId,rating in userRating.items():
    user_movies.loc[userId,movieId]=rating
    
#predicting rating based on user preferences
moviePrediction=user_movies.apply(lambda row: cFilter.predict(userId,row.name,r_ui=row.values.mean()).est,axis=1)
#recommendening movies
top=5
recommendedMovies=moviePrediction.sort_values(ascending=False)[:top].index
moviesTitles=movies[movies['movieId'].isin(recommendedMovies)]['title']
print(moviesTitles)
