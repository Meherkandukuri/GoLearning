package main

func rotateRight(head *ListNode, k int) *ListNode {
	if head == nil || head.Next == nil || k == 0 {
		return head
	}

	// Find the length and the tail
	length := 1
	tail := head
	for tail.Next != nil {
		tail = tail.Next
		length++
	}

	// Make the list circular
	tail.Next = head

	// Find the new tail: (length - k % length - 1)th node
	k = k % length
	if k == 0 {
		tail.Next = nil // Break the circle
		return head
	}

	stepsToNewTail := length - k
	newTail := head
	for i := 1; i < stepsToNewTail; i++ {
		newTail = newTail.Next
	}

	// Set the new head and break the circle
	newHead := newTail.Next
	newTail.Next = nil

	return newHead
}
