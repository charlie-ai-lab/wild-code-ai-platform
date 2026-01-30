"""
算法实现 - TDD Green Phase
"""


def quick_sort(arr):
    """快速排序实现"""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def inorder_traversal(data):
    """
    二叉树中序遍历
    data: 层序表示的数组，-1表示空节点
    """
    if not data or data[0] == -1:
        return []
    
    # 构建树
    class TreeNode:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None
    
    nodes = [None if val == -1 else TreeNode(val) for val in data]
    kids = iter(nodes[1:])
    for node in nodes:
        if node is not None:
            try:
                left = next(kids)
                node.left = left
            except StopIteration:
                break
            try:
                right = next(kids)
                node.right = right
            except StopIteration:
                break
    
    # 中序遍历
    result = []
    def traverse(node):
        if node:
            traverse(node.left)
            result.append(node.val)
            traverse(node.right)
    traverse(nodes[0])
    return result


def merge_sort(arr):
    """归并排序实现"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


if __name__ == "__main__":
    print("=== 算法实现 ===")
    print(f"Quick Sort: {quick_sort([3, 1, 4, 1, 5, 9, 2, 6])}")
    print(f"Inorder: {inorder_traversal([1, 2, 3])}")
    print(f"Merge Sort: {merge_sort([38, 27, 43, 3, 9, 82, 10])}")
