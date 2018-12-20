import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.preprocessing import StandardScaler
import pickle

class Dataset:
    def __init__(self):
        self.dataset = pd.read_csv('data/survey.csv')
        
    def dataSelection(self, selectionString="2,1,3", extension="independent" ):     

        # get rid of leading columns
        dataset = self.dataset.iloc[1:,10:].values

        #breakup set
        selArray = selectionString.split(",")

        #change to set of integers (no repeats) in reverse order
        iSet = set()
        for i in selArray:
            iSet.add(int(i))
        length = len(dataset[0])  
        for i in reversed(range(0,length)):
           if i not in iSet:
            dataset = np.delete(dataset,i,1)
        print("LENGTH: ", len(dataset))
        #change categorical data to 1/0 columns
        labelencoder = LabelEncoder()
        catFeatures = {}
        for i in range(0, len(dataset[0])):
            try:
                #test to see if it is an integer
                int(dataset[:,i][0])
            # Not an integer
            except ValueError:
                #determine length
                if( len(set(dataset[:,i])) > 2):                
                    dataset[:,i] = labelencoder.fit_transform(dataset[:,i])
                    catFeatures.update({i:len(set(dataset[:,i]))})
                else:
                    dataset[:,i] = labelencoder.fit_transform(dataset[:,i]) 

        catFeaturesArray = []
        for key, value in catFeatures.items():
            catFeaturesArray.append(key)
            onehotencoder = OneHotEncoder(categorical_features = catFeaturesArray)
            dataset = onehotencoder.fit_transform(dataset).toarray()

        #must delete one column for each categorical data set
        delCol = 0
        for key, value in catFeatures.items():
            dataset = np.delete(dataset, delCol, 1)
            #adjusts for the disappearing column from above
            delCol += value -1

        # Must scale the data
        # Feature Scaling

        sc = StandardScaler()
        dataset = sc.fit_transform(dataset)
        
        # save scaler to later reverse transform
        filenameBase = 'data/ML' + extension
        
        filename = filenameBase + '.pkl'
        with open(filename, 'wb') as f:
            pickle.dump(sc, f, pickle.HIGHEST_PROTOCOL)

        #save data
        fileName = filenameBase +".npy"
        np.save(fileName, dataset)

        #datasetNew = np.load('data/MachineLine2.npy')

        #if( np.array_equal(dataset, datasetNew)):
            #message = "Exact Copy"
            #return dataset
        #else:
            #message = "Incorrect Data Copy"
        return dataset
            
      
#d = Dataset()
#datas = d.dataSelection(selectionString = '1')
