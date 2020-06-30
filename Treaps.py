from BitHash import BitHash
import pytest
import random
import math

class Node(object): ##adapted from Professor Alan Broder's BST code on nodes
    def __init__(self, k, d):        
        self.key  = k
        self.data = d
        
        #the priority is assigned by a hash function
        #this hash functions assures that a reliably-random priority is assigned
        self.priority = BitHash(k)       
        self.leftChild = None  
        self.rightChild = None

    def __str__(self):
        return "{" + str(self.key) + " , " + str(self.data) + "}"
     


# A Treap object's nodes are balanced as in a BST
# Each node is also assigned a priority randomly
# and is set up as a min-heap according to priority   
class Treaps(object):
    def __init__(self):
        self.__root = None
        self.__nElems = 0
        
    #this method returns the number of nodes present in the Treap    
    def size(self): return self.__nElems            
    
    #returns the string representation of the tree 
    #using the wrapper method below
    def stringify(self):                            
        return self.__stringify(self.__root)
    
    ##this method and its wrapper method(above) were also taken from Prof. Broder's code on BST
    def __stringify(self, cur): 
        if not cur: return ''
        return str(cur) + \
               '(' + self.__stringify(cur.leftChild)  + ')' + \
               '(' + self.__stringify(cur.rightChild) + ')'    
        
    #wrapper method for the __insert method
    #calls the method starting at the root        
    def insert(self, k, d):                                 
        self.__root = self.__insert(k, d, self.__root)
        return True
    
    #this method takes a key and data point and a current node pointer
    #if the key already exists, the original data is replaced by the new data
    #it returns a reference to the node
    def __insert(self, k, d, cur):
        if not cur:                                       
            self.__nElems += 1                            
            return Node(k, d)
        
        if k == cur.key:
            cur.data = d
            return cur
        
        #find the priority of the tree by using the same hashfunction as above, seeded by the desired key
        priority = BitHash(k)                        
        
        #as long as key's proper location is not found
        #continue recursively searching for the key's proper location
        #if the search key is less than the current node's key
        #recursively insert the node into its left child
        if k < cur.key:                                                  
            cur.leftChild = self.__insert(k, d, cur.leftChild)  
            
            #balance the tree to account for the heap properties as well
            #if the current node's priority is greater than the desired priority
            #rotate right around the key to maintain min-heap characteristic
            if cur.priority > priority:                          
                cur = self.rotateRight(cur)  
        
        #if the search key is greater than the current node's key
        #recursively insert the desired node into the rightchild of the node
        elif k > cur.key:                                       
            cur.rightChild = self.__insert(k, d, cur.rightChild)
            
            #again check the priorities
            #rotate if necessary to maintain min-heap characteristics
            if cur.priority > priority: 
                cur = self.rotateLeft(cur)       
            
        return cur
    
    ##both rotate methods based off of Prof. Broder's AVL class file 
    #this method rotates the node to the right
    #uses a simple swap, its leftchild replaces the current node
    #it becomes the new node's right child
    def rotateRight(self, cur):           
        temp = cur.leftChild              
        cur.leftChild = temp.rightChild   
        temp.rightChild = cur           
        return temp                       
    
    #this method rotates the node to the left
    #uses a simple swap, its rightchild replaces the current node
    #and it becomes the new current node's leftchild
    def rotateLeft(self, cur):         
        temp = cur.rightChild            
        cur.rightChild = temp.leftChild  
        temp.leftChild = cur              
        return temp                      

    ##find method adopted from Prof. Broder's BST class code file
    #wrapper method for __find methodstarts from the root and returns the node if found
    def find(self, key):
        n = self.__find(key, self.__root)
        return n
    
    #recursively searches for the key
    #returns data if found, None otherwise
    def __find(self, key, cur): 
        if not cur: return None                                  
        if cur.key == key: return cur.data                      
        if key < cur.key: return self.__find(key, cur.leftChild)
        else: return self.__find(key, cur.rightChild)     
        
        
    #delete method recursively searches for specified key
    #1)if it is found and has two children
    #it is rotated until one of the other 2 conditions apply         
    #2)if it's found and it is a leaf node, it is snipped off
    #3)if its found and has one child, it is replaced with its child 
    def delete(self, key):
        num = self.__nElems
        self.__delete(key, self.__root)
        return self.__nElems < num
        
    def __delete(self, key, cur):        
        if not cur: return None                  
    
        if cur.key == key:                                          
            
            while cur.rightChild and cur.leftChild:
                
                #check the priorities of the two children
                #to rotate in a way that will maintain the min- heap priorities
                
                #if the rightChild's priority is less than the left child's priority
                if cur.rightChild.priority < cur.leftChild.priority: 
                    
                    #rotate left to make the right one the parent node
                    temp = self.rotateLeft(cur)
                    
                     #if the original node was the root
                     #set the root to equal the new parent (original right child)
                    if cur == self.__root: self.__root = temp
                    
                    #set the current node to the original node
                    #(the updated node's left..)
                    cur = temp.leftChild                       
                    
                    #recursively accessing the desired node to delete 
                    #until it no longer has two children
                    return self.__delete(key, temp)              
            
                    
                else: 
                    #the leftchild's priority is less than the rightchild's priority
                    #rotate right around the node to make the leftchild the parent node
                    temp = self.rotateRight(cur)
                  
                    #if the original node was the root
                    #set the root equal to the original left child
                    if cur == self.__root: self.__root = temp
                    
                    #the current node is set to the original node
                    #which is temps rightchild
                    cur = temp.rightChild                      
                    
                    #recursively access the desire node to delete 
                    #until it no longer has two children
                    return self.__delete(key, temp)             
            
            #if the node is a leaf node -- set it to None        
            if not cur.rightChild and not cur.leftChild:
                if cur == self.__root: self.__root = None 
                self.__nElems -=1                     
                return None            
            
            #if there is one child..
            
            
            #if its a right child
            #replace current node with its right child
            elif cur.rightChild and not cur.leftChild:
                
                #if its the root- make root pointer point to that child
                if cur == self.__root:                     
                    cur = cur.rightChild                  
                    self.__root = cur.rightChild
                else: cur= cur.rightChild                  
                self.__nElems -=1                 
                return cur
            
            #if it is a leftChild:
            #do the same as above- just replace the current node with its left child
            elif cur.leftChild and not cur.rightChild:   
                if cur == self.__root: 
                    cur = cur.leftChild
                    self.__root = cur.leftChild
                else: cur = cur.leftChild
                self.__nElems -=1
                return cur
        
        #if the current node exists but its key is not the desired search key
        #continue searching for the key to delete
        #if the key is greater than the current node's key, recursively check its leftchild
        elif key > cur.key: cur.rightChild =  self.__delete(key, cur.rightChild) 
        
        #if the key is less than the current node's key, recursively check its rightchild
        else: cur.leftChild = self.__delete(key, cur.leftChild)
        
        return cur
              
    
    #This method is for testing purposes- used in pytest suite below
    #evaluates the treap to ensure that it maintains the min - heap characteristics
    def isHeap(self, cur = "start"):
        if cur == "start": cur = self.__root
        
        #if it doesnt exist, it is a heap
        if not cur: return True
        
        #if it is a leaf, it is considered as if follows heap qualifications
        if not cur.rightChild and not cur.leftChild: return True         
        
        #if one of its child's priorities are greater than its own, not a min heap
        if cur.rightChild and cur.leftChild: 
            if cur.priority > cur.rightChild.priority or cur.priority > cur.leftChild.priority: return False 
        elif cur.rightChild:
            if cur.rightChild.priority <cur.priority: return False
        elif cur.leftChild:
            if cur.leftChild.priority< cur.priority: return False
        
        #recursively check the entire tree for this characteristic
        rightHeap = self.isHeap(cur.rightChild)
        leftHeap = self.isHeap(cur.leftChild)
        
        #determine whether both the right and left children are heaps
        return rightHeap and leftHeap     
    
    #method used for testing only- used in testing suite below
    #tests that the nodes are in the proper order for a BST in terms of key
    def isBST(self, cur = "start"):                                    
        if cur == "start": cur = self.__root
        if not cur: return True
        if cur.leftChild and cur.leftChild.key> cur.key: return False
        elif cur.rightChild and cur.rightChild.key< cur.key: return False
        
        rightBST = self.isBST(cur.rightChild)
        leftBST = self.isBST(cur.leftChild)
        return rightBST and leftBST

        

    
    
##testing code:     

#tests a treap to ensure that it maintains binary search tree properties 
def test_assertBSTpropertiesWithInsert():
    t = Treaps()
    for i in range(55):
        k = chr(random.randint(1, 200))
        d = random.randint(1, 100000)
        t.insert(k, d)
    assert t.isBST() == True
 
#test for basic insertion
#utilizes find method to check insertion of one item 
def test_basicInsertFind():            
    t = Treaps()
    t.insert("Me", 5555)
    assert t.find("Me") == 5555

#test empty tree for heap properties
#should return True    
def test_emptyTreapforHeapProperties(): 
    t = Treaps()
    assert t.isHeap() == True          

#using random insertion into a treap
#test that everything that is inserted remains
#and that heap properties maintained
def test_heapPropertiesWithInsert():   
    times = 1000
    rand = 250
    t = Treaps()
    elems = set()
    for i in range(times):
        k = chr(random.randint(0, rand))
        d = random.random()
        t.insert(k, d)
        elems.add(k)
    assert t.size() == len(elems)
    assert t.isHeap() == True
    
#test the insertion of many random nodes
#using find method and change in size
def test_insertion():                      
    t = Treaps()
    elems = set()                          
    for i in range(1000):
        key = chr(random.randint(0, 250))
        data = random.randint(0, 1000000)
        t.insert(key, data)
        elems.add(key)
    for e in elems:                       
        assert t.find(key) != None
    assert t.size() == len(elems)  
    
#attempts to delete from an empty treap
#should return False        
def test_deleteEmpty():              
    t = Treaps()
    assert t.delete("Car") == False   

#attempts to delete a non-existant key from a treap that has many nodes
#tests the size to ensure that delete does not work
def test_deleteNonElement():
    t = Treaps()
    for i in range(26):
        k = chr(i + ord('A'))
        d = random.random()
        t.insert(k,d)
    s = t.size()   
    t.delete(" ")
    assert t.size() == s

#simple delete test with a node that is definately present
#ensures that key is present before and not after the delete
#and that size decreases with the delete
def test_deleteActualElement():
    t = Treaps()
    for i in range(26):
        k = chr(i + ord('A'))
        d = chr(i + ord('A'))
        t.insert(k,d)
    assert t.find("A") == "A"  
    s = t.size()             
    t.delete("A")              
    assert s-1 == t.size()       
    assert t.find("A") == None
    
#further deletion test
def test_deleteMore():
    t = Treaps()
    for i in range(95):
        k = chr(i + ord('A'))
        d = chr(i + ord('A'))
        t.insert(k,d)               
        assert t.find(k) == d      
    assert t.size() == 95           
    for i in range(95):             
        k = chr(i + ord('A'))
        d = chr(i + ord('A'))
        t.delete(k)
    for i in range(95):         
        k = chr(i + ord('A'))
        d = chr(i + ord('A'))
        assert t.find(k) == None

#tests find, insert, and heap using rigorous and random insertion    
def test_testFindInsertHeap():            
    t = Treaps()
    kList = []
    dList = []
    r = 10000
    elems = set()
    for i in range(r):
        rand = random.randint(0, 10000000)
        k = str(rand)
        d = r*rand
        t.insert(k,d)
        assert t.find(k) == d
        elems.add(k)
    assert t.isHeap()== True
    assert t.size() == len(elems)
        
        
        

    
pytest.main(["-v", "-s", "Treaps.py"])  
