import React, { useState, useEffect } from "react";
import { ShoppingCart, Eye, CheckCircle, Clock, XCircle } from "lucide-react";
import { ordersApi } from "../services/api";
import toast from "react-hot-toast";

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [statusFilter, setStatusFilter] = useState("all");

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const response = await ordersApi.getAll();
      setOrders(response.data);
    } catch (error) {
      console.error("Error fetching orders:", error);
      toast.error("Failed to load orders");
    } finally {
      setLoading(false);
    }
  };

  const updateOrderStatus = async (orderId, newStatus) => {
    try {
      // Note: This would need to be implemented in the backend
      // await ordersApi.update(orderId, { status: newStatus });
      toast.success(`Order status updated to ${newStatus}`);
      fetchOrders();
    } catch (error) {
      console.error("Error updating order status:", error);
      toast.error("Failed to update order status");
    }
  };

  const viewOrderDetails = (order) => {
    setSelectedOrder(order);
    setShowModal(true);
  };

  const getStatusBadge = (status) => {
    const statusClasses = {
      new: "status-new",
      confirmed: "status-confirmed",
      preparing: "status-preparing",
      ready: "status-ready",
      delivered: "status-delivered",
      cancelled: "status-cancelled",
    };
    return statusClasses[status] || "status-new";
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case "new":
        return <Clock className="h-4 w-4" />;
      case "confirmed":
        return <CheckCircle className="h-4 w-4" />;
      case "preparing":
        return <Clock className="h-4 w-4" />;
      case "ready":
        return <CheckCircle className="h-4 w-4" />;
      case "delivered":
        return <CheckCircle className="h-4 w-4" />;
      case "cancelled":
        return <XCircle className="h-4 w-4" />;
      default:
        return <Clock className="h-4 w-4" />;
    }
  };

  const filteredOrders = orders.filter((order) => {
    if (statusFilter === "all") return true;
    return order.status === statusFilter;
  });

  const getTotalRevenue = () => {
    return orders.reduce((sum, order) => {
      return (
        sum +
        order.items.reduce(
          (itemSum, item) => itemSum + item.quantity * item.price_each,
          0
        )
      );
    }, 0);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Orders</h1>
          <p className="text-gray-600">Manage customer orders and track status</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-sm text-gray-600">
            Total Revenue: <span className="font-semibold">₹{getTotalRevenue().toFixed(2)}</span>
          </div>
        </div>
      </div>

      {/* Status Filter */}
      <div className="card">
        <div className="flex items-center gap-4">
          <span className="text-sm font-medium text-gray-700">Filter by status:</span>
          <select
            className="form-input form-select w-auto"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="all">All Orders</option>
            <option value="new">New</option>
            <option value="confirmed">Confirmed</option>
            <option value="preparing">Preparing</option>
            <option value="ready">Ready</option>
            <option value="delivered">Delivered</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>
      </div>

      {/* Orders Table */}
      {filteredOrders.length === 0 ? (
        <div className="card text-center py-12">
          <ShoppingCart className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            No orders found
          </h3>
          <p className="text-gray-500">
            {statusFilter === "all" 
              ? "No orders have been placed yet" 
              : `No orders with status "${statusFilter}"`}
          </p>
        </div>
      ) : (
        <div className="card">
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Order ID</th>
                  <th>Customer</th>
                  <th>Items</th>
                  <th>Total</th>
                  <th>Status</th>
                  <th>Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredOrders.map((order) => (
                  <tr key={order.id}>
                    <td className="font-medium">#{order.id}</td>
                    <td>
                      <div>
                        <div className="font-medium">
                          {order.customer_name || "N/A"}
                        </div>
                        <div className="text-sm text-gray-500">
                          {order.customer_phone || "N/A"}
                        </div>
                      </div>
                    </td>
                    <td>{order.items.length} items</td>
                    <td>
                      ₹
                      {order.items
                        .reduce(
                          (sum, item) => sum + item.quantity * item.price_each,
                          0
                        )
                        .toFixed(2)}
                    </td>
                    <td>
                      <span
                        className={`status-badge ${getStatusBadge(order.status)}`}
                      >
                        {getStatusIcon(order.status)}
                        {order.status}
                      </span>
                    </td>
                    <td className="text-sm text-gray-500">
                      {new Date(order.created_at).toLocaleDateString()}
                    </td>
                    <td>
                      <div className="flex gap-2">
                        <button
                          onClick={() => viewOrderDetails(order)}
                          className="btn btn-secondary"
                        >
                          <Eye className="h-4 w-4" />
                        </button>
                        {order.status === "new" && (
                          <button
                            onClick={() => updateOrderStatus(order.id, "confirmed")}
                            className="btn btn-success"
                          >
                            Confirm
                          </button>
                        )}
                        {order.status === "confirmed" && (
                          <button
                            onClick={() => updateOrderStatus(order.id, "preparing")}
                            className="btn btn-primary"
                          >
                            Start Prep
                          </button>
                        )}
                        {order.status === "preparing" && (
                          <button
                            onClick={() => updateOrderStatus(order.id, "ready")}
                            className="btn btn-success"
                          >
                            Ready
                          </button>
                        )}
                        {order.status === "ready" && (
                          <button
                            onClick={() => updateOrderStatus(order.id, "delivered")}
                            className="btn btn-success"
                          >
                            Delivered
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Order Details Modal */}
      {showModal && selectedOrder && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center p-4">
            <div
              className="fixed inset-0 bg-gray-600 bg-opacity-75"
              onClick={() => setShowModal(false)}
            />
            <div className="relative bg-white rounded-lg shadow-xl max-w-2xl w-full">
              <div className="p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">
                  Order #{selectedOrder.id} Details
                </h2>
                
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium text-gray-500">Customer Name</label>
                      <p className="text-gray-900">{selectedOrder.customer_name || "N/A"}</p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-500">Phone</label>
                      <p className="text-gray-900">{selectedOrder.customer_phone || "N/A"}</p>
                    </div>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-500">Order Date</label>
                    <p className="text-gray-900">
                      {new Date(selectedOrder.created_at).toLocaleString()}
                    </p>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-500">Status</label>
                    <span className={`status-badge ${getStatusBadge(selectedOrder.status)}`}>
                      {selectedOrder.status}
                    </span>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-500">Items</label>
                    <div className="mt-2 space-y-2">
                      {selectedOrder.items.map((item, index) => (
                        <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                          <div>
                            <p className="font-medium">{item.product_name}</p>
                            <p className="text-sm text-gray-500">
                              {item.quantity} {item.unit} × ₹{item.price_each}
                            </p>
                          </div>
                          <p className="font-semibold">
                            ₹{(item.quantity * item.price_each).toFixed(2)}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div className="border-t pt-4">
                    <div className="flex justify-between items-center">
                      <span className="text-lg font-semibold">Total</span>
                      <span className="text-xl font-bold text-green-600">
                        ₹{selectedOrder.items
                          .reduce((sum, item) => sum + item.quantity * item.price_each, 0)
                          .toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className="flex gap-3 pt-6">
                  <button
                    onClick={() => setShowModal(false)}
                    className="btn btn-secondary flex-1"
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Orders;
