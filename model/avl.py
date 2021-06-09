class RGB(object):
    def __init__(self, value):
        if not isinstance(value, list):
             raise TypeError('Type is supposed to be of list')
        if len(value) != 3:
            raise TypeError('Length of list is supposed to be 3')
        self.value = value
    
    def lt(self, rgb):
        if (self.value[0] < rgb.value[0]):
            return True
        elif(self.value[0] > rgb.value[0]):
            return False
        elif(self.value[1] < rgb.value[1]):
            return True
        elif (self.value[1] > rgb.value[1]):
            return False
        elif (self.value[2] < rgb.value[2]):
            return True
        elif (self.value[2] > rgb.value[2]):
            return False
        else:
            return False
    
    def eq(self, rgb):
        if self.value == rgb.value:
            return True
        return False

    def to_string(self):
        return str(self.value)

class Node(object):
    # Key is a RGB list such as [26, 171, 125] = #1aab7d
    # value is the filename corresponding to the determined RGB value
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVL(object):
    def insert(self, root, key, value):
     
        if not root:
            return Node(key, value)
        elif key.lt(root.key):
            root.left = self.insert(root.left, key, value)
        else:
            root.right = self.insert(root.right, key, value)

        root.height = 1 + max(self.getHeight(root.left),
                           self.getHeight(root.right))
 
        balance = self.getBalance(root)
 
        if balance > 1 and key.lt(root.left.key):
            return self.rightRotate(root)
 
        if balance < -1 and root.right.key.lt(key):
            return self.leftRotate(root)
 
        if balance > 1 and root.left.key.lt(key):
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
 
        if balance < -1 and key.lt(root.right.key):
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
 
        return root
 
    def leftRotate(self, z):
 
        y = z.right
        T2 = y.left
 
        y.left = z
        z.right = T2
 
        z.height = 1 + max(self.getHeight(z.left),
                         self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                         self.getHeight(y.right))
 
        return y
 
    def rightRotate(self, z):
 
        y = z.left
        T3 = y.right
 
        y.right = z
        z.left = T3
 
        z.height = 1 + max(self.getHeight(z.left),
                        self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                        self.getHeight(y.right))
 
        return y
 
    def getHeight(self, root):
        if not root:
            return 0
 
        return root.height
 
    def getBalance(self, root):
        if not root:
            return 0
 
        return self.getHeight(root.left) - self.getHeight(root.right)
 
    def preOrder(self, root):
 
        if not root:
            return
 
        print("{0} ".format(root.key.to_string()), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)

    def getInOrder(self, root, rgbs):
        if not root:
            return

        self.getInOrder(root.left, rgbs)
        rgbs.append(root.key)
        self.getInOrder(root.right, rgbs)
        return rgbs
 



myTree = AVL()
root = None
 
root = myTree.insert(root, RGB([101, 183, 64]), "A")
root = myTree.insert(root, RGB([53, 187, 110]), "B")
root = myTree.insert(root, RGB([101, 118, 74]), "C")
root = myTree.insert(root, RGB([19, 203, 245]), "D")
 

rgbs = myTree.getInOrder(root, [])

for i in range(len(rgbs)-2):
    if not rgbs[i].lt(rgbs[i+1]):
        print("List aint sorted")

print("List is sorted")