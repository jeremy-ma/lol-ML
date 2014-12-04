__author__ = 'Colin Feo'
import numpy as np
import time
import sklearn as sk
import scipy as sp
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.ensemble import RandomTreesEmbedding
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import cross_val_score
from sklearn.utils import shuffle
from sklearn.neural_network import BernoulliRBM
from sklearn.lda import LDA
from sklearn.qda import QDA
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.linear_model import LogisticRegression, Perceptron, LinearRegression

#load data
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
#X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2)

#nearest neighbor
kneighbor = KNeighborsClassifier(n_neighbors=3)
#linear svm
lsvm = SVC(kernel="linear", C = 0.025)
#rbf svm
rsvm = SVC(gamma=2,C=0.025)
#decision tree
dtree = DecisionTreeClassifier(max_depth=7)
#random forest
rforest = RandomForestClassifier(max_depth=7,n_estimators=350,max_features='auto',criterion="entropy",bootstrap="True",n_jobs=-1)
#rforestemb = RandomTreesEmbedding(max_depth=5,n_estimators=150)
#nn = BernoulliRBM()
#NB
nb = GaussianNB()
#AdaBoost
adaboost = AdaBoostClassifier(rforest, algorithm="SAMME")
#qda = QDA()
#lda = LDA()

logreg = LogisticRegression(penalty='l1', C=0.1)

perceptron = Perceptron(penalty = 'l2')
linearreg = LinearRegression()

#gBoostClass = GradientBoostingClassifier(GradientBoostingClassifier(n_estimators=100, max_depth=1, random_state=0,loss='ls'))

print("KNEIGHBOR: " + str(np.mean(cross_val_score(kneighbor,X,y,cv=3))))
print("LSVM: " + str(np.mean(cross_val_score(lsvm,X,y,cv=3))))
print("RSVM: " + str(np.mean(cross_val_score(rsvm,X,y,cv=3))))
print("DTREE: " + str(np.mean(cross_val_score(dtree,X,y,cv=3))))
print("RFOREST: " + str(np.mean(cross_val_score(rforest,X,y,cv=3))))
#print("NN: " + str(np.mean(cross_val_score(nn,X,y,cv=10,scoring=accuracy_score))))
#print("RFORESTEMB: " + str(np.mean(cross_val_score(rforestemb,X,y,cv=10))))
print("ADABOOST: " + str(np.mean(cross_val_score(adaboost,X,y,cv=3))))
#print("NB: " + str(np.mean(cross_val_score(nb,X,y,cv=3))))
print("Logistic Regression: " + str(np.mean(cross_val_score(logreg,X,y,cv=3))))
print("Perceptron: " + str(np.mean(cross_val_score(perceptron,X,y,cv=3))))
print("LinearRegression: " + str(np.mean(cross_val_score(linearreg,X,y,cv=3))))
#print("GradBoost: " + str(np.mean(cross_val_score(gBoostClass,X,y,cv=3))))
#print("LDA: " + str(np.mean(cross_val_score(QDA,X,y,cv=10))))
#print("QDA: " + str(np.mean(cross_val_score(LDA,X,y,cv=10))))
#close file
fX.close()
fY.close()

