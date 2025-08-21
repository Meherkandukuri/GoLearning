package main

func isPalindromeLinkedList(head *ListNode) bool {

	if head == nil || head.Next == nil {
		return true
	}

	slow, fast := head, head

	for fast != nil && fast.Next != nil {
		slow = slow.Next
		fast = fast.Next.Next
	}

	if fast != nil {
		slow = slow.Next
	}

	prev, curr := (*ListNode)(nil), slow

	for curr != nil {

		next := curr.Next
		curr.Next = prev
		prev = curr
		curr = next

	}

	right, left := prev, head
	for right != nil {
		if right.Val != left.Val {
			return false
		}

		left = left.Next
		right = right.Next
	}

	return true

}
