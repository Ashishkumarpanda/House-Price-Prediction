import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler #for feature scalling
import tensorflow as tf

housing=pd.read_csv("house.csv")
housing.head()

#housing.describe().transpose()

x_data=housing.drop(['medianHouseValue'],axis=1)#drop the value to be predicted

y_val=housing['medianHouseValue']#the output

x_train, x_test, y_train, y_test = train_test_split(x_data, y_val, test_size=0.33, random_state=42)

scaler=MinMaxScaler()
scaler.fit(x_train) #performing featurescalling to train data

x_train=pd.DataFrame(data=scaler.transform(x_train),columns=x_train.columns,index=x_train.index) #covert train data into dataframe

x_test=pd.DataFrame(data=scaler.transform(x_test),columns=x_test.columns,index=x_test.index) #creating dataframe from testing data

housing.columns #all the colums of dataset

#converting all columns into numeric columns
age=tf.feature_column.numeric_column('housingMedianAge')
rooms=tf.feature_column.numeric_column('totalRooms')
bedrooms=tf.feature_column.numeric_column('totalBedrooms')
pop=tf.feature_column.numeric_column('population')
households=tf.feature_column.numeric_column('households')
income=tf.feature_column.numeric_column('medianIncome')

#creating a list containing all numeric colums
feat_col=[age,rooms,bedrooms,pop,households,income]

#input the data by help of estimator to train the data i.e. creating input function
input_func=tf.estimator.inputs.pandas_input_fn(x=x_train,y=y_train,batch_size=10,num_epochs=1000,shuffle=True)

#creating model using DNNREGRESSOR
model=tf.estimator.DNNRegressor(hidden_units=[6,6,6],feature_columns=feat_col)

#now train the model
model.train(input_fn=input_func,steps=25000)

#perform prediction by taking testing data as input
predict_input_func=tf.estimator.inputs.pandas_input_fn(x=x_test,batch_size=10,num_epochs=1,shuffle=False)

#predict and store the prediction value in list
predictions=list(model.predict(predict_input_func))

#converting the dictionary output into list
final_pred=[]
for pred in predictions:
  final_pred.append(pred['predictions'])
print(final_pred)

#calculating root mean square error
#it takes two arguments the actual ouput(y_test) and predicted output(final_pred)
#from sklearn.metrics import mean_squared_error
#mean_squared_error(y_test,final_pred)**0.5
