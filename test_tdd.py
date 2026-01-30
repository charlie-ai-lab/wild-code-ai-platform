"""
TDD实践 - 基准测试算法改进
"""
import algorithms


def test_quick_sort():
    """测试快速排序实现"""
    input_data = [3, 1, 4, 1, 5, 9, 2, 6]
    expected = [1, 1, 2, 3, 4, 5, 6, 9]
    result = algorithms.quick_sort(input_data)
    assert result == expected, f"Expected {expected}, got {result}"
    print("✅ test_quick_sort PASSED")


def test_binary_tree_traversal():
    """测试二叉树中序遍历"""
    input_data = [1, 2, 3]  # 层序表示
    expected = [2, 1, 3]
    result = algorithms.inorder_traversal(input_data)
    assert result == expected, f"Expected {expected}, got {result}"
    print("✅ test_binary_tree_traversal PASSED")


def test_merge_sort():
    """测试归并排序实现"""
    input_data = [38, 27, 43, 3, 9, 82, 10]
    expected = [3, 9, 10, 27, 38, 43, 82]
    result = algorithms.merge_sort(input_data)
    assert result == expected, f"Expected {expected}, got {result}"
    print("✅ test_merge_sort PASSED")


if __name__ == "__main__":
    print("=== 运行TDD测试 (Green Phase) ===\n")
    
    tests = [
        ("Quick Sort", test_quick_sort),
        ("Binary Tree", test_binary_tree_traversal),
        ("Merge Sort", test_merge_sort),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except (AssertionError, Exception) as e:
            print(f"❌ {name} FAILED: {e}")
            failed += 1
    
    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}")
    print(f"失败: {failed}")
    
    if passed == 3:
        print("\n🎉 Green Phase完成！所有测试通过")
        print("下一步: Refactor Phase - 优化代码")
