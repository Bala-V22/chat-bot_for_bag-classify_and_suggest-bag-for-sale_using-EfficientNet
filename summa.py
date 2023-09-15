from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import cv2
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# model=load_model('classifier-chatbot-97.35.h5')
# img=image.load_img('./sample img/backbag1.jpg',target_size=(224,224))
# cv2.imshow(img)


def predictor(sdir, csv_path,  model_path, crop_image = False):    
    # read in the csv file
    class_df=pd.read_csv(csv_path)    
    img_height=int(class_df['height'].iloc[0])
    img_width =int(class_df['width'].iloc[0])
    img_size=(img_width, img_height)
    scale=class_df['scale by'].iloc[0] 
    try: 
        s=int(scale)
        s2=1
        s1=0
    except:
        split=scale.split('-')
        s1=float(split[1])
        s2=float(split[0].split('*')[1]) 
        print (s1,s2)
    path_list=[]
    paths=os.listdir(sdir)
    for f in paths:
        path_list.append(os.path.join(sdir,f))
    print (' Model is being loaded- this will take about 10 seconds')
    model=load_model(model_path)
    image_count=len(path_list)    
    index_list=[] 
    prob_list=[]
    cropped_image_list=[]
    good_image_count=0
    for i in range (image_count):       
        img=cv2.imread(path_list[i])
        if crop_image == True:
            status, img=crop(img)
        else:
            status=True
        if status== True:
            good_image_count +=1
            img=cv2.resize(img, img_size)            
            cropped_image_list.append(img)
            img=img*s2 - s1
            img=np.expand_dims(img, axis=0)
            p= np.squeeze (model.predict(img))           
            index=np.argmax(p)            
            prob=p[index]
            index_list.append(index)
            prob_list.append(prob)
    if good_image_count==1:
        class_name= class_df['class'].iloc[index_list[0]]
        probability= prob_list[0]
        img=cropped_image_list [0] 
        plt.title(class_name, color='blue', fontsize=16)
        plt.axis('off')
        plt.imshow(img)
        return class_name, probability
    elif good_image_count == 0:
        return None, None
    most=0
    for i in range (len(index_list)-1):
        key= index_list[i]
        keycount=0
        for j in range (i+1, len(index_list)):
            nkey= index_list[j]            
            if nkey == key:
                keycount +=1                
        if keycount> most:
            most=keycount
            isave=i             
    best_index=index_list[isave]    
    psum=0
    bestsum=0
    for i in range (len(index_list)):
        psum += prob_list[i]
        if index_list[i]==best_index:
            bestsum += prob_list[i]  
    img= cropped_image_list[isave]/255    
    class_name=class_df['class'].iloc[best_index]
    plt.title(class_name, color='blue', fontsize=16)
    plt.axis('off')
    plt.imshow(img)
    return class_name, bestsum/image_count


def main(file):
    store_path="./storage"
    # if os.path.isdir(store_path):
    #     shutil.rmtree(store_path)
    # os.mkdir(store_path)
    # input an image of a melanoma
    print("---------------------------passed pic name" , file)
    # img_path='static/{}'.format(file)
    img_path=file
    print(img_path)
    img=cv2.imread(img_path,  cv2.IMREAD_REDUCED_COLOR_2)
    img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # model was trained on rgb images so convert image to rgb
    file_name=os.path.split(img_path)[1]
    dst_path=os.path.join(store_path, file_name)
    cv2.imwrite(dst_path, img)
    # check if the directory was created and image stored
    print (os.listdir(store_path))

    csv_path="class_dict.csv" # path to class_dict.csv
    # model_path=model_save_loc # path to the trained model
    model_path="classifier-chatbot-97.35.h5"
    class_name,probability=predictor(store_path, csv_path,  model_path, crop_image = False) # run the classifier
    # msg=f' image is of class {class_name} with a probability of {probability * 100: 6.2f} %'
    # msg="this is the answer"
    # cv2.imshow(msg, (0,255,255), (65,85,55))
    print(class_name)
    return class_name

file=r'C:\Users\User\Desktop\bag\sample img\backbag1.jpg'
main(file)