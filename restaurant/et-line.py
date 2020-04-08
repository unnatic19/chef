from flask import Flask,render_template,jsonify,request,abort,Response
import time
import sqlite3
import requests
import re
import csv
import datetime
import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel 
import math
from collections import Counter
############Find recommendations########################
ds = pd.read_csv("chef_102.csv")
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(ds['Ingredients'])


cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix) 
results = {}
for idx, row in ds.iterrows():
   similar_indices = cosine_similarities[idx].argsort()[:-100:-1] 
   similar_items = [(cosine_similarities[idx][i], ds['Ingredients'][i]) for i in similar_indices] 
   results[row['Ingredients']] = similar_items[1:]


def item(Ingredients):  
	lis=ds.loc[ds['Ingredients']==Ingredients][['Recipe_id','Recipe_name','Recipe_url','Recipe_image','Ingredients']].values.tolist()[0]
	lis[-1]=lis[-1].split("+")#####change it to , for book1
	return lis
def recommend(Ing, num):
	rec_book=[]
	#print("Recommending " + str(num) + " products similar to " + str(item(Ing)) + "...")   
	#print("-------")   
	recs = results[Ing][:num]   
	for rec in recs: 
		#print("Recommended: " + str(item(rec[1])) + " (score:" +      str(rec[0]) + ")")
		rec_book.append(item(rec[1]))
	return rec_book
########################################################
def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

con = sqlite3.connect("database.db")

cur=con.cursor()
con.execute("PRAGMA foreign_keys=ON")
cur.execute("CREATE TABLE IF NOT EXISTS users(User_id INTEGER PRIMARY KEY NOT NULL ,Username TEXT NOT NULL,Name TEXT NOT NULL,Password TEXT NOT NULL, Email TEXT NOT NULL,Phone INTEGER NOT NULL,Bookmark TEXT)")
#cur.execute("CREATE TABLE IF NOT EXISTS recipes(Recipe_id INT PRIMARY KEY NOT NULL, Recipe_name TEXT NOT NULL,Recipe_url TEXT NOT NULL,Ingredients TEXT NOT NULL,Recipe_image BLOB NOT NULL)")
con.commit()

app=Flask(__name__)

@app.route("/login",methods=["POST"])
def login():
	Username=request.get_json()['Username']
	Password=request.get_json()['Password']
	try:

		with sqlite3.connect("database.db") as con:
			cur=con.cursor()
			cur.execute("SELECT User_id FROM users WHERE Username='"+str(Username)+"' AND Password='"+str(Password)+"'")
			present_flag=cur.fetchone()[0]
			con.commit()
			if(present_flag!=None):
				return str(present_flag)
			else:
				return "User no present"
	except Exception as e:
		return "USER DOESNT EXIST"
@app.route("/signup",methods=["POST"])
def signup():
	Name=request.get_json()['Name']
	Username=request.get_json()['Username']
	Password=request.get_json()['Password']
	Email=request.get_json()['Email']
	Phone=request.get_json()['Phone']
	#User_id=2
	print(Name,Username,Password,Email,Phone)
	try:
		with sqlite3.connect("database.db") as con:
			cur=con.cursor()
			print(Name)
			cur.execute("INSERT INTO users(Username,Name,Password,Email,Phone) values (?,?,?,?,?)",(Username,Name,Password,Email,Phone))
			con.commit()
			return "success"
	except Exception as e:
		return e

@app.route("/bookmark",methods=["POST"])
def bookmark():
	Recipe_id=request.get_json()['Recipe_id']
	User_id=request.get_json()['User_id']
	try:
		with sqlite3.connect("database.db") as con:
			cur=con.cursor()
			
			cur.execute("SELECT Bookmark FROM users WHERE User_id="+str(User_id))

			rec_id=cur.fetchone()[0]
			if(rec_id==None):
				rec_id=[]
			else:
				rec_id=rec_id.split(',')
			
			if(str(Recipe_id) in rec_id):
				rec_id.remove(str(Recipe_id))
				rec_id_st=(",").join(rec_id)
				cur.execute("UPDATE users SET Bookmark='"+rec_id_st+"' WHERE User_id="+str(User_id ))
				con.commit()
				return "white"
			else:
				print(rec_id)
				rec_id.append(str(Recipe_id))
				if(rec_id[0]==""):
					rec_id=rec_id[1:]
				rec_id_st=(",").join(rec_id)
				print(rec_id_st)
				cur.execute("UPDATE users SET Bookmark='"+rec_id_st+"' WHERE User_id="+str(User_id))
				con.commit()
				return "pink"

	except Exception as e:
		return e
	

@app.route("/profile",methods=["GET","POST"])
def profile():
	User_id=request.get_json()['User_id']
	with sqlite3.connect("database.db") as con:
		cur=con.cursor()
		cur.execute("SELECT Username,Bookmark FROM users WHERE User_id="+str(User_id))
		cur_lis=list(cur.fetchone())
		print(cur_lis)
		usr_name=cur_lis[0]####
		bookmarks=cur_lis[1].split(',')
		print(bookmarks)
		all_rec=[]##########
		all_rec_bookmarks=[]
		for rec_id in bookmarks:
			rec_dets=ds.loc[ds['Recipe_id']==int(rec_id)][['Recipe_id','Recipe_name','Recipe_url','Recipe_image','Ingredients']].values.tolist()[0]
			ing_lis=rec_dets[-1]
			rec_dets[-1]=rec_dets[-1].split("+")####change it to , for book1
			all_rec.append(rec_dets)

			rec_for_bookmarks=recommend(Ing=ing_lis,num=5)
			all_rec_bookmarks.append(rec_for_bookmarks)

		random.shuffle(all_rec_bookmarks)
		all_rec_bookmarks_top_5=all_rec_bookmarks[:5]#####

		return jsonify(
			User_id=User_id,
			Username=usr_name,
			Bookmarks=all_rec,
			Recommendation=all_rec_bookmarks_top_5
			)

@app.route("/ingredients",methods=["POST"])
def ingredients():
	ingredients_str=request.get_json()['Ingredients']
	ingredients_lis=list(set(ingredients_str.split(',')))
	lis=ds.values.tolist()

	for row in lis:
		score=counter_cosine_similarity(Counter(ingredients_lis),Counter(row[-1].split('+')))#######change , to +
		row.append(score)

	rec_top_rec=lis[:15]

	return jsonify(
		Top_recommendations=rec_top_rec
		)



			




if __name__=="__main__":
	app.run(host="0.0.0.0",debug=True)