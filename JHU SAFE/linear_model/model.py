# %%
from scipy.io import loadmat, savemat
import torch
import torch.nn as nn
import torch.nn.functional as F
import seaborn as sns
import numpy as np
import torch.optim as optim
import seaborn as sns
from sklearn import metrics
from torch.utils.data.sampler import WeightedRandomSampler

#%%
class ordinal_regression(nn.Module):
    def __init__(self, ndim, ydim):
        super(ordinal_regression, self).__init__()
        self.w = nn.Linear(ndim, 1, bias=False)
        self.bias = nn.Parameter(torch.zeros((1, ydim)))
        self.ydim = ydim
   
    def forward(self, X):
        X = torch.tensor(X, dtype=torch.float32)
        y_hat = self.w(X)
        y_hat = F.sigmoid(y_hat.repeat(1,self.ydim) + self.bias)
        return y_hat
   
    def predict(self, X):
        X = torch.tensor(X, dtype=torch.float32)
        with torch.no_grad():
            y_hat = self.w(X)
            y_hat = F.sigmoid(y_hat.repeat(1,self.ydim) + self.bias)
            return y_hat.numpy()      
#%%
def training(model, X, y, samples_weight, max_iter):
    learning_rate = 0.0001
    epsilon = 1e-7
    criterion = torch.nn.BCELoss()
    opt_j     = optim.Adam(model.parameters(), lr=learning_rate)
    y_train = torch.Tensor(y)
    X_train = X
    loss_criterion = []
    loss_sparsity = []
    old_loss = 0
    for i in range(max_iter):
        opt_j.zero_grad() # Setting our stored gradients equal to zero
        sampler = list(WeightedRandomSampler(samples_weight, len(samples_weight), replacement = True))
        # X_data = X_train[sampler, :]
        # y_data = y_train[sampler]
        X_data = X_train
        y_data = y_train
        outputs = model(X_data)
        loss_c = criterion(outputs, y_data) 
        loss_criterion.append(loss_c.detach().item())
        loss = loss_c
        loss.backward() # Computes the gradient of the given tensor w.r.t. the weights/bias
        opt_j.step() # Updates weights and biases with the optimizer (SGD)
        if abs(old_loss - loss) < epsilon:
            break
        old_loss = loss.detach().item()
        
    return loss_criterion, loss_sparsity, model.w.weight.detach().numpy()

# %%
X_train = (loadmat('fold1.mat')['X_train'])
y_train = (loadmat('fold1.mat')['y_train']) 
X_test = (loadmat('fold1.mat')['X_test'])  
y_test = (loadmat('fold1.mat')['y_test'])
y_test = y_test.sum(axis = 1)
# %%
y_train_label = y_train.sum(axis = 1)
class_sample_count = np.array([len(np.where(y_train_label==t)[0]) for t in np.unique(y_train_label)])
weight = 1. / class_sample_count
samples_weight = np.array([weight[t] for t in y_train_label])
samples_weight = torch.from_numpy(samples_weight)

# %%
# training
model = ordinal_regression(X_train.shape[1], y_train.shape[1])
loss_c, loss_s,weights = training(model, X_train.astype('double'), y_train.astype('int16'), samples_weight,  10000)
importance = weights

# %%
with torch.no_grad():
    y_prob_fixed = model(torch.Tensor(X_test))
    #Y_hat = (cpu(y_j_hat).data.numpy()> ordinal_thres).cumprod(axis = 1).sum(axis = 1)
    y_te = (y_prob_fixed.detach().numpy() > 0.5).cumprod(axis = 1).sum(axis = 1)
    y_te[y_te < 0] = 0
    f1 = metrics.f1_score(y_test, y_te, average='macro')
    accuracy = metrics.accuracy_score(y_test, y_te)
    kappa = metrics.cohen_kappa_score(y_test, y_te)
    sensitivity = metrics.recall_score(y_test, y_te, average='macro')
    specs = []
    for i in range(1, 4):
        prec, recall,_, _ = metrics.precision_recall_fscore_support(y_test==i, y_te==i, pos_label=True, average=None)
        specs.append(recall[0])
    specificity = sum(specs)/len(specs)
    Y = y_test
    Y_PRED = y_te

# %%
sns.heatmap(metrics.confusion_matrix(Y, Y_PRED), annot = True)
# %%
sns.scatterplot(importance.ravel())
# %%
