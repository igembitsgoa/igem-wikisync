# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import esprima


# %%
esprima.tokenize


# %%
with open('dist/js/index.js', 'r') as file:
    contents = file.read()


# %%
contents


# %%
parsed = esprima.parseScript(contents)


# %%
print(parsed)


# %%


