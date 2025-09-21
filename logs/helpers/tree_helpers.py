from collections import deque


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def build_tree_level_order(nodes):
    """
    Builds a binary tree from a list representation (level-order traversal).
    """
    if not nodes or nodes[0] == -1:
        return None

    root = TreeNode(nodes[0])
    q = deque([root])
    i = 1

    while q and i < len(nodes):
        current_node = q.popleft()

        # Process left child
        if i < len(nodes) and nodes[i] != -1:
            left_child = TreeNode(nodes[i])
            current_node.left = left_child
            q.append(left_child)
        i += 1

        # Process right child
        if i < len(nodes) and nodes[i] != -1:
            right_child = TreeNode(nodes[i])
            current_node.right = right_child
            q.append(right_child)
        i += 1

    return root


def build_tree_pre_order(nodes) -> TreeNode:
    """
    Builds a binary tree from a list representation (pre-order traversal).
    '-1' values in the list denote missing nodes.

    Args:
        nodes: A list of integers and -1 values.

    Returns:
        The root of the constructed binary tree.
    """
    if not nodes:
        return None

    def helper(it):
        val = next(it)
        if val == -1:
            return None
        node = TreeNode(val)
        node.left = helper(it)
        node.right = helper(it)
        return node

    return helper(iter(nodes))


def print_tree(root, prefix="", is_left=True):
    if root is not None:
        print(prefix + ("└── " if is_left else "┌── ") + str(root.val))
        # If there are children, print them
        if root.left or root.right:
            if root.right:
                print_tree(root.right, prefix + ("    " if is_left else "│   "), False)
            else:
                # Explicit None for right child
                print(prefix + ("    " if is_left else "│   ") + "┌── None")

            if root.left:
                print_tree(root.left, prefix + ("    " if is_left else "│   "), True)
            else:
                # Explicit None for left child
                print(prefix + ("    " if is_left else "│   ") + "└── None")
    else:
        print(prefix + ("└── " if is_left else "┌── ") + "None")
