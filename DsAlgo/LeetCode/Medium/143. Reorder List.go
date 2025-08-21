package main

/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func reorderList(head *ListNode) {

	if head == nil || head.Next == nil {
		return
	}

	// find the middle node
	slow, fast := head, head
	for fast != nil && fast.Next != nil {
		slow = slow.Next
		fast = fast.Next.Next
	}

	prev, curr := (*ListNode)(nil), slow.Next
	slow.Next = nil
	for curr != nil {
		next := curr.Next
		curr.Next = prev
		prev = curr
		curr = next
	}

	// 3. Merge Two halves
	first, second := head, prev
	for second != nil {
		tmp1, tmp2 := first.Next, second.Next

		first.Next = second
		second.Next = tmp1

		first = tmp1
		second = tmp2
	}

}
