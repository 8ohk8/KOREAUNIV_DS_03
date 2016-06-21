class rbNode:
    def __init__(self, key, color='', string=''):
        self.key = key
        self.p = None
        self.left = None
        self.right = None
        self.color = color
        self.buf = {}
        self.count = 0
        self.string = string

    @property
    def buflen(self):
        return len(self.buf)
    
# all are implemented based on the textbook
class rbTree:
    def __init__(self, flag=0):
        self.flag = flag
        self.nil = rbNode(key=None, color='b')
        self.root = self.nil # the root of our tree i.e. the entry to the tree

    def insert(self, key, string=''):
        if self.root is self.nil:
            self.root = rbNode(key=key, string=string)
            self.root.p = self.nil
            self.root.left = self.nil
            self.root.right = self.nil
        else:
            self._insert(rbNode(key=key, string=string))

    def _insert(self, z):
        y = self.nil
        x = self.root
        while x is not self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            elif z.key == x.key and self.flag == 0:
                return
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

    def search(self, key, x=None):
        if x == None:
            x = self.root
        while key != x.key and x != self.nil:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def maximum(self, x=None):
        if x == None:
            x = self.root
        while x.right is not self.nil:
            x = x.right
        return x

    def minimum(self, x=None):
        if x == None:
            x = self.root
        while x.left is not self.nil:
            x = x.left
        return x

    def findPred(self, x=None):
        if x == None:
            x = self.root
        if x.left != self.nil:
            x = self.maximum(x.left)
            return x
        else:
            while x.p.left == x:
                x = x.p
                if x.p.p == self.nil:
                    return self.nil
            return x.p

    def findTop5(self):
        cnt = 1
        buf = []
        a = self.maximum()
        buf.append(a)
        while cnt < 6:
            b = self.findPred(a)
            if a.key != b.key:
                cnt += 1
                buf.append(b)
                a = b
            else:
                a = b
        return buf
            

def readUserTxt(filename, rbtree):
    cnt1, cnt2 = -1, 0
    with open(filename, 'r') as f:
        for line in f:
            cnt1 += 1
            if cnt1 % 4 == 0:
                tmp = line.rstrip()
                rbtree.insert(tmp)
                cnt2 += 1
            else:
                continue
    return cnt2

def readWordTxt(filename, rbtree, user_rb):
    cnt1, cnt2 = -1, 0
    with open(filename, 'r') as f:
        buf = []
        for line in f:
            cnt1 += 1
            if cnt1 % 4 == 0:
                buf.append(line)
            elif cnt1 % 4 == 2:
                rbtree.insert(line.rstrip())
                usr = buf.pop().rstrip()
                x = rbtree.search(line.rstrip())
                x.count += 1
                if usr in x.buf:
                    x.buf[usr] += 1
                else:
                    x.buf[usr] = 1
                y = user_rb.search(usr)
                y.count += 1
                cnt2 += 1
    return cnt2

def readFriendTxt(filename, rbtree):
    cnt1, cnt2 = -1, 0
    x = None
    with open(filename, 'r') as f:
        for line in f:
            cnt1 += 1
            tmp = line.rstrip()
            if cnt1 % 3 == 0:
                x = rbtree.search(tmp)
            elif cnt1 % 3 == 1:
                x.buf[tmp] = 1
                cnt2 += 1
        return cnt2

def buildFriendNumRBtree(user_node, user_rb, rbtree):
    node = user_node
    if node.left is not user_rb.nil:
        buildFriendNumRBtree(node.left, user_rb, rbtree)
    rbtree.insert(key=node.buflen, string=node.key)
    if node.right is not user_rb.nil:
        buildFriendNumRBtree(node.right, user_rb, rbtree)


def buildTweetsPerUserRBtree(user_node, user_rb, rbtree):
    node = user_node
    if node.left is not user_rb.nil:
        buildTweetsPerUserRBtree(node.left, user_rb, rbtree)
    rbtree.insert(key=node.count, string=node.key)
    if node.right is not user_rb.nil:
        buildTweetsPerUserRBtree(node.right, user_rb, rbtree)
    
    
def buildWordFreqTRBtree(word_node, word_rb, rbtree):
    node = word_node
    if node.left is not word_rb.nil:
        buildWordFreqTRBtree(node.left, word_rb, rbtree)
    rbtree.insert(key=node.count, string=node.key)
    if node.right is not word_rb.nil:
        buildWordFreqTRBtree(node.right, word_rb, rbtree)
        
def IsDataEmpty(rbtree1, rbtree2):
    if rbtree1.root == rbtree1.nil or rbtree2.root == rbtree2.nil:
        return True
    else:
        return False

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
    friend_num_rb = rbTree(1)
    tweets_per_rb = rbTree(1)
    word_freq_rb = rbTree(1)

    while True:
        print("=======================================================")
        print("0. Read data files")
        print("1. Display statistics")
        print("2. Get more detailed statistics")
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
                    word_rb.root = word_rb.nil
                    friend_num_rb.root = friend_num_rb.nil
                    tweets_per_rb.root = tweets_per_rb.nil
                    word_freq_rb.root = word_freq_rb.nil
                elif b == 'N':
                    flag = -1
                    break
                else:
                    print("Wrong option.")
            if flag == 0:
                print("reading user.txt...")
                t_user = readUserTxt('user.txt', user_rb)
                print("user.txt reading complete")
                
                print("reading word.txt...")
                t_tweet = readWordTxt('word.txt', word_rb, user_rb)
                print("word.txt reading complete")

                print("reading friend.txt..")
                t_friend = readFriendTxt('friend.txt', user_rb)
                print("friend.txt reading complete")

                buildFriendNumRBtree(user_rb.root, user_rb, friend_num_rb)
                buildTweetsPerUserRBtree(user_rb.root, user_rb, tweets_per_rb)
                buildWordFreqTRBtree(word_rb.root, word_rb, word_freq_rb)
                
                print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
                print("Total users: {}\nTotal friendship records: {}\nTotal tweets: {}\n" .format(t_user, t_friend, t_tweet))
                print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")
                flag = 1
            elif flag == -1:
                flag = 1
                
        elif IsDataEmpty(user_rb, word_rb):
            if a == '99':
                print("Good Bye.")
                return user_rb, word_rb, friend_num_rb, tweets_per_rb, word_freq_rb
            print("No data available to analyze! Plz read data files first!")
            continue
        
        elif a == '1':
            print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
            print("Total users: {}\nTotal friendship records: {}\nTotal tweets: {}\n" .format(t_user,t_friend,t_tweet))
            print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")
            
        elif a == '2':
            avg_f = t_friend / t_user
            min_f = friend_num_rb.minimum().key
            max_f = friend_num_rb.maximum().key

            avg_t = t_tweet / t_user
            min_t = tweets_per_rb.minimum().key
            max_t = tweets_per_rb.maximum().key
            
            print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
            print("Average number of friends: {:.3f}\nMinimum number of friends: {}\nMaximum number of friends: {}\n". format(avg_f, min_f, max_f))
            print("Average tweets per user: {:.3f}\nMinimum tweets per user: {}\nMaximum tweets per user: {}\n" .format(avg_t ,min_t ,max_t))
            print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")
            
        elif a == '3':
            buf = word_freq_rb.findTop5()
            
            print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
            print("<<Top 5 most tweeted words>>\n")
            for i in buf:
                print("{1} : {0} times tweeted" .format(i.key, i.string))
            print("\n♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")

        elif a == '4':
            buf = tweets_per_rb.findTop5()

            print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
            print("<<Top 5 users who tweeted the most>>\n")
            for i in buf:
                print("{1} : tweeted {0} times" .format(i.key, i.string))
            print("\n♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")

        elif a == '5':
            b = input("Enter a word: ")
            tmp = word_rb.search(b)
            if tmp == word_rb.nil:
                print("No user ever tweeted the word.")
                continue
            while True:
                c = input("Would you like to store the data in usersOf{}.txt? (Y/N) " .format(b))
                if c == 'Y':
                    f = open('usersOf' + b + '.txt', 'w')
                    print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
                    print("<<Who tweeted the word '{}'?>>\n" .format(b))
                    for key in tmp.buf:
                       print(key)
                       f.write(key + '\n')
                    print("\n♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")
                    f.close()
                    break
                elif c == 'N':
                    print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
                    print("<<Who tweeted the word '{}'?>>\n" .format(b))
                    for key in tmp.buf:
                       print(key)
                    print("\n♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")
                    break
                else:
                    print("Wrong option")
                    
        elif a == '6':
            b = input("Enter a user id: ")
            tmp = user_rb.search(b)
            if tmp == user_rb.nil:
                print("No user with such id number exists.")
                continue
            while True:
                c = input("Would you like to store the data in friendsOf{}.txt? (Y/N) " .format(b))
                if c == 'Y':
                    f = open('friendsOf' + b + '.txt', 'w')
                    print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
                    print("<<Who are the friends of the user '{}'?>>\n" .format(b))
                    for key in tmp.buf:
                       print(key)
                       f.write(key + '\n')
                    print("\n♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")
                    f.close()
                    break
                elif c == 'N':
                    print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
                    print("<<Who are the friends of the user '{}'?>>\n" .format(b))
                    for key in tmp.buf:
                       print(key)
                    print("\n♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")
                    break
                else:
                    print("Wrong option")

        elif a == '7':
            print("yet to be implemented")

        elif a == '8':
            print("yet to be implemented")
            
        elif a == '99':
            print("Good Bye.")
            return user_rb, word_rb, friend_num_rb, tweets_per_rb, word_freq_rb
        
        else:
            print("Wrong option. Try again.")


a, b, c, d, e = main()

