"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
from math import log2
import time
import random
from copy import deepcopy



class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            _s = ""
            if node != None:
                _s += recurse(node.right, level + 1)
                _s += "| " * level
                _s += str(node.data) + "\n"
                _s += recurse(node.left, level + 1)
            return _s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        newNode = BSTNode(item)
        if self.isEmpty():
            self._root = newNode
        else:
            currentNode = self._root
            while True:
                if item < currentNode.data:
                    if currentNode.left is None:
                        currentNode.left = newNode
                        break
                    else:
                        currentNode = currentNode.left
                else:
                    if currentNode.right is None:
                        currentNode.right = newNode
                        break
                    else:
                        currentNode = currentNode.right
        self._size += 1


    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            liftMaxInLeftSubtreeToTop(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of the tree.
        :return: int
        """
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return 0
            else:
                return 1 + max(height1(top.right), height1(top.left))
        if self._root.left or self._root.right:
            return height1(self._root) - 1
        else:
            return 0

    def is_balanced(self):
        """
        Return True if the tree is balanced.
        :return: bool
        """
        return self.height() < 2 * (log2(self._size + 2)) - 1

    def range_find(self, low, high):
        """
        Returns a list of items in the tree where low <= item <= high.
        :param low: The lower bound of the range.
        :param high: The upper bound of the range.
        :return: A list of items within the range.
        """
        result = []
        for element in self.inorder():
            if  high >= element >= low:
                result.append(element)
        return result
    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def build_tree(items):
            """
            Builds a balanced binary search tree from a sorted list of items.
            :param items: The sorted list of items.
            :return: The root node of the balanced tree.
            """
            if not items:
                return None

            mid = len(items) // 2
            root = BSTNode(items[mid])
            root.left = build_tree(items[:mid])
            root.right = build_tree(items[mid + 1:])
            return root

        # Get a sorted list of all items in the tree
        sorted_items = list(self.inorder())

        # Rebuild the tree with the sorted items
        self._root = build_tree(sorted_items)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def find_successor(node, target):
            """
            Recursive helper function to find the successor.
            :param node: The current node.
            :param target: The target item.
            :return: The successor item, or None.
            """
            if node is None:
                return None

            if node.data <= target:
                return find_successor(node.right, target)
            else:
                left_result = find_successor(node.left, target)
                return left_result if left_result is not None else node.data

        return find_successor(self._root, item)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def find_predecessor(node, target):
            """
            Recursive helper function to find the predecessor.
            :param node: The current node.
            :param target: The target item.
            :return: The predecessor item, or None.
            """
            if node is None:
                return None

            if node.data >= target:
                return find_predecessor(node.left, target)
            else:
                right_result = find_predecessor(node.right, target)
                return right_result if right_result is not None else node.data

        return find_predecessor(self._root, item)


    def demo_bst(self, path):
        word_list = []

        with open(path, 'r') as file:
            for line in file:
                word_list.append(line.strip())
        word_list.sort()
        word_list = word_list[:994]

        rand_word_lst = []
        for _ in range(10000):
            rand_word_lst.append(random.choice(word_list))

        start = time.perf_counter()

        for word in rand_word_lst:
            word_list.index(word)
        end = time.perf_counter()
        print('Task1: Time for list: ', end - start)

        bst = LinkedBST()
        for word in word_list:
            bst.add(word)

        start = time.perf_counter()
        for word in rand_word_lst:
            bst.find(word)
        end = time.perf_counter()
        print('Task2: Time for bst: ', end - start)

        words_rand = deepcopy(word_list)
        random.shuffle(words_rand)
        bst1 = LinkedBST()
        for word in words_rand:
            bst1.add(word)

        start = time.perf_counter()
        for word in rand_word_lst:
            bst1.find(word)
        end = time.perf_counter()
        print('Task3: Time for bst shuffled: ', end - start)

        bst.rebalance()
        start = time.perf_counter()
        for word in rand_word_lst:
            bst.find(word)
        end = time.perf_counter()
        print('Task4: Time for rebalanced bst: ', end - start)


if __name__ == '__main__':
    bst = LinkedBST()
    bst.demo_bst('words.txt')
