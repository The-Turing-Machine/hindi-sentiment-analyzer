from flask import Flask,render_template
import requests
import json

app=Flask(__name__)

@app.route("/")
def Faceook_Data_Extract():

	access_token = 'CAAIExyN1towBABpcpxhCeedfpIpFuIL5Jcj4yd5IqnOCEWJtyfdQVLtZBL4JavVxrnJvfkNS5JX90b1Q4pIJydNMsryJvQ5AvqwZAtZA9RABAZC2891kH2sj78wavRcB1teRDqssorZAQIO723GxeZAEZCxbNsJe0lSpaCaHZClughuXUbqXdOnhfNYlZAmM3AZCsZA8ByowOJMeNfgA1u1rfqV'      # The short lived access token obtained from https://developers.facebook.com/tools/accesstoken/

	app_id = "568203293341324"                      	       # Obtained from https://developers.facebook.com/   

	client_secret = "537b0a2c89c6de326a28f08a2c027db2"         # Obtained from https://developers.facebook.com/

	link = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=" + app_id +"&client_secret=" + client_secret + "&fb_exchange_token=" + access_token   #The link from where the long lived token will be generated

	#Generaing the long lived token
	try:
		s = requests.Session()
		token = s.get(link).content
		token = token.split("&")[0]                 # this strips out the expire info (now set set about 5184000 seconds, or 60 days)
		token = token.strip("access_token=")        # Strips out access token
	except:
		token = "568203293341324|iqOMvQ3OlQGX-6r75P-IxROAdoA" #Using the app_access_token in case user_access_token expires


	#Sending request to the initial page
	r1=requests.get("https://graph.facebook.com/v2.5/BBCHindi?fields=posts.limit(1){message,comments.limit(999)}", params={"access_token":token})

	#Creating a python object of the obtained json
	comments_page_1=json.loads(r1.text)

	#Dumping data into a file named as data.json
	with open("data.json","w") as outfile:
		json.dump(comments_page_1,outfile)

	#Extracting the url for the second batch of comments
	try:
		page_2_comments_link=comments_page_1["data"][0]["comments"]["paging"]["next"]
	except KeyError:
		pass

	#A function to recursively extract all the comments based according to pagination
	def recursive_extracting_comments(url):

		try:
			r2=requests.get(url, params={"access_token":token})
			comments=json.loads(r2.text)
			with open("data.json","a") as outfile:
				json.dump(comments,outfile)
			next_comment_link=comments["paging"]["next"]

			try:
				recursive_extracting_comments(next_comment_link)
			except KeyError:
				pass
		except KeyError:
			pass

	# recursive_extracting_comments(page_2_comments_link)
	try:
		recursive_extracting_comments(page_2_comments_link)
	except NameError:
		pass	

	return render_template('index.html',template_folder='templates')

if __name__ == '__main__' :
		app.run(debug=True)

