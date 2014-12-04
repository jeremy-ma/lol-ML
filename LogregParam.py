__author__ = 'Colin Feo'
import numpy as np
import sklearn as sk
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.utils import shuffle
from sklearn.grid_search import GridSearchCV
import time
from sklearn.linear_model import LogisticRegression

fX = open("X-1000-b.csv")
fY = open("Y-1000-b.csv")
dataX = np.loadtxt(fX,delimiter=',')
dataY = np.loadtxt(fY,delimiter=',')

X = dataX
y = dataY

time = time.time()
X = shuffle(X,random_state=int(time))
y = shuffle(y,random_state=int(time))
#preprocess data
X = StandardScaler().fit_transform(X)

#rforest = RandomForestClassifier(max_depth=4,n_estimators=100,max_features='auto',criterion="entropy",bootstrap="True",n_jobs=-1)
#rforest = RandomForestClassifier()
params = {'penalty':['l1', 'l2'], 'C': [x * 0.1 for x in xrange(1,200)]}
gSearch = GridSearchCV(LogisticRegression(),param_grid=params,cv=10)
gSearch.fit(X,y)
#gSearch.score(X,y)

print(str(gSearch.best_params_))
#print("RFOREST: " + str(np.mean(cross_val_score(rforest,X,y,cv=30))))
