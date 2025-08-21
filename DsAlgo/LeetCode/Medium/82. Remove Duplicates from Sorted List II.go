package Medium

/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
type ListNode struct {
	Val  int
	Next *ListNode
}

func deleteDuplicates(head *ListNode) *ListNode {

	dummy := &ListNode{Next: head}
	curr := head
	prev := dummy

	for curr != nil {

		duplicate := false
		for curr.Next != nil && curr.Val == curr.Next.Val {
			duplicate = true
			curr = curr.Next
		}
		if duplicate {
			prev.Next = curr.Next
		} else {
			prev = prev.Next
		}
		curr = curr.Next

	}

	return dummy.Next

}
