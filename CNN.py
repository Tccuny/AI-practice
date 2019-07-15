# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 10:18:50 2019

@author: dell
"""

# -*- coding: utf-8 -*-
"""

@author: zrf

@purpose:CarID-Classification
"""
import os
from PIL import Image
import torch
import torchvision
import torch.utils.data as data
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.optim as optim
import copy
import pickle
from torch.optim import lr_scheduler
'''
class  testSet(data.Dataset):
    def __init__(self,img_root,imagepathset,img_transform=None):
        super(testSet,self).__init__()
        self.img_root=img_root
        self.img_pathset=imagepathset
        self.img_transform=img_transform
        #self.imgfilenames=[join(img_root,x) for x in jsonlist]
    def __getitem__(self,index):
        img_path=os.path.join(self.img_root,self.img_pathset[index])
        img=Image.open(img_path)
        #print(img.size)
        #print(np.array(img).shape)
        if self.img_transform:
            img=self.img_transform(img)
        labelno=os.path.splitext(self.img_pathset[index])[0]
        #print(labelno)
        label=int(labelno.split('-')[0])-1
        #print(label)
        return img,label
        
    def __len__(self):
        return len(self.img_pathset)
'''        
        
img_root= '../trainset'
imgvalida_root='../testset'

transform_train=transforms.Compose([transforms.Resize(256),transforms.RandomCrop(224),transforms.RandomHorizontalFlip(),transforms.ToTensor(),transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])])
transform_test=transforms.Compose([transforms.Resize(256),transforms.CenterCrop(224),transforms.ToTensor(),transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])])
#dataset_sizes = {'train':len(jsonTrainSet),'val':len(jsonValidaSet)}

''' 加载训练集'''

trainset=ImageFolder(img_root,transform_train)
#print(trainset.class_to_idx)

''' 加载测试集'''
testset=ImageFolder(imgvalida_root,transform_test)
#imagepathset=[]
#for imagepath in os.listdir(imgvalida_root):
#    #imagepath=os.path.join(imgvalida_root,imagepath)
#    imagepathset.append(imagepath)
    
#testset=testSet(imgvalida_root,imagepathset,transform_test)

trainloader=torch.utils.data.DataLoader(trainset,batch_size=16,shuffle=True)
testloader=torch.utils.data.DataLoader(testset,batch_size=32,shuffle=False)

print(len(trainset))
print(len(testset))

dataset_sizes={'train':len(trainset),'val':len(testset)}  
#model=Net()
#param=list(model.parameters())
#print(param)

''' 加载模型'''

#model=torchvision.models.resnet50()
model=torchvision.models.vgg16()
model.load_state_dict(torch.load('vgg16-397923af.pth'))
#model.load_state_dict(torch.load('resnet50-19c8e357.pth'))
#num_ftrs=model.fc.in_features
#model.fc=nn.Linear(num_ftrs,65)
model.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096,65),
        )
#model=torch.load("../model/modelAll2_2.pkl")
model=model.cuda()
criterion=nn.CrossEntropyLoss()
optimizer=optim.SGD(model.parameters(),lr=0.0015,momentum=0.9)
model.train(mode=True)
best_acc=0.0
num_epochs=10
#device=0
acclist=[]
losslist=[]
scheduler=lr_scheduler.StepLR(optimizer,step_size=3,gamma=0.1)
for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 30)

        
        for phase in ['train','val']:
            if phase == 'train':
                #scheduler.step()
                model.train()  
            else:
                model.eval()   

            running_loss = 0.0
            running_corrects = 0
            if phase=='train':
                 dataloaders=trainloader
            else:
                 dataloaders=testloader
           
            for inputs, labels in dataloaders:
               # inputs = inputs.to(device)
               # labels = labels.to(device)
                #labels=dataU.getLabel(labels)
                inputs=inputs.cuda()
                labels=labels.cuda()
                inputs,labels=Variable(inputs),Variable(labels)
                #print(labels)
             
                optimizer.zero_grad()

             
                
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)
                    if phase=='val':
                       pass#print(preds)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()
 
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]
            losslist.append(epoch_loss)
            acclist.append(epoch_acc)
            

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))
            #model.load_state_dict(model.state.dict())
            torch.save(model,"../model/model"+str(epoch)+"_res50.pkl")
            # deep copy the model
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())
with open ("../result/acc-vgg16.pkl","wb") as f:
    pickle.dump(acclist,f)
with open("../result/loss-vgg16.pkl","wb") as f:
    pickle.dump(losslist,f)
print('Best val Acc: {:4f}'.format(best_acc))
#model.load_state_dict(best_model_wts)
#torch.save(model,"../model/model-best_res50.pkl")
                                                                           
