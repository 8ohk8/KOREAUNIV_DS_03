def main():
    t_user = 0
    t_friend = 0
    t_tweet = 0
    avg_f = 0
    min_f = 0
    max_f = 0
    avg_t = 0
    min_t = 0
    max_t = 0
    flag = 0
        
    while True:
        print("=======================================================")
        print("0. Read data files")
        print("1. Total info")
        print("2. Display statistics")
        print("3. Top 5 most tweeted words")
        print("4. Top 5 users who tweeted the most")
        print("5. Find users who tweeted a word")
        print("6. Find all people who are friends of the above users")
        print("7. Delete all mentions of a word")
        print("8. Delete all users who mentioned a word")
        print("9. Find strongly connected components")
        print("10. Find shortest path from a given user")
        print("99. Quit")
        print("=======================================================")

        a = input("Select Menu: ")
        if a == '0':
            while flag == 1:
                b = input("Love to kill the current database and rebuild a new one? (Y/N) :")
                if b == 'Y':
                    flag = 0
                elif b == 'N':
                    flag = -1
                    break
                else:
                    print("Wrong option.")
            if flag == 0:           
                print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
                print("user.txt reading complete...")
                print("word.txt reading complete...")
                print("friend.txt reading complete...")
                print("\nTotal users: {}\nTotal friendship records: {}\nTotal tweets: {}\n" .format(t_user, t_friend, t_tweet))
                print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")
                flag = 1
            elif flag == -1:
                flag = 1
        elif a == '1':
            print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
            print("Total users: {}\nTotal friendship records: {}\nTotal tweets: {}\n" .format(t_user,t_friend,t_tweet))
            print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")
        elif a == '2':
            print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
            print("Average number of friends: {}\nMinimum number of friends: {}\nMaximum number of friends: {}\n". format(avg_f, min_f, max_f))
            print("Average tweets per user: {}\nMinimum tweets per user: {}\nMaximum tweets per user: {}\n" .format(avg_t ,min_t ,max_t))
            print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")
        elif a == '99':
            print("Good Bye.")
            return
        else:
            print("Wrong option. Try again.")
        

main()

