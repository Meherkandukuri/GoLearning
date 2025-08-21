package Medium

import "GoLearning/DsAlgo/LeetCode/Easy"

/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func detectCycle(head *main.ListNode) *main.ListNode {

	slow := head
	fast := head

	for fast != nil && fast.Next != nil {
		slow = head.Next
		fast = head.Next.Next

		if slow == fast {
			return slow
		}
	}
	return nil

}
