parser 需求：

1. location: x,y  

2. title        //(the title of the group purchase)

3. cover img   // (one img url from group purchase info)

4. time interval  // (start time & end time)

5. content //(realted text of this purchase info)



DATABASE 需求：

with all 5 basic info we need add more parse info into databse:

6. parse website loactoin(from which web site, eg:www.gaopeng.com)

7. type_tag (which category does this group buying belongs to )

    type_tag:  0: food
               1: film
               2: travelling
               3: others
        
   (hard work exist in this part)

   some website gives the categoary ,we could easily get the type_tag info
   others which do not give the categoary we at present directly gives it type_tag:3 
   which we can later optimize 
               


since x,y location is very accurate (float number)
we define a unique database record with location+website_address (1 and 6)  
if there is any overlap we simply skip this .
why we do this: in prevention of any reparsement. 