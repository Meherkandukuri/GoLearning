package Medium

func removeNthFromEnd(head *ListNode, n int) *ListNode {

	node := head
	lenNode := 1

	for node.Next != nil {
		node = node.Next
		lenNode += 1
	}

	if lenNode == 1 {
		return nil
	} else if lenNode == 2 && n == 1 {
		head.Next = nil
		return head
	} else if lenNode == 2 && n == 2 {
		node = head.Next
		return node
	}

	node = head
	for i := 1; i <= lenNode-n; i++ {
		node = node.Next
	}

	if node.Next.Next != nil {
		node.Next = node.Next.Next
	} else {
		node.Next = nil
	}
	return head
}
