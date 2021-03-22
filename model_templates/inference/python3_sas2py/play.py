#%%
import pickle 

sas2py_model = {'framework': 'sas2py'}

#%%
with open('sas_loader.pkl', 'wb') as handle:
    pickle.dump(sas2py_model, handle, protocol=pickle.HIGHEST_PROTOCOL)

# %%
with open('sas_loader.pkl', 'rb') as handle:
    b = pickle.load(handle)

b
# %%
