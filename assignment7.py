#BY Paramroop PARMAR 301555338
import pymssql
from datetime import datetime
import random
import string

# helper function
def generate_random_string():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=22))

def login():
    print("type 'exit' to quit")
    user_id = input("Enter your user ID or (exit to leave): ")
    if user_id == 'exit':
        return 'leave'
    cursor.execute("SELECT name,user_id FROM dbo.User_yelp WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        print("Login successful!")
        return user
    else:
        print("Invalid user ID!")
        return "denied"
    
def search_business():
    while True:
        try:
            min_stars = float(input("Enter the MINIMUM NUMBER of stars from 1-5 or 0 for no requirement: "))
            if min_stars < 0 or min_stars > 5:
                print("Please enter a valid number between 0 and 5.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        break

    min_stars = str(min_stars) 
    # get the city name
    city = input("Enter the name of a city (or press Enter for no requirement): ").lower()
    if (city != ""):
        city = " And city= '" + city +"'"

    name = input("Enter the name (or part of the name) of the business (or press Enter for no requirement): ").lower() # get the name of a business
    if (name != ""):
        name = " And name LIKE '" + name +"%'"

    print("Choose the sorted order:")
    print("1. Name")
    print("2. City")
    print("3. Number of Stars")
    order_choice = input("Enter your choice (1/2/3): ")

    # Determine the sort order based on the user's input
    if order_choice == '1':
        order_by = 'name'
    elif order_choice == '2':
        order_by = 'city'
    elif order_choice == '3':
        order_by = 'stars DESC'  # Sort stars in descending order
    else:
        print("Invalid choice. Defaulting to sorting by name.")
        order_by = 'name'


    # Build the query dynamically
    query = f'''
    SELECT name,business_id,address,city,stars
    FROM dbo.Business
    WHERE stars >= {min_stars}{name}{city}
    order by {order_by}
   
    '''

    # Execute the query
    cursor.execute(query)
    results = cursor.fetchall()
    name_width = 30
    city_width = 15
    stars_width = 10
    id_width = 10
    # Display the results
    if results:
        print(f"{'Name'.ljust(name_width)}{'City'.ljust(city_width)}{'Stars'.ljust(stars_width)}{'ID'.ljust(id_width)}")
        print("-" * (name_width + city_width + stars_width + id_width))
        for row in results:
            print(
        f"{str(row['name']).ljust(name_width)}"
        f"{str(row['city']).ljust(city_width)}"
        f"{str(row['stars']).ljust(stars_width)}"
        f"{str(row['business_id']).ljust(id_width)}"
    )
    else:
        print("No businesses found matching your criteria.")


def search_users():
    # Prompt for user input to filter the search
    name = input("Enter the name (or part of the name) of the user (or press Enter for no filter): ").lower()
    if name != "":
        name = " And name LIKE '" + name +"%'"
    try:
        min_review_count = int(input("Enter the minimum number of reviews (or 0 for no filter): "))
    except ValueError:
        print("Invalid input. Setting minimum reviews to 0.")
        min_review_count = 0

    try:
        min_avg_stars = float(input("Enter the minimum average stars (or 0 for no filter): "))
    except ValueError:
        print("Invalid input. Setting minimum average stars to 0.")
        min_avg_stars = 0.0
    # make the two in values into string format
    min_avg_stars = str(min_avg_stars)
    min_review_count = str(min_review_count)
    # Construct the query
    query = f'''
    SELECT user_id, name, review_count, useful, funny, cool, average_stars, yelping_since
    FROM user_yelp
    WHERE  review_count >= {min_review_count} AND average_stars >= {min_avg_stars} {name}
    ORDER BY name
    '''

    # Execute the query with parameters
    cursor.execute(query)
    results = cursor.fetchall()
    id_width = 30
    name_width = 15
    reviews_width = 10
    useful_width = 10
    funny_width = 10
    cool_width = 10
    avg_stars_width = 15
    yelping_since_width = 15
    # Display results
    if results:
        print(
            f"{'User ID'.ljust(id_width)}"
            f"{'Name'.ljust(name_width)}"
            f"{'Reviews'.ljust(reviews_width)}"
            f"{'Useful'.ljust(useful_width)}"
            f"{'Funny'.ljust(funny_width)}"
            f"{'Cool'.ljust(cool_width)}"
            
            f"{'Avg Stars'.ljust(avg_stars_width)}"
            f"{'Yelping Since'.ljust(yelping_since_width)}"
        )
        print("-" * (id_width + name_width + reviews_width + useful_width +
                     funny_width + cool_width  + avg_stars_width + yelping_since_width))

        # Print each row of results with aligned columns
        for row in results:
            print(
                f"{str(row['user_id']).ljust(id_width)}"
                f"{str(row['name']).ljust(name_width)}"
                f"{str(row['review_count']).ljust(reviews_width)}"
                f"{str(row['useful']).ljust(useful_width)}"
                f"{str(row['funny']).ljust(funny_width)}"
                f"{str(row['cool']).ljust(cool_width)}"
                
                f"{format(row['average_stars'], '.2f').ljust(avg_stars_width)}"
                f"{str(row['yelping_since']).ljust(yelping_since_width)}"
            )
    else:
        print("No users found matching your criteria.")
    return results

def make_friend(user_Id,friend_Id): #need to check if friendship exist that user input, (do i need to make sure that the friendsip is in the list its easy using the in function) then insert

    user_Id = str(user_Id)
    friend_Id = str(friend_Id)
    if user_Id == friend_Id:
        print("You can't make a friend for yourself!")
        return
    #check if friend id is vaild that user inputed
    check_id = f'''
        select *
        from user_yelp u
        where u.user_id = '{friend_Id}' 
    '''
    cursor.execute(check_id)
    exist = cursor.fetchall()

    if not exist:
        print("the friend ID chosen is not vaild")
        return

    check_query = f'''
    SELECT * 
    FROM friendship 
    WHERE user_id = '{user_Id}' AND friend = '{friend_Id}'
    '''
  
    cursor.execute(check_query)
    exist = cursor.fetchall()
   
    if exist:
        print("The friendship already exists ")
        return
   
    insert_query = f''' 
    INSERT INTO friendship (user_id, friend)
    VALUES ('{user_Id}','{friend_Id}')
    '''
    try:
        cursor.execute(insert_query)
        conn.commit()  # Commit the transaction
        print("Friendship successfully added!")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
                

#review the busness

def review_business(user_Id):
    # Step 1: Prompt for the Business ID
    business_Id = input("Enter the Business ID of the business you'd like to review: ")

    # Step 2: Validate that the business exists
    check_business_query = '''
        SELECT * 
        FROM business 
        WHERE business_id = %s
    '''
    cursor.execute(check_business_query, (business_Id,))
    business = cursor.fetchone()

    if not business:
        print("The business ID you entered does not exist.")
        return

    # Step 3: Get the Star rating 
    while True:
        try:
            stars = float(input("Enter your rating for the business (1 to 5): "))
            if stars < 1 or stars > 5:
                print("Please enter a rating between 1 and 5.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter an number between 1 and 5.")
    # Step 5: get the other inputs
    useful = 0 # useful
    try:
        useful = int(input("Enter your useful rating for the business (minimum of 0): "))
        if stars < 0:
            print("Please enter a rating minimum of 0")
            useful = 0  
       
    except ValueError:
        print("Invalid input. your input is 0")
        useful = 0
  
    try:
        funny = int(input("Enter your funny rating for the business (minimum of 0): "))
        if funny < 0:
            print("Please enter a rating minimum of 0")
            funny = 0
        
    except ValueError:
        print("Invalid input. your input is 0")
        funny = 0

    
    try:
        cool = int(input("Enter your rating for the business (minimum of 0): "))
        if cool < 0:
            print("Please enter a rating minimum of 0")
            cool = 0
    except ValueError:
        print("Invalid input. your input is 0")
        cool = 0

    # Step 5: Generate Review ID and Insert the Review, ensuring it's unique
    while True:
        review_Id = generate_random_string()
        check_review_query = '''
            SELECT * 
            FROM review 
            WHERE review_id = %s
        '''
        cursor.execute(check_review_query, (review_Id,))
        existing_review = cursor.fetchone()
        if not existing_review:
            break  # Unique ID found

    # step 6: get the date
    date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # Step7: build query
    useful = str(useful)
    funny = str(funny)
    cool = str(cool)

    review_query = f'''
       INSERT INTO review (review_id, user_id, business_id, stars, useful, funny, cool, date)
      VALUES ('{review_Id}', '{user_Id}', '{business_Id}', {stars}, {useful}, {funny}, {cool}, '{date}')
    '''
  
    

    

    # insert the review just made
    try:
        cursor.execute(review_query)
        conn.commit()  # Commit the transaction
        print("Your review has been successfully added!")
    except Exception as e:
        print(f"An error occurred while adding the review: {e}")
        conn.rollback()  # Rollback the transaction in case of an error
        return

    update_star_query = f'''
        UPDATE dbo.business
            SET stars = (
                    SELECT AVG(CAST(stars AS FLOAT))
                    FROM (
                        SELECT r.stars
                        FROM dbo.review r
                        WHERE r.business_id = '{business_Id}'
                        AND r.date = (
                            SELECT MAX(date)
                            FROM dbo.review
                            WHERE business_id = r.business_id
                            AND user_id = r.user_id
                        )
                    ) AS latest_reviews
                )
            WHERE business_id = '{business_Id}';
    '''
    try:
        cursor.execute(update_star_query, ( business_Id))
        conn.commit()
    except Exception as e:
        print(f"An error occurred while updating the review: {e}")
        conn.rollback()


# qQ5uuXrKu-Japb9rT2sx0Q bussniess
#make friend with this guy: HAnoq5ztXMaFgOi8K1bCYQ
 #INSERT INTO friendship (user_id, friend)
  #  VALUES ('{user_Id}','{friend_Id}')


try:
    conn = pymssql.connect(
        host='cypress.csil.sfu.ca',
        user='s_psp10',  # Your SFU username
        password='NLhefh23bTbaeNgE',  # Your passphrase
        database='psp10354'  # Your database name
    )
    cursor = conn.cursor(as_dict=True)
    
    # Test the connection by running a simple query
   


    print("\nPlease log in!")
    access = "denied"
    while access == "denied":
        access = login()
    if access == 'leave':
        if conn:
            conn.close()
        exit(0)

        
    
    print("welcome back",access["name"])
    
    #note access contains the user log in
    while True:
        print("\nWhat would you like to do Dear User? ")
        print("Type the (number or the word)")
        print("1. Search Business")
        print("2. Search Users")
        print("   a) make a friend")
        print("3. Make a friend")
        print("4. Review Business")
        print("5. Exit")
        option = input("please select what you would like to do? ").lower()
            
        
        if(option == "1" or option == "search business"):
            print("\nplease select the filters")
            search_business()

        elif(option == "search user" or option == "2" or option == "search users"):
            friend_list = search_users()
            print("\nwould you like to make a friend?: ") #wants to check
            id = input("\nPlease type the user id if you would like to make a friend (otherwise press enter): ").replace(" ",'')
            if (id != ""):
                make_friend(access["user_id"],id)    

        elif(option == "make a friend" or option == "3"):
            id = input("\nPlease type the user id to whom you would like to make a friend ").replace(" ",'')
            if (id != ""):
                make_friend(access["user_id"],id)  

        elif(option == "review business" or option == "4"):
             review_business(access["user_id"])
        elif(option == "exit" or option == "5"):
             break
        

        
    

except pymssql.Error as e:
    print(f"Error: {e}")
finally:
    # Close the connection after testing
    if conn:
        conn.close()




