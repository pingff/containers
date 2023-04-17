'''
This file implements the Heap data structure as a subclass of the BinaryTree.
The book implements Heaps using an *implicit* tree with an *explicit* vector implementation,
so the code in the book is likely to be less helpful than the code for the other data structures.
The book's implementation is the traditional implementation because it has a faster constant factor
(but the same asymptotics).
This homework is using an explicit tree implementation to help you get more practice with OOP-style programming and classes.
'''

from containers.BinaryTree import BinaryTree, Node


class Heap(BinaryTree):
    '''
    FIXME:
    Heap is currently not a subclass of BinaryTree.
    You should make the necessary changes in the class declaration line above
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        If xs is a list (i.e. xs is not None),
        then each element of xs needs to be inserted into the Heap.
        '''
        super().__init__()
        self.num_nodes = 0
        if xs:
            for x in xs:
                self.insert(x)

    def __repr__(self):
        '''
        Notice that in the BinaryTree class,
        we defined a __str__ function,
        but not a __repr__ function.
        Recall that the __repr__ function should return a string that can be used to recreate a valid instance of the class.
        Thus, if you create a variable using the command Heap([1,2,3])
        it's __repr__ will return "Heap([1,2,3])"

        For the Heap, type(self).__name__ will be the string "Heap",
        but for the AVLTree, this expression will be "AVLTree".
        Using this expression ensures that all subclasses of Heap will have a correct implementation of __repr__,
        and that they won't have to reimplement it.
        '''
        return type(self).__name__ + '(' + str(self.to_list('inorder')) + ')'

    def is_heap_satisfied(self):
        '''
        Whenever you implement a data structure,
        the first thing to do is to implement a function that checks whether
        the structure obeys all of its laws.
        This makes it possible to automatically test whether insert/delete functions
        are actually working.
        '''
        if self.root:
            return Heap._is_heap_satisfied(self.root)
        return True

    @staticmethod
    def _is_heap_satisfied(node):
        '''
        FIXME:
        Implement this method.
        '''
        ret = True
        if node.left:
            ret &= node.value <= node.left.value
            ret &= Heap._is_heap_satisfied(node.left)
        if node.right:
            ret &= node.value <= node.right.value
            ret &= Heap._is_heap_satisfied(node.right)
        return ret

    def insert(self, value):
        '''
        Inserts value into the heap.

        FIXME:
        Implement this function.

        HINT:
        The pseudo code is
        1. Find the next position in the tree using the binary representation of the total number of nodes
            1. You will have to explicitly store the size of your heap in a variable (rather than compute it) to maintain the O(log n) runtime
            1. See https://stackoverflow.com/questions/18241192/implement-heap-using-a-binary-tree for hints
        1. Add `value` into the next position
        1. Recursively swap value with its parent until the heap property is satisfied

        HINT:
        Create a @staticmethod helper function,
        following the same pattern used in the BST and AVLTree insert functions.
        '''
        self.num_nodes += 1
        binary_str = bin(self.num_nodes)[3:]

        if not self.root:
            self.root = Node(value)
        else:
            Heap._insert(self.root, value, binary_str)

    @staticmethod
    def _insert(node, value, binary_str):
        if binary_str[0] == '0':
            if node.left is None:
                node.left = Node(value)
            else:
                Heap._insert(node.left, value, binary_str[1:])
            if node.value > node.left.value:
                node.value, node.left.value = node.left.value, node.value
        elif binary_str[0] == '1':
            if node.right is None:
                node.right = Node(value)
            else:
                Heap._insert(node.right, value, binary_str[1:])
            if node.value > node.right.value:
                node.value, node.right.value = node.right.value, node.value

    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.

        FIXME:
        Implement this function.
        '''
        for x in xs:
            self.insert(x)

    def find_smallest(self):
        '''
        Returns the smallest value in the tree.

        FIXME:
        Implement this function.
        '''
        if self.root:
            return self.root.value

    def remove_min(self):
        '''
        Removes the minimum value from the Heap.
        If the heap is empty, it does nothing.

        FIXME:
        Implement this function.

        HINT:
        The pseudocode is
        1. remove the bottom right node from the tree
        2. replace the root node with what was formerly the bottom right
        3. "trickle down" the root node: recursively swap it with its largest child until the heap property is satisfied

        HINT:
        I created two @staticmethod helper functions: _remove_bottom_right and _trickle.
        It's possible to do it with only a single helper (or no helper at all),
        but I personally found dividing up the code into two made the most sense.
        '''
        if self.num_nodes == 1:
            self.root = None
            self.num_nodes -= 1
        else:
            binary_str = bin(self.num_nodes)[3:]
            newvalue = Heap._find_bottom_right(self.root, binary_str)
            self.root.value = newvalue
            Heap._remove_bottom_right(self.root, binary_str)
            Heap._trickle(self.root)
            self.num_nodes -= 1

    @staticmethod
    def _trickle(node):
        while node.left or node.right:
            if node.right is None or node.left.value < node.right.value:
                min_new_node = node.left
            else:
                min_new_node = node.right
            if node.value > min_new_node.value:
                node.value, min_new_node.value = min_new_node.value, node.value
                node = min_new_node
            else:
                break

    @staticmethod
    def _remove_bottom_right(node, binary_str):
        path = binary_str[:-1]
        curr_node = node
        for direction in path:
            if direction == "0":
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right
        if binary_str[-1] == "0":
            new_node = curr_node.left
            curr_node.left = None
        else:
            new_node = curr_node.right
            curr_node.right = None
        return new_node.value

    @staticmethod
    def _find_bottom_right(node, binary_str):
        path = binary_str[:-1]
        curr_node = node
        for direction in path:
            if direction == "0":
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right
        if binary_str[-1] == "0":
            return Heap._find_deepest_right(curr_node.left)
        else:
            return Heap._find_deepest_right(curr_node.right)

    @staticmethod
    def _find_deepest_right(node):
        if not node.right:
            return node.value
        else:
            return Heap._find_deepest_right(node.right)
