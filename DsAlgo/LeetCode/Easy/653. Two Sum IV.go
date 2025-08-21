package main

func findTarget(root *TreeNode, k int) bool {
	return dfs(root, k, map[int]struct{}{})
}

func dfs(root *TreeNode, k int, m map[int]struct{}) bool {
	if root == nil {
		return false
	}

	if _, ok := m[k-root.Val]; ok {
		return true
	}

	m[root.Val] = struct{}{}
	return dfs(root.Left, k, m) || dfs(root.Right, k, m)

}

type TreeNode struct {
	Left  *TreeNode
	Val   int
	Right *TreeNode
}
