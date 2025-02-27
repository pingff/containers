'''
This file implements the AVL Tree data structure.
The functions in this file are considerably harder than the
functions in the BinaryTree and BST files,
but there are fewer of them.
'''

from containers.BinaryTree import BinaryTree, Node
from containers.BST import BST


class AVLTree(BST):
    '''
    FIXME:
    AVLTree is currently not a subclass of BST.
    You should make the necessary changes in the class declaration line above
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        Implement this function.
        '''
        super().__init__()

    def balance_factor(self):
        '''
        Returns the balance factor of a tree.
        '''
        return AVLTree._balance_factor(self.root)

    @staticmethod
    def _balance_factor(node):
        '''
        Returnsthe balance factor of a node.
        '''
        if node is None:
            return 0
        return BinaryTree._height(node.left) - BinaryTree._height(node.right)

    def is_avl_satisfied(self):
        '''
        Returns True if the avl tree satisfies that all nodes
        have a balance factor in [-1,0,1].
        '''
        return AVLTree._is_avl_satisfied(self.root)[0]

    @staticmethod
    def _is_avl_satisfied(node):
        '''
        FIXME:
        Implement this function.
        '''
        if node is None:
            return True, 0
        else:
            left_satisfied, left_height = AVLTree._is_avl_satisfied(node.left)
            right_satisfied, right_height = AVLTree._is_avl_satisfied(node.right)
            balanced = left_height - right_height in [-1, 0, 1]
            return (left_satisfied and right_satisfied and balanced, max(left_height, right_height) + 1)

    @staticmethod
    def _left_rotate(node):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of tree rotations,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code
        is fairly different from our class hierarchy,
        however, so you will have to adapt their code.
        '''
        root = node
        if root.right:
            new = Node(root.right.value)
            new.left = Node(root.value)
            new.right = root.right.right
            new.left.left = root.left
            new.left.right = root.right.left
            return new
        return root

    @staticmethod
    def _right_rotate(node):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of tree rotations,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL
        tree code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.
        '''
        root = node
        if root.left:
            new = Node(root.left.value)
            new.right = Node(root.value)
            new.left = root.left.left
            new.right.right = root.right
            new.right.left = root.left.right
            return new
        return root

    def insert(self, value):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level
        overview of how to insert into an AVL tree,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL
        tree code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.

        HINT:
        It is okay to add @staticmethod helper functions for this code.
        The code should look very similar to the code
        for your insert function for the BST,
        but it will also call the left and right rebalancing functions.
        '''
        if self.root is None:
            self.root = Node(value)
        else:
            self.root = AVLTree._insert(value, self.root)

    def insert_list(self, xs):
        for x in xs:
            self.insert(x)

    @staticmethod
    def _insert(value, node):
        if node:
            if value < node.value:
                if node.left is None:
                    node.left = Node(value)
                    return node.left
                else:
                    return AVLTree._insert(node.left, value)
            elif value > node.value:
                if node.right is None:
                    node.right = Node(value)
                    return node.right
                else:
                    return AVLTree._insert(node.right, value)
        if node is None:
            return Node(value)

    @staticmethod
    def _rebalance(node):
        '''
        There are no test cases for the rebalance function,
        so you do not technically have to implement it.
        But both the insert function needs the rebalancing code,
        so I recommend including that code here.
        '''
        balance_factor = AVLTree._balance_factor(node) if node else 0
        if balance_factor > 1:
            if AVLTree._balance_factor(node.left) < 0:
                node.left = AVLTree._right_rotate(node.right)
            node = AVLTree._left_rotate(node)
        elif balance_factor < -1:
            if AVLTree._balance_factor(node.right) > 0:
                node.right = AVLTree._right_rotate(node.right)
            node = AVLTree._left_rotate(node)
        return node
