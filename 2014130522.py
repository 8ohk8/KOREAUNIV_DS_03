import os

class rbNode:
    def __init__(self, key, color='', string=''):
        self.key = key
        self.p = None
        self.left = None
        self.right = None
        self.color = color
        self.buf = {}
        self.buf2 = {}
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

    def insert(self, key, string=''): # O(logn)
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
                    z.p.color = 'b'
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
                    z.p.color = 'b'
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

    def search(self, key, x=None): # O(logn)
        if x == None:
            x = self.root
        while key != x.key and x != self.nil: # O(logn)
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x
    
    def maximum(self, x=None): # O(logn)
        if x == None:
            x = self.root
        while x.right is not self.nil: # O(logn)
            x = x.right
        return x

    def minimum(self, x=None): # O(logn)
        if x == None:
            x = self.root
        while x.left is not self.nil: # O(logn)
            x = x.left
        return x

    def findPred(self, x=None): # O(logn)
        if x == None:
            x = self.root
        if x.left != self.nil:
            x = self.maximum(x.left) # O(logn)
            return x
        else: 
            while x.p.left == x: # O(logn)
                x = x.p
                if x.p.p == self.nil:
                    return self.nil
            return x.p

    def findTop5(self): # O(logn)
        cnt = 1
        buf = []
        a = self.maximum() # O(logn)
        buf.append(a)
        while cnt < 6: # O(logn) - average
            b = self.findPred(a) # O(logn)
            if a.key != b.key:
                cnt += 1
                buf.append(b)
                a = b
            else:
                a = b
        return buf

    def transplant(self, u, v):
        if u.p == self.nil:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p

    def delete(self, z): # O(logn)
        y = z
        y_original_color = y.color
        if z.left == self.nil:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.p == z:
                x.p = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            self.transplant(z, y)
            y.left = z.left
            y.left.p = y
            y.color = z.color
        if y_original_color == 'b':
            self._deleteFixup(x)

    def _deleteFixup(self, x):
        while x != self.root and x.color == 'b':
            if x == x.p.left:
                w = x.p.right
                if w.color == 'r':
                    w.color = 'b'
                    x.p.color = 'r'
                    self._rotateLeft(x.p)
                    w = x.p.right
                if w.left.color == 'b' and w.right.color == 'b':
                    w.color = 'r'
                    x = x.p
                elif w.right.color == 'b':
                    w.left.color = 'b'
                    w.color = 'r'
                    self._rotateRight(w)
                elif w.color == 'b' and w.right.color == 'r':
                    w = x.p.right
                    w.color = x.p.color
                    x.p.color = 'b'
                    w.right.color = 'b'
                    self._rotateLeft(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.color == 'r':
                    w.color = 'b'
                    x.p.color = 'r'
                    self._rotateRight(x.p)
                    w = x.p.left
                if w.right.color == 'b' and w.left.color == 'b':
                    w.color = 'r'
                    x = x.p
                elif w.left.color == 'b':
                    w.right.color = 'b'
                    w.color = 'r'
                    self._rotateLeft(w)
                else:
                    w = x.p.left
                    w.color = x.p.color
                    x.p.color = 'b'
                    w.left.color = 'b'
                    self._rotateRight(x.p)
                    x = self.root
        x.color = 'b'
        
def readUserTxt(filename, rbtree): # O(nlogn)
    cnt1 = -1
    with open(filename, 'r') as f: # O(n)
        for line in f:
            cnt1 += 1
            if cnt1 % 4 == 0:
                tmp = line.rstrip()
                rbtree.insert(tmp) # O(logn)
                
def readWordTxt(filename, rbtree, user_rb): # O(nlogn)
    cnt1 = -1
    with open(filename, 'r') as f: # O(n)
        buf = []
        for line in f:
            cnt1 += 1
            if cnt1 % 4 == 0:
                buf.append(line)
            elif cnt1 % 4 == 2:
                word = line.rstrip()
                rbtree.insert(word) # O(logn)
                usr = buf.pop().rstrip()
                x = rbtree.search(word) # O(logn)
                x.count += 1
                if usr in x.buf:
                    x.buf[usr] += 1 # O(1)
                else:
                    x.buf[usr] = 1 # O(1)
                y = user_rb.search(usr) # O(logn)
                y.count += 1
                if word in y.buf2:
                    y.buf2[word] += 1 # O(1)
                else:
                    y.buf2[word] = 1 # O(1)
            
def readFriendTxt(filename, rbtree): # O(nlogn)
    cnt1 = -1
    x = None
    with open(filename, 'r') as f: # O(n)
        for line in f:
            cnt1 += 1
            tmp = line.rstrip()
            if cnt1 % 3 == 0:
                x = rbtree.search(tmp) # O(logn)
            elif cnt1 % 3 == 1:
                x.buf[tmp] = 1 # O(1)

def buildFriendNumRBtree(user_node, user_rb, rbtree, total, total2):
    node = user_node
    if node.left is not user_rb.nil:
        total, total2 = buildFriendNumRBtree(node.left, user_rb, rbtree, total, total2)
    rbtree.insert(key=node.buflen, string=node.key)  # O(logn)
    total += 1
    total2 += node.buflen
    if node.right is not user_rb.nil:
        total, total2 = buildFriendNumRBtree(node.right, user_rb, rbtree, total, total2)
    return total, total2

def buildTweetsPerUserRBtree(user_node, user_rb, rbtree, total):
    node = user_node
    if node.left is not user_rb.nil:
       total = buildTweetsPerUserRBtree(node.left, user_rb, rbtree, total)
    rbtree.insert(key=node.count, string=node.key) # O(logn)
    total += node.count
    if node.right is not user_rb.nil:
        total = buildTweetsPerUserRBtree(node.right, user_rb, rbtree, total)
    return total
    
    
def buildWordFreqRBtree(word_node, word_rb, rbtree, total):
    node = word_node
    if node.left is not word_rb.nil:
        total = buildWordFreqRBtree(node.left, word_rb, rbtree, total)
    rbtree.insert(key=node.count, string=node.key) # O(logn)
    total += node.count
    if node.right is not word_rb.nil:
        total =buildWordFreqRBtree(node.right, word_rb, rbtree, total)
    return total
        
def IsDataEmpty(rbtree1, rbtree2):
    if rbtree1.root == rbtree1.nil or rbtree2.root == rbtree2.nil:
        return True
    else:
        return False

def rbPrint(tree, level):
    if (tree.right):
        rb_print(tree.right, level + 1)
    for i in range(level):
        print('    ', end = '')
    if tree.color == 'r':
        color = 'red'
    else:
        color = 'blk'
    print("{} :{}" .format(color, tree.key))
    if (tree.left):
        rb_print(tree.left, level + 1)

def traversalWhilePopping(node, user_rb, userid):
    if node.left != user_rb.nil:
        traversalWhilePopping(node.left, user_rb, userid)
    if userid in node.buf:
        node.buf.pop(userid)
    if node.right != user_rb.nil:
        traversalWhilePopping(node.right, user_rb, userid)
        
def main():
    clear = lambda: os.system('cls')
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

    print("*********************************************************************")
    print("*********************************************************************")
    print("***************************TwittyTidbit 1.0**************************")
    print("*********************************************************************")
    print("*********************************************************************")
    print("                                                         Hyeongeun Oh")
    input("Press Enter key to start\n")
    clear()
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
        if a == '0': # O(nlogn)
            while flag is 1:
                b = input("Love to kill the current database and rebuild a new one? (Y/N) ")
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
                readUserTxt('user.txt', user_rb) # O(nlogn)
                print("user.txt reading complete")
                
                print("reading word.txt...")
                readWordTxt('word.txt', word_rb, user_rb) # O(nlogn)
                print("word.txt reading complete")

                print("reading friend.txt..")
                readFriendTxt('friend.txt', user_rb) # O(nlogn)
                print("friend.txt reading complete")

                t_user, t_friend = buildFriendNumRBtree(user_rb.root, user_rb, friend_num_rb, 0, 0) # O(nlogn)
                t_tweet = buildTweetsPerUserRBtree(user_rb.root, user_rb, tweets_per_rb, 0) # O(nlogn)
                assert t_tweet == buildWordFreqRBtree(word_rb.root, word_rb, word_freq_rb, 0) # O(nlogn)
                
                flag = 1
            elif flag == -1:
                flag = 1
                
        elif IsDataEmpty(user_rb, word_rb):
            if a == '99':
                print("Good Bye.")
                return
            print("No data available to analyze! Plz read data files first!")
            input("Press Enter key to continue\n")
            clear()
            continue
            
        elif a == '1': # O(1)
            print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
            print("Total users: {}\nTotal friendship records: {}\nTotal tweets: {}\n" .format(t_user,t_friend,t_tweet))
            print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")
            
        elif a == '2': # O(logn)
            avg_f = t_friend / t_user # O(1)
            min_f = friend_num_rb.minimum().key # O(logn)
            max_f = friend_num_rb.maximum().key # O(logn)

            avg_t = t_tweet / t_user # O(1)
            min_t = tweets_per_rb.minimum().key # O(logn)
            max_t = tweets_per_rb.maximum().key # O(logn)
 
            print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
            print("Average number of friends: {:.5f}\nMinimum number of friends: {}\nMaximum number of friends: {}\n". format(avg_f, min_f, max_f))
            print("Average tweets per user: {:.5f}\nMinimum tweets per user: {}\nMaximum tweets per user: {}\n" .format(avg_t ,min_t ,max_t))
            print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")
            
        elif a == '3': # O(logn)
            buf = word_freq_rb.findTop5() # O(logn)
            
            print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
            print("<<Top 5 most tweeted words>>\n")
            for i in buf: # O(k)
                print("{1} : {0} times tweeted" .format(i.key, i.string))
            print("\n♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")

        elif a == '4': # O(logn)
            buf = tweets_per_rb.findTop5() # O(logn)

            print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
            print("<<Top 5 users who tweeted the most>>\n")
            for i in buf: # O(k)
                print("{1} : tweeted {0} times" .format(i.key, i.string))
            print("\n♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")

        elif a == '5': # O(logn)
            b = input("Enter a word: ")
            tmp = word_rb.search(b) # O(logn)
            if tmp == word_rb.nil:
                print("No user ever tweeted the word.")
                input("Press Enter key to continue\n")
                clear()
                continue
            while True:
                c = input("Would you like to store the data in usersOf{}.txt? (Y/N) " .format(b))
                if c == 'Y':
                    f = open('usersOf' + b + '.txt', 'w')
                    print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
                    print("<<Who tweeted the word '{}'?>>\n" .format(b))
                    for key in tmp.buf: # O(k) - k is a constant on average
                       print(key)
                       f.write(key + '\n')
                    print("\n♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")
                    f.close()
                    break
                elif c == 'N':
                    print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
                    print("<<Who tweeted the word '{}'?>>\n" .format(b))
                    for key in tmp.buf: # O(k) - k is a constant on average
                       print(key)
                    print("\n♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")
                    break
                else:
                    print("Wrong option")
                    
        elif a == '6': # O(logn)
            b = input("Enter a user id: ")
            tmp = user_rb.search(b) # O(logn)
            if tmp == user_rb.nil:
                print("No user with such id number exists.")
                input("Press Enter key to continue\n")
                clear()
                continue
            while True:
                c = input("Would you like to store the data in friendsOf{}.txt? (Y/N) " .format(b))
                if c == 'Y':
                    f = open('friendsOf' + b + '.txt', 'w')
                    print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
                    print("<<Who are the friends of the user '{}'?>>\n" .format(b))
                    for key in tmp.buf: # O(k) - k is a constant on average
                       print(key)
                       f.write(key + '\n')
                    print("\n♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")
                    f.close()
                    break
                elif c == 'N':
                    print("♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣\n")
                    print("<<Who are the friends of the user '{}'?>>\n" .format(b))
                    for key in tmp.buf: # O(k) - k is a constant on average
                       print(key)
                    print("\n♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣♣")
                    break
                else:
                    print("Wrong option")

        elif a == '7': # O(nlogn)
            b = input("Enter a word: ")
            tmp = word_rb.search(b) # O(logn)
            if tmp == word_rb.nil:
                print("Cannot find any mention of such a word.")
                input("Press Enter key to continue\n")
                clear()
                continue
            else:
                print("Deleting all mentions of {}....." .format(b))
                word_rb.delete(tmp) # O(logn)
                for key in tmp.buf: # k * O(logn)
                    x = user_rb.search(key=key) # O(logn)
                    x.count -= tmp.buf[key] # O(1)
                    x.buf2.pop(tmp.key) # O(1)
                friend_num_rb.root = friend_num_rb.nil
                tweets_per_rb.root = tweets_per_rb.nil
                word_freq_rb.root = word_freq_rb.nil
                t_user, t_friend = buildFriendNumRBtree(user_rb.root, user_rb, friend_num_rb, 0, 0) # O(nlogn)
                t_tweet = buildTweetsPerUserRBtree(user_rb.root, user_rb, tweets_per_rb, 0) # O(nlogn)
                assert t_tweet == buildWordFreqRBtree(word_rb.root, word_rb, word_freq_rb, 0) # O(nlogn)
                print("All mentions of {} are deleted." .format(b))
                    
        elif a == '8': # O(nlogn)
            b = input("Enter a word: ")
            tmp = word_rb.search(b) # O(logn)
            if tmp == word_rb.nil:
                print("No user ever mention the word already.")
                input("Press Enter key to continue\n")
                clear()
                continue
            else:
                print("Deleting all users that mentioned {}....." .format(b))
                buf = []
                for key in tmp.buf: # O(k)
                    buf.append(key)
                for key in buf: # k * O(n)
                    x = user_rb.search(key) # O(logn)
                    t_tweet -= x.count
                    for key in x.buf2: # k * O(logn)
                        z = word_rb.search(key) # O(logn)
                        z.count -= z.buf[x.key] # O(1) (Average)
                        z.buf.pop(x.key) # O(1) (Average)
                    traversalWhilePopping(user_rb.root, user_rb, x.key) # O(n) (Average)
                    user_rb.delete(x) # O(logn)
                word_rb.delete(tmp) # O(logn)
                friend_num_rb.root = friend_num_rb.nil
                tweets_per_rb.root = tweets_per_rb.nil
                word_freq_rb.root = word_freq_rb.nil
                t_user, t_friend = buildFriendNumRBtree(user_rb.root, user_rb, friend_num_rb, 0, 0) # O(nlogn)
                t_tweet = buildTweetsPerUserRBtree(user_rb.root, user_rb, tweets_per_rb, 0) # O(nlogn)
                assert t_tweet == buildWordFreqRBtree(word_rb.root, word_rb, word_freq_rb, 0) # O(nlogn)
                print("All mentions of {} are deleted." .format(b))
                print("All users who mentioned the word {} are deleted." .format(b))
                
        elif a == '9':
            print("yet to be implemented")

        elif a == '10':
            print("yet to be implemented")
            
        elif a == '99':
            print("Good Bye.")
            return
        
        else:
            print("Wrong option. Try again.")

        if not a == '0':
            e = input("Press Enter key to continue\n")
            clear()

        else:
            clear()

main()
