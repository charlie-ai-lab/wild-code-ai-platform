"""
算法实现 - TDD Refactor Phase
优化版本
"""


def quick_sort(arr):
    """
    快速排序 - 原地排序版本
    
    Args:
        arr: 待排序列表
    
    Returns:
        排序后的新列表
    """
    if len(arr) <= 1:
        return arr
    
    # 选择中间元素作为基准，减少最坏情况
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)


def inorder_traversal(data):
    """
    二叉树中序遍历 - 简化版本
    
    Args:
        data: 层序表示的数组，-1表示空节点
    
    Returns:
        中序遍历结果列表
    """
    if not data or data[0] == -1:
        return []
    
    # 构建树
    class TreeNode:
        __slots__ = ['val', 'left', 'right']
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None
    
    nodes = [None if val == -1 else TreeNode(val) for val in data]
    
    # 链接子节点
    for i, node in enumerate(nodes):
        if node is not None:
            left_idx = 2 * i + 1
            right_idx = 2 * i + 2
            if left_idx < len(nodes):
                node.left = nodes[left_idx]
            if right_idx < len(nodes):
                node.right = nodes[right_idx]
    
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
    """
    归并排序 - 优化版本
    
    Args:
        arr: 待排序列表
    
    Returns:
        排序后的新列表
    """
    n = len(arr)
    if n <= 1:
        return arr
    
    mid = n // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # 合并两个有序列表
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# 性能测试
if __name__ == "__main__":
    import time
    
    test_cases = [
        ([3, 1, 4, 1, 5, 9, 2, 6], "小数组"),
        (list(range(100, 0, -1)), "逆序数组"),
        (list(range(1000)), "有序数组"),
    ]
    
    print("=== 性能测试 ===")
    for arr, name in test_cases:
        start = time.time()
        quick_sort(arr.copy())
        merge_sort(arr.copy())
        elapsed = time.time() - start
        print(f"{name}: {elapsed*1000:.2f}ms")
