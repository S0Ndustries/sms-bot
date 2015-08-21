import requests
#import json
def detect(imgURL):
	response = requests.get("https://faceplusplus-faceplusplus.p.mashape.com/detection/detect?attribute=glass%2Cpose%2Cgender%2Cage%2Crace%2Csmiling&url="+imgURL,
	  headers={
	    "X-Mashape-Key": "Kg2mHoXfzBmshhUtuPDK4xAxTsSOp1lQbBPjsnoAl4tW4TEw0s",
	    "Accept": "application/json"
	  }
	).json()
	agerange = response['face'][0]['attribute']['age']['range']
	agevalue = response['face'][0]['attribute']['age']['value']
	agestring = " You seem to be in the age range of %d to %d years. If I were to take a guess, you are %d years old."%((agevalue-agerange),(agevalue+agerange),agevalue)
	#print agestring
	gender = response['face'][0]['attribute']['gender']['value']
	genderc = response['face'][0]['attribute']['gender']['confidence']
	genderstring =  " I'm %f percent sure that you are a %s."%(genderc,gender)
	#print genderstring
	specs = response['face'][0]['attribute']['glass']['value']
	specsc = response['face'][0]['attribute']['glass']['confidence']
	specsstring = " I'm fairly certain (i.e. %f percent) that you are wearing"%(specsc)
	if specs == 'None':
		specsstring += ' no glasses.'
	elif specs == 'Dark':
		specsstring += ' sunglasses.'
	elif specs == 'Normal':
		specsstring += ' glasses.'
	#print specsstring
	#racev = response['face'][0]['race']['confidence']
	#race = response['face'][0]['race']['value']
	#racestring = " And based on my powers of perception, you seem to be %s"%(racev)
	#print racestring
	masterstring = "Oy! I am not just some stupid bot who can send SMSs. I can do way more. Here's an example of my supreme intelligence."+genderstring+agestring+specsstring#+racestring
	print masterstring
	return masterstring


if __name__ == '__main__':
    detect("http://www.npg.si.edu/exhibit/feature/images/schoeller_full.jpg")

# ADD LOGIC FOR MANY FACES IN THE IMAGE AND NO FACES. Check the parameters being passed in the GET request from the API    