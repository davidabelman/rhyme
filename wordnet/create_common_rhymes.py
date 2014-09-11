#!/usr/bin/env python
#coding: utf8 

"""
Creates list of common rhyming words according to online list
Saves list [of, words] as a pickle (created/common_rhyming_words.p)
"""

from general_functions import save_pickle

online_to_parse = [
{"Band":"2Pac","W1":"Me/See","W2":"Be/Me","W3":"Down/Now","W4":"Baby/Me","W5":"Do/You","Q1":"Combat/That","Q2":"Go/Through","Q3":"Me/See","Q4":"Better/Together","Q5":"Be/Me"},
{"Band":"ABBA","W1":"Go/Know","W2":"Free/Me","W3":"Through/You","W4":"Through/You","W5":"Say/Way","Q1":"Light/Night","Q2":"Through/You","Q3":"Strong/Wrong","Q4":"Stay/Way","Q5":"Smile/While"},
{"Band":"AC/DC","W1":"Do/You","W2":"Around/Down","W3":"Night/Right","W4":"Be/Me","W5":"Play/Way","Q1":"Make/Take","Q2":"True/You","Q3":"Round/Sound","Q4":"Play/Say","Q5":"One/Son"},
{"Band":"Adele","W1":"Do/You","W2":"Mind/Time","W3":"Knew/You","W4":"Flies/Lives","W5":"Behind/Find","Q1":"Flies/Lives","Q2":"Days/Haze","Q3":"Behind/Find","Q4":"Instead/Said","Q5":"Knew/You"},
{"Band":"Aerosmith","W1":"Do/You","W2":"True/You","W3":"Night/Right","W4":"Sky/Why","W5":"Lady/Me","Q1":"Sky/Why","Q2":"Me/See","Q3":"Lady/Me","Q4":"Go/So","Q5":"Girl/World"},
{"Band":"Alabama","W1":"Be/Me","W2":"Night/Right","W3":"Light/Night","W4":"Line/Time","W5":"Day/Way","Q1":"Around/Town","Q2":"Light/Night","Q3":"Know/So","Q4":"Down/Town","Q5":"Bed/Head"},
{"Band":"Andrea Bocelli","W1":"Light/Night","W2":"Go/Know","W3":"Above/Love","W4":"Find/Kind","W5":"Me/Tree","Q1":"Above/Love","Q2":"Say/Yesterday","Q3":"Find/Kind","Q4":"Go/Know","Q5":"Me/Tree"},
{"Band":"Aretha Franklin","W1":"Do/You","W2":"Be/Me","W3":"Me/See","W4":"True/You","W5":"Mine/Time","Q1":"Blind/Time","Q2":"Know/So","Q3":"Care/There","Q4":"Care/There","Q5":"Alone/Home"},
{"Band":"Backstreet Boys","W1":"Go/Know","W2":"Be/Me","W3":"True/You","W4":"Say/Way","W5":"Baby/Me","Q1":"Heartache/Mistake","Q2":"Desire/Fire","Q3":"Long/Wrong","Q4":"Before/More","Q5":"Away/Stay"},
{"Band":"Barbra Streisand","W1":"Be/Me","W2":"Do/You","W3":"True/You","W4":"Go/Know","W5":"Say/Way","Q1":"Be/Tree","Q2":"Again/When","Q3":"For/More","Q4":"Through/You","Q5":"Be/Me"},
{"Band":"Barry Manilow","W1":"Be/Me","W2":"Do/You","W3":"Me/See","W4":"True/You","W5":"Night/Right","Q1":"Clear/Years","Q2":"Love/Of","Q3":"Down/Town","Q4":"Days/Ways","Q5":"Bright/Night"},
{"Band":"Barry White","W1":"Do/You","W2":"Baby/Me","W3":"Mind/Time","W4":"To/You","W5":"Knew/You","Q1":"To/You","Q2":"Lie/Try","Q3":"Knew/You","Q4":"Mind/Time","Q5":"Day/Way"},
{"Band":"Bee Gees","W1":"Mind/Time","W2":"Do/You","W3":"Me/See","W4":"Be/Me","W5":"Through/You","Q1":"True/You","Q2":"Die/I","Q3":"Say/Way","Q4":"Night/Tight","Q5":""},
{"Band":"Beyoncé","W1":"Be/Me","W2":"Me/See","W3":"Do/You","W4":"Baby/Me","W5":"Mind/Time","Q1":"Talkin/Walkin","Q2":"Never/Together","Q3":"No/Oh","Q4":"Face/Grace","Q5":"Be/Me"},
{"Band":"Billy Joel","W1":"Be/Me","W2":"Do/You","W3":"Me/See","W4":"Long/Wrong","W5":"Light/Night","Q1":"Late/Wait","Q2":"Am/Man","Q3":"Right/Tonight","Q4":"Light/Night","Q5":"Fine/Mine"},
{"Band":"Blake Shelton","W1":"Mind/Time","W2":"Around/Down","W3":"To/You","W4":"Night/Right","W5":"Light/Night","Q1":"Me/See","Q2":"Down/Round","Q3":"Bed/Head","Q4":"Night/Right","Q5":"Away/Day"},
{"Band":"Bob Dylan","W1":"Do/You","W2":"Me/See","W3":"Away/Day","W4":"Gone/On","W5":"Long/Wrong","Q1":"Long/Wrong","Q2":"Dawn/Gone","Q3":"Down/Ground","Q4":"Pain/Rain","Q5":"Pay/Say"},
{"Band":"Bob Marley","W1":"Be/Me","W2":"Do/You","W3":"Do/Through","W4":"To/You","W5":"Through/You","Q1":"Again/Friend","Q2":"Too/You","Q3":"One/Son","Q4":"Mind/Time","Q5":"Blue/Do"},
{"Band":"Bon Jovi","W1":"Do/You","W2":"Me/See","W3":"True/You","W4":"Down/Ground","W5":"To/You","Q1":"Say/Way","Q2":"Fight/Tight","Q3":"Eye/Goodbye","Q4":"Alone/Stone","Q5":"Through/You"},
{"Band":"Britney Spears","W1":"Do/You","W2":"Me/See","W3":"True/You","W4":"Baby/Me","W5":"Around/Down","Q1":"Face/Place","Q2":"Cheek/Weak","Q3":"Floor/More","Q4":"Me/See","Q5":"Floor/More"},
{"Band":"Bruce Springsteen","W1":"To/You","W2":"Girl/World","W3":"Me/See","W4":"Night/Wife","W5":"Name/Shame","Q1":"Girl/World","Q2":"Face/Place","Q3":"Me/See","Q4":"Line/Time","Q5":"Face/Place"},
{"Band":"Bruno Mars","W1":"Mind/Time","W2":"True/You","W3":"Be/See","W4":"Smile/While","W5":"Love/Us","Q1":"Be/See","Q2":"Away/Way","Q3":"Smile/While","Q4":"Long/Wrong","Q5":"Gone/Wrong"},
{"Band":"Bryan Adams","W1":"True/You","W2":"Be/Me","W3":"Right/Night","W4":"Say/Way","W5":"Me/See","Q1":"Down/Round","Q2":"Me/See","Q3":"Day/Way","Q4":"True/You","Q5":"Alone/Home"},
{"Band":"Carrie Underwood","W1":"Be/Me","W2":"Gone/On","W3":"To/You","W4":"Down/Ground","W5":"Away/Say","Q1":"Down/Ground","Q2":"Gone/On","Q3":"Cool/Fool","Q4":"Belong/Strong","Q5":"High/Sky"},
{"Band":"Celine Dion","W1":"Do/You","W2":"Be/Me","W3":"Day/Way","W4":"True/You","W5":"Go/Know","Q1":"Pain/Vain","Q2":"Grace/Place","Q3":"Far/Stars","Q4":"Day/Way","Q5":"Do/You"},
{"Band":"Cher","W1":"Be/Me","W2":"Me/See","W3":"True/You","W4":"Baby/Me","W5":"Night/Right","Q1":"Around/Down","Q2":"Me/Sea","Q3":"Mind/Time","Q4":"Me/Sea","Q5":"Inside/Price"},
{"Band":"Chicago","W1":"Be/Me","W2":"Do/You","W3":"Light/Night","W4":"Go/Know","W5":"Day/Way","Q1":"Long/Wrong","Q2":"Go/Know","Q3":"Fine/Time","Q4":"Before/More","Q5":"Away/Stay"},
{"Band":"Def Leppard","W1":"True/You","W2":"Free/Me","W3":"Night/Right","W4":"Go/Show","W5":"Mind/Time","Q1":"Say/Way","Q2":"Night/Right","Q3":"Eyes/Surprise","Q4":"Door/For","Q5":"Care/There"},
{"Band":"Depeche Mode","W1":"Me/See","W2":"Do/You","W3":"Mind/Time","W4":"Above/Love","W5":"Hand/Understand","Q1":"Mind/Time","Q2":"Forver/Together","Q3":"Arms/Harm","Q4":"Above/Love","Q5":"Me/See"},
{"Band":"Dire Straits","W1":"Down/Town","W2":"Do/You","W3":"Blues/Shoes","W4":"Around/Down","W5":"Strong/Wrong","Q1":"Delight/Tonight","Q2":"Blues/Shoes","Q3":"Away/Day","Q4":"Home/Stone","Q5":"Around/Down"},
{"Band":"Donna Summer","W1":"Be/Me","W2":"True/You","W3":"Free/Me","W4":"Go/Know","W5":"Mind/Time","Q1":"True/You","Q2":"More/Shore","Q3":"Hand/Understand","Q4":"Home/Own","Q5":"Free/Me"},
{"Band":"Drake","W1":"Do/You","W2":"It/Shit","W3":"Be/Me","W4":"To/You","W5":"Go/Know","Q1":"It/Shit","Q2":"Go/Know","Q3":"Ego/Hero","Q4":"Call/Mall","Q5":"Mine/Time"},
{"Band":"Eagles","W1":"Down/Town","W2":"Be/Me","W3":"True/You","W4":"To/You","W5":"Down/Round","Q1":"Go/Know","Q2":"Down/Round","Q3":"Sign/Time","Q4":"To/You","Q5":"Mine/Time"},
{"Band":"Elivs","W1":"Do/You","W2":"Be/Me","W3":"True/You","W4":"Through/You","W5":"Me/See","Q1":"Gone/Song","Q2":"Door/More","Q3":"Do/True","Q4":"Along/Song","Q5":"View/You"},
{"Band":"Elton John","W1":"Do/You","W2":"Me/See","W3":"Say/Way","W4":"Light/Night","W5":"Mind/Time","Q1":"Dark/Heart","Q2":"All/Fall","Q3":"View/You","Q4":"Sky/Why","Q5":"Hand/Understand"},
{"Band":"Eminem","W1":"Me/See","W2":"Be/Me","W3":"Back/That","W4":"Through/You","W5":"Rap/That","Q1":"It/Spit","Q2":"Off/Soft","Q3":"House/Shout","Q4":"Broke/Smoke","Q5":"Night/Shit"},
{"Band":"Fleetwood Mac","W1":"Around/Down","W2":"Be/Me","W3":"Go/Know","W4":"Mine/Time","W5":"Away/Day","Q1":"Ago/Know","Q2":"Line/Time","Q3":"Tears/Years","Q4":"Line/Time","Q5":"Go/Know"},
{"Band":"Florida Georgia Line","W1":"Mine/Time","W2":"Down/Town","W3":"Clock/Rock","W4":"Baby/Me","W5":"Around/Town","Q1":"Mine/Time","Q2":"Clock/Rock","Q3":"Down/Town","Q4":"Around/Down","Q5":"Down/Town"},
{"Band":"Foreigner","W1":"Day/Way","W2":"Do/You","W3":"Be/Me","W4":"Night/Right","W5":"Apart/Heart","Q1":"Night/Right","Q2":"Line/Time","Q3":"Find/Mind","Q4":"Day/Way","Q5":"Light/Tonight"},
{"Band":"Frank Sinatra","W1":"Me/See","W2":"Go/Know","W3":"Away/Day","W4":"Away/Day","W5":"Two/You","Q1":"Talk/Walk","Q2":"Storm/Warm","Q3":"One/Sun","Q4":"Floor/More","Q5":"Eyes/Skies"},
{"Band":"Garth Brooks","W1":"True/You","W2":"Me/See","W3":"Be/Me","W4":"Be/Me","W5":"About/Out","Q1":"About/Out","Q2":"Name/Same","Q3":"Mind/Time","Q4":"Line/Time","Q5":"Away/Today"},
{"Band":"Genesis","W1":"Be/Me","W2":"Do/You","W3":"Me/See","W4":"Night/Right","W5":"True/You","Q1":"Door/Floor","Q2":"Me/See","Q3":"Know/Show","Q4":"Know/Show","Q5":"Here/There"},
{"Band":"George Michael","W1":"Be/Me","W2":"Me/See","W3":"Free/Me","W4":"Do/You","W5":"Face/Place","Q1":"Be/Free","Q2":"Find/Mind","Q3":"Face/Place","Q4":"Don’T/Won'T","Q5":"Bed/Head"},
{"Band":"Gloria Estefan","W1":"Do/You","W2":"True/You","W3":"Free/Me","W4":"Me/See","W5":"Away/Day","Q1":"True/You","Q2":"Right/Tight","Q3":"Too/You","Q4":"Go/Know","Q5":"Game/Same"},
{"Band":"Green Day","W1":"Love/Of","W2":"Me/See","W3":"Lights/Tonight","W4":"Go/Show","W5":"Down/Ground","Q1":"Love/Of","Q2":"Fast/Last","Q3":"Crime/Time","Q4":"Control/Soul","Q5":"Me/See"},
{"Band":"Guns N' Roses","W1":"True/You","W2":"Do/You","W3":"Me/See","W4":"Do/True","W5":"Through/You","Q1":"Blame/Name","Q2":"Along/On","Q3":"Smile/While","Q4":"Sky/Try","Q5":"True/You"},
{"Band":"Imagine Dragons","W1":"To/You","W2":"Down/Town","W3":"Do/You","W4":"Be/Me","W5":"All/Call","Q1":"To/You","Q2":"Down/Town","Q3":"All/Call","Q4":"Be/Me","Q5":"Do/You"},
{"Band":"Jason Aldean","W1":"Go/Slow","W2":"Do/You","W3":"To/You","W4":"Now/Town","W5":"Me/See","Q1":"Gone/On","Q2":"Fast/Last","Q3":"Down/Round","Q4":"Around/Sound","Q5":"Alright/Night"},
{"Band":"Jay Z","W1":"Be/Me","W2":"Do/You","W3":"At/That","W4":"Me/See","W5":"One/Son","Q1":"Know/Low","Q2":"Em/Women","Q3":"Dumb/One","Q4":"Real/Squeal","Q5":"Insane/Same"},
{"Band":"Journey","W1":"Do/You","W2":"Away/Day","W3":"Me/See","W4":"True/You","W5":"Light/Night","Q1":"For/More","Q2":"Day/Way","Q3":"Care/There","Q4":"Before/Door","Q5":"Alone/Home"},
{"Band":"Julio Iglesias","W1":"Do/You","W2":"Amor/Ayer","W3":"True/You","W4":"Too/You","W5":"Say/Way","Q1":"Amor/Ayer","Q2":"True/You","Q3":"Son/One","Q4":"Pure/Sure","Q5":"Need/Read"},
{"Band":"Justin Bieber","W1":"Do/You","W2":"Be/Me","W3":"Baby/Me","W4":"Go/Know","W5":"Enough/Love","Q1":"Enough/Love","Q2":"Dear/Here","Q3":"Find/Time","Q4":"Find/Time","Q5":"Do/You"},
{"Band":"Justin Timberlake","W1":"Me/See","W2":"Do/You","W3":"Be/Me","W4":"Through/You","W5":"Right/Tonight","Q1":"Alone/Phone","Q2":"Right/Tonight","Q3":"Name/Same","Q4":"Man/Understand","Q5":"Away/Way"},
{"Band":"Kanye West","W1":"Do/You","W2":"Go/Know","W3":"Night/Right","W4":"Through/You","W5":"To/You","Q1":"Right/Tonight","Q2":"Ball/Mall","Q3":"Mine/Shine","Q4":"One/Sun","Q5":"Lying/Trying"},
{"Band":"Kenny Rogers","W1":"Do/You","W2":"Be/Me","W3":"Me/See","W4":"Mind/Time","W5":"Too/You","Q1":"Sorrow/Tomorrow","Q2":"Right/Tonight","Q3":"Man/Understand","Q4":"Door/Floor","Q5":"Bed/Head"},
{"Band":"Kiss","W1":"Me/See","W2":"Through/You","W3":"Away/Say","W4":"Alone/Own","W5":"Say/Way","Q1":"Mind/Time","Q2":"Do/Through","Q3":"Control/Roll","Q4":"Away/Say","Q5":"Got/Hot"},
{"Band":"Lady Antebellum","W1":"Do/You","W2":"Be/Me","W3":"Through/You","W4":"Say/Stay","W5":"Mine/Time","Q1":"Away/Day","Q2":"Me/Tree","Q3":"Mine/Time","Q4":"Through/You","Q5":"Do/You"},
{"Band":"Lady Gaga","W1":"Me/See","W2":"Baby/Me","W3":"Girl/World","W4":"Around/Down","W5":"Night/Tonight","Q1":"Regret/Set","Q2":"Forever/Together","Q3":"Truth/Youth","Q4":"Cupid/Stupid","Q5":"Truth/Youth"},
{"Band":"Led Zeppelin","W1":"Baby/Me","W2":"Know/So","W3":"Away/Day","W4":"Know/So","W5":"Insane/Same","Q1":"Know/So","Q2":"Me/Sea","Q3":"Child/While","Q4":"Know/Soul","Q5":"Me/Sea"},
{"Band":"Lil Wayne","W1":"Baby/Me","W2":"Me/Money","W3":"Be/Me","W4":"Me/See","W5":"Do/You","Q1":"Me/Money","Q2":"Shit/It","Q3":"Me/Free","Q4":"Me/Free","Q5":"Dog/Long"},
{"Band":"Linda Ronstadt","W1":"Do/You","W2":"Through/You","W3":"True/You","W4":"Me/See","W5":"Go/Know","Q1":"Through/True","Q2":"One/Sun","Q3":"Hand/Understand","Q4":"Face/Place","Q5":"Dreaming/Scheming"},
{"Band":"Lionel Richie","W1":"Do/You","W2":"True/You","W3":"Me/See","W4":"Through/You","W5":"Go/Know","Q1":"Through/You","Q2":"Say/Way","Q3":"Learn/Turn","Q4":"Down/Round","Q5":"Doubt/Out"},
{"Band":"Luke Bryan","W1":"Gone/On","W2":"Be/Me","W3":"On/Song","W4":"Me/See","W5":"Kiss/This","Q1":"On/Song","Q2":"Be/Me","Q3":"Home/Phone","Q4":"Kiss/This","Q5":"Along/Song"},
{"Band":"Madonna","W1":"Do/You","W2":"Signs/Time","W3":"Game/Same","W4":"Far/Star","W5":"End/Pretend","Q1":"Do/You","Q2":"True/You","Q3":"Girl/World","Q4":"Free/Me","Q5":"Too/You"},
{"Band":"Meat Loaf","W1":"Do/You","W2":"True/You","W3":"Go/Know","W4":"Alone/Home","W5":"Do/True","Q1":"Say/Today","Q2":"Line/Time","Q3":"Be/Me","Q4":"Baby/Me","Q5":"All/Fall"},
{"Band":"Metallica","W1":"Line/Time","W2":"Me/See","W3":"Feel/Real","W4":"Eyes/Lies","W5":"Through/You","Q1":"Feel/Real","Q2":"Done/Run","Q3":"Cry/Die","Q4":"Mine/Time","Q5":"Done/Gone"},
{"Band":"Michael Jackson","W1":"Baby/Me","W2":"Me/See","W3":"Do/You","W4":"Be/Me","W5":"Through/You","Q1":"Love/Of","Q2":"Down/Sounds","Q3":"Storm/Warm","Q4":"Mind/Nine","Q5":"Through/You"},
{"Band":"Mötley Crüe","W1":"Go/Show","W2":"Back/Black","W3":"True/You","W4":"Dead/Head","W5":"Dream/Scream","Q1":"Back/Black","Q2":"Dead/Head","Q3":"Dream/Scream","Q4":"Sorrow/Tomorrow","Q5":"Sight/Tonight"},
{"Band":"Neil Diamond","W1":"Be/Me","W2":"Do/You","W3":"Day/Way","W4":"Go/Know","W5":"Around/Down","Q1":"Away/Stay","Q2":"Stay/Way","Q3":"Nowhere/There","Q4":"Mine/Time","Q5":"Meet/Street"},
{"Band":"New Kids on the Block","W1":"Do/You","W2":"Girl/World","W3":"Mind/Time","W4":"True/You","W5":"Baby/Me","Q1":"Do/Through","Q2":"Rough/Tough","Q3":"Mind/Time","Q4":"Girl/World","Q5":"True/You"},
{"Band":"Nirvana","W1":"Too/You","W2":"Myself/Yourself","W3":"Mind/Mine","W4":"Down/Town","W5":"True/You","Q1":"Dead/Head","Q2":"Die/Sky","Q3":"Mind/Mine","Q4":"Reason/Season","Q5":"Mind/Mine"},
{"Band":"Olivia Newton-John","W1":"Do/You","W2":"Be/Me","W3":"Me/See","W4":"Go/Know","W5":"Away/Day","Q1":"Might/Right","Q2":"Through/You","Q3":"Hide/Inside","Q4":"Hand/Sand","Q5":"Grow/Know"},
{"Band":"One Directoin","W1":"Do/You","W2":"To/You","W3":"Forever/Together","W4":"Kiss/This","W5":"Bed/Said","Q1":"Kiss/This","Q2":"Long/On","Q3":"Bed/Said","Q4":"Sun/Young","Q5":"Polo/Solo"},
{"Band":"Paul McCartney","W1":"Me/See","W2":"Be/Me","W3":"Day/Way","W4":"Line/Time","W5":"Door/More","Q1":"Mine/Shine","Q2":"Man/Understand","Q3":"Hide/Inside","Q4":"Fight/Night","Q5":"Door/For"},
{"Band":"Phil Collins","W1":"True/You","W2":"Say/Way","W3":"Go/Know","W4":"Before/Moer","W5":"To/You","Q1":"Everywhere/There","Q2":"How/Now","Q3":"Anyway/Say","Q4":"Smile/While","Q5":"True/You"},
{"Band":"Pink Floyd","W1":"Say/Way","W2":"Home/Phone","W3":"Child/Wild","W4":"Light/Night","W5":"Do/You","Q1":"Home/Phone","Q2":"Child/Wild","Q3":"Sides/Tide","Q4":"Say/Today","Q5":"Light/Night"},
{"Band":"Prince","W1":"Do/You","W2":"Me/See","W3":"Mind/Time","W4":"Girl/World","W5":"Around/Down","Q1":"Door/Yours","Q2":"Shy/Sky","Q3":"Ring/Sing","Q4":"Game/Same","Q5":"Fantasy/Me"},
{"Band":"Queen","W1":"Night/Right","W2":"Day/Way","W3":"Be/See","W4":"Style/While","W5":"Say/Way","Q1":"Band/Land","Q2":"Style/While","Q3":"Say/Way","Q4":"Pleasure/Treasure","Q5":"Disgrace/Place"},
{"Band":"R.E.M.","W1":"Around/Down","W2":"Do/You","W3":"Me/Sea","W4":"Day/Way","W5":"Away/Stay","Q1":"Eyes/Sky","Q2":"Blue/You","Q3":"Fun/Run","Q4":"Around/Down","Q5":"Me/Sea"},
{"Band":"Reba McEntire","W1":"True/You","W2":"Be/Me","W3":"Through/You","W4":"Me/See","W5":"Mind/Time","Q1":"Hand/Man","Q2":"Again/Friend","Q3":"High/Sky","Q4":"Too/True","Q5":"Pain/Rain"},
{"Band":"Red Hot Chili Peppers","W1":"Go/Know","W2":"Me/See","W3":"Free/Me","W4":"Away/Day","W5":"Through/You","Q1":"Stay/Way","Q2":"Care/There","Q3":"Away/Hey","Q4":"Fun/One","Q5":"For/Store"},
{"Band":"Rihanna","W1":"Be/Me","W2":"Me/See","W3":"Mind/Time","W4":"Do/You","W5":"Baby/Me","Q1":"More/Pour","Q2":"Naughty/Party","Q3":"Longer/Stronger","Q4":"Do/Knew","Q5":"Tell/Well"},
{"Band":"Rod Stewart","W1":"Do/You","W2":"Be/Me","W3":"Me/See","W4":"True/You","W5":"Baby/Me","Q1":"Enough/Tough","Q2":"Again/Friends","Q3":"Two/You","Q4":"Style/While","Q5":"Pain/Rain"},
{"Band":"Sade","W1":"Do/You","W2":"Say/Way","W3":"Go/Know","W4":"Day/Stay","W5":"Above/Love","Q1":"Playing/Staying","Q2":"Ago/Go","Q3":"Life/Side","Q4":"How/Now","Q5":"Gun/One"},
{"Band":"Santana","W1":"Me/See","W2":"Do/You","W3":"Be/Me","W4":"Me/Sea","W5":"Go/Know","Q1":"Light/Night","Q2":"Me/See","Q3":"True/You","Q4":"Do/You","Q5":"True/You"},
{"Band":"Scorpions","W1":"Away/Day","W2":"Blue/You","W3":"Do/You","W4":"Dark/Heart","W5":"Around/Down","Q1":"Feet/Need","Q2":"Enough/Rough","Q3":"Forever/Never","Q4":"Go/Show","Q5":"Dark/Heart"},
{"Band":"Shakira","W1":"Do/You","W2":"Moral/Rosal","W3":"Ella/Fiesta","W4":"Be/Me","W5":"Through/You","Q1":"Mortal/Rosal","Q2":"Ella/Fiesta","Q3":"Be/Three","Q4":"Do/You","Q5":"Be/Me"},
{"Band":"Shania Twain","W1":"Be/Me","W2":"Apart/Heart","W3":"Night/Right","W4":"Mind/Time","W5":"Day/Way","Q1":"Night/Right","Q2":"On/Strong","Q3":"Night/Right","Q4":"Enough/Love","Q5":"Much/Touch"},
{"Band":"Spice Girls","W1":"Be/Me","W2":"Go/Know","W3":"Fine/Time","W4":"Do/You","W5":"Night/Right","Q1":"Go/Low","Q2":"Fine/Time","Q3":"Swear/There","Q4":"Fast/Past","Q5":"Feel/Real"},
{"Band":"Taylor Swift","W1":"Do/You","W2":"To/You","W3":"Around/Down","W4":"Through/You","W5":"Baby/Me","Q1":"To/You","Q2":"Find/Mind","Q3":"Feel/Real","Q4":"Down/Town","Q5":"Day/Way"},
{"Band":"The Beach Boys","W1":"Be/Me","W2":"Do/You","W3":"Me/See","W4":"Night/Right","W5":"Me/Sea","Q1":"Light/Tonight","Q2":"Know/Snow","Q3":"Hand/Sand","Q4":"Down/Found","Q5":"Blue/You"},
{"Band":"The Beatles","W1":"Do/You","W2":"Me/See","W3":"Be/Me","W4":"Too/You","W5":"Be/See","Q1":"Do/You","Q2":"Mind/Time","Q3":"Eyes/Lies","Q4":"Know/So","Q5":""},
{"Band":"The Black Eyed Peas","W1":"Go/Know","W2":"Day/Way","W3":"Back/That","W4":"Around/Ground","W5":"To/You","Q1":"True/You","Q2":"Back/That","Q3":"Go/Know","Q4":"Disrespect/Effect","Q5":"Back/That"},
{"Band":"The Carpenters","W1":"Be/Me","W2":"Me/See","W3":"Do/You","W4":"Mine/Time","W5":"Heart/Smart","Q1":"Talk/Walk","Q2":"Be/Me","Q3":"Storm/Warm","Q4":"Heart/Smart","Q5":"Devotion/Ocean"},
{"Band":"The Doors","W1":"Do/You","W2":"Beer/Near","W3":"Free/Sea","W4":"Chairs/There","W5":"Untrue/You","Q1":"Pain/Rain","Q2":"Now/Vows","Q3":"Hide/Tide","Q4":"Hide/Tide","Q5":"Hide/Side"},
{"Band":"The Rolling Stones","W1":"Do/You","W2":"Baby/Me","W3":"Mind/Time","W4":"ok","W5":"ok","Q1":"Cry/High","Q2":"Cold/Old","Q3":"Feet/Street","Q4":"ok","Q5":"ok"},
{"Band":"The Who","W1":"Me/See","W2":"Be/Me","W3":"Go/Know","W4":"True/You","W5":"Through/You","Q1":"Hear/Near","Q2":"Feet/Heat","Q3":"Day/Way","Q4":"Apart/Start","Q5":"True/You"},
{"Band":"Tina Turner","W1":"Be/Me","W2":"Me/See","W3":"Around/Down","W4":"Through/You","W5":"Heart/Start","Q1":"Wrong/Strong","Q2":"Say/Way","Q3":"Mine/Time","Q4":"Be/Me","Q5":"Above/Love"},
{"Band":"Tom Petty","W1":"Down/Town","W2":"Do/You","W3":"Light/Night","W4":"Away/Say","W5":"Around/Town","Q1":"Long/Song","Q2":"Again/Friend","Q3":"True/You","Q4":"Down/Town","Q5":"Alright/Night"},
{"Band":"U2","W1":"Do/You","W2":"Away/Day","W3":"Rhyme/Time","W4":"Moon/Room","W5":"Hips/Lips","Q1":"Do/You","Q2":"Around/Down","Q3":"Down/Ground","Q4":"Free/Me","Q5":"Be/Me"},
{"Band":"Usher","W1":"Do/You","W2":"Be/Me","W3":"Me/See","W4":"Girl/World","W5":"To/You","Q1":"Car/Star","Q2":"Go/Low","Q3":"Back/Stack","Q4":"Him/Win","Q5":"Know/Oh"},
{"Band":"Van Halen","W1":"Me/See","W2":"Go/Know","W3":"Through/You","W4":"Around/Down","W5":"True/You","Q1":"Through/You","Q2":"Satisfied/Tried","Q3":"Roll/Soul","Q4":"Mind/Time","Q5":"Me/Sea"}
]

swear_words = ['fuck', 'shit']

# Parse the online thing (from source code of http://www.slate.com/articles/arts/culturebox/2014/02/justin_bieber_and_the_beatles_they_both_liked_to_rhyme_the_same_words.html)
pairs = []
for entry in online_to_parse:
	for key in entry:
		if key != "Band":
			pairs.append(entry[key])  # e.g. ['Do/You', 'True/You']
unique_words = {}
for pair in pairs:
	words = pair.split('/')
	for word in words:
		unique_words[word] = unique_words.get(word,0) + 1   # e.g. {'Do':2, 'You':1 etc.}

common_words = [ x.lower() for x in unique_words if unique_words[x]>=3 and x.lower() not in swear_words ]

save_pickle(common_words, 'created/common_rhyming_words.p')