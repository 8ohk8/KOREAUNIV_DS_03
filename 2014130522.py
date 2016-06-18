class rbNode:
    def __init__(self, key, color=''):
        self.key = key
        self.p = None
        self.left = None
        self.right = None
        self.color = color
        self.dict = {}
        self.count = 0

#all are implemented based on the textbook
class rbTree:
    def __init__(self):
        self.nil = rbNode(key=None, color='b')
        self.root = self.nil # the root of our tree i.e. the entry to the tree

    def insert(self, key):
        if self.root is self.nil:
            self.root = rbNode(key)
            self.root.p = self.nil
            self.root.left = self.nil
            self.root.right = self.nil
        else:
            self._insert(rbNode(key))

    def _insert(self, z):
        y = self.nil
        x = self.root
        while x is not self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.p = y
        if y is self.nil:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        z.color = 'r'
        self._insertFixup(z)

    def _insertFixup(self, z):
        while z.p.color is 'r':
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.color == 'r':
                    z.p.color == 'b'
                    y.color = 'b'
                    z.p.p.color = 'r'
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self._rotateLeft(z)
                    z.p.color = 'b'
                    z.p.p.color = 'r'
                    self._rotateRight(z.p.p)
            else:
                y = z.p.p.left
                if y.color == 'r':
                    z.p.color == 'b'
                    y.color = 'b'
                    z.p.p.color = 'r'
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self._rotateRight(z)
                    z.p.color = 'b'
                    z.p.p.color = 'r'
                    self._rotateLeft(z.p.p)
        self.root.color = 'b'
        
    def _rotateLeft(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.p = x
        y.p = x.p
        if x.p == self.nil:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y

    def _rotateRight(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.p = y
        x.p = y.p
        if y.p == self.nil:
            self.root = x
        elif y == y.p.right:
            y.p.right = x
        else:
            y.p.left = x
        x.right = y
        y.p = x

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
    user_rb = rbTree()
    word_rb = rbTree()
    friend_heap = []
    word_heap = []
        
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
            while flag is 1:
                b = input("Love to kill the current database and rebuild a new one? (Y/N) :")
                if b == 'Y':
                    flag = 0
                    user_rb.root = user_rb.nil
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

