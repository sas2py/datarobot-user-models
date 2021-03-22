

#%%
import pickle
import pandas as pd
from sas2py_runner import SAS2PYBaseEstimator


# %%
class _sas2py_model_scoring1(SAS2PYBaseEstimator):
    
    def predict(self, foo):
        def bar_func(row):
            row['score'] = (row['CRIM'] + row['ZN']) * row['TAX'] / row['LSTAT']
            return row

        bar = foo.apply(bar_func, axis=1)


        return bar['score']
    
#%%
df = pd.read_csv('/sas2py/app/workspace/drum/datarobot-user-models/tests/testdata/boston_housing_inference.csv')
df.head()
#%%
modelA = _sas2py_model_scoring1()
#%%
#%%
import dill
with open('sas_loader.pkl', 'wb') as handle:
    dill.dump(modelA, handle, protocol=pickle.HIGHEST_PROTOCOL)
#%%
with open('sas_loader.pkl', 'rb') as handle:
    modelA_loaded = dill.load(handle)
out = modelA_loaded.predict(df)

out.head()

# %%
out.dtypes
# %%
