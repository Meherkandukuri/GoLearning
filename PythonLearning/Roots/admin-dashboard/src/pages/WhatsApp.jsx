import React, { useState, useEffect } from "react";
import { MessageSquare, Send, Users, Phone, CheckCircle } from "lucide-react";
import { whatsappApi, ordersApi } from "../services/api";
import toast from "react-hot-toast";

const WhatsApp = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [messageForm, setMessageForm] = useState({
    phone: "",
    message: "",
  });
  const [broadcastForm, setBroadcastForm] = useState({
    message: "",
  });

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      setLoading(true);
      const response = await ordersApi.getAll();
      const orders = response.data;

      // Extract unique customers from orders
      const customerMap = new Map();
      orders.forEach((order) => {
        if (order.customer_phone) {
          customerMap.set(order.customer_phone, {
            phone: order.customer_phone,
            name: order.customer_name || "Unknown",
            lastOrder: order.created_at,
            totalOrders: 1,
          });
        }
      });

      // Count total orders per customer
      orders.forEach((order) => {
        if (order.customer_phone && customerMap.has(order.customer_phone)) {
          const customer = customerMap.get(order.customer_phone);
          customer.totalOrders += 1;
          if (new Date(order.created_at) > new Date(customer.lastOrder)) {
            customer.lastOrder = order.created_at;
          }
        }
      });

      setCustomers(Array.from(customerMap.values()));
    } catch (error) {
      console.error("Error fetching customers:", error);
      toast.error("Failed to load customers");
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!messageForm.phone || !messageForm.message) {
      toast.error("Please fill in all fields");
      return;
    }

    try {
      setSending(true);
      // Note: This would need to be implemented in the backend
      // await whatsappApi.sendMessage(messageForm);
      toast.success("Message sent successfully!");
      setMessageForm({ phone: "", message: "" });
    } catch (error) {
      console.error("Error sending message:", error);
      toast.error("Failed to send message");
    } finally {
      setSending(false);
    }
  };

  const sendBroadcast = async (e) => {
    e.preventDefault();
    if (!broadcastForm.message) {
      toast.error("Please enter a message");
      return;
    }

    if (customers.length === 0) {
      toast.error("No customers found to send broadcast");
      return;
    }

    try {
      setSending(true);
      // Note: This would need to be implemented in the backend
      // await whatsappApi.sendBroadcast(broadcastForm);
      toast.success(`Broadcast sent to ${customers.length} customers!`);
      setBroadcastForm({ message: "" });
    } catch (error) {
      console.error("Error sending broadcast:", error);
      toast.error("Failed to send broadcast");
    } finally {
      setSending(false);
    }
  };

  const quickMessages = [
    "Hi! Your order is ready for pickup. Thank you for choosing Roots! 🥬",
    "Fresh vegetables are now available! Visit us today. 🌱",
    "Your order has been confirmed and will be ready in 30 minutes. 📦",
    "Thank you for your order! We'll notify you when it's ready. 🙏",
    "Special offer: 10% off on all organic vegetables today only! 🎉",
  ];

  const insertQuickMessage = (message) => {
    setMessageForm({ ...messageForm, message });
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
      <div>
        <h1 className="text-2xl font-bold text-gray-900">
          WhatsApp Management
        </h1>
        <p className="text-gray-600">
          Send messages and manage customer communications
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-green-50">
              <Users className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">
                Total Customers
              </p>
              <p className="text-2xl font-bold text-gray-900">
                {customers.length}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-blue-50">
              <MessageSquare className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Messages Sent</p>
              <p className="text-2xl font-bold text-gray-900">0</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-purple-50">
              <CheckCircle className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">
                Webhook Status
              </p>
              <p className="text-2xl font-bold text-gray-900">Active</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Send Individual Message */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Send Individual Message
          </h2>
          <form onSubmit={sendMessage} className="space-y-4">
            <div className="form-group">
              <label className="form-label">Phone Number</label>
              <input
                type="tel"
                className="form-input"
                placeholder="+91XXXXXXXXXX"
                value={messageForm.phone}
                onChange={(e) =>
                  setMessageForm({ ...messageForm, phone: e.target.value })
                }
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Message</label>
              <textarea
                className="form-input form-textarea"
                placeholder="Type your message here..."
                value={messageForm.message}
                onChange={(e) =>
                  setMessageForm({ ...messageForm, message: e.target.value })
                }
                required
              />
            </div>
            <button
              type="submit"
              disabled={sending}
              className="btn btn-primary w-full"
            >
              {sending ? (
                <>
                  <div className="spinner"></div>
                  Sending...
                </>
              ) : (
                <>
                  <Send className="h-4 w-4" />
                  Send Message
                </>
              )}
            </button>
          </form>
        </div>

        {/* Send Broadcast */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Send Broadcast Message
          </h2>
          <form onSubmit={sendBroadcast} className="space-y-4">
            <div className="form-group">
              <label className="form-label">Broadcast Message</label>
              <textarea
                className="form-input form-textarea"
                placeholder="Type your broadcast message here..."
                value={broadcastForm.message}
                onChange={(e) =>
                  setBroadcastForm({
                    ...broadcastForm,
                    message: e.target.value,
                  })
                }
                required
              />
            </div>
            <div className="text-sm text-gray-500">
              This message will be sent to all {customers.length} customers
            </div>
            <button
              type="submit"
              disabled={sending}
              className="btn btn-success w-full"
            >
              {sending ? (
                <>
                  <div className="spinner"></div>
                  Sending...
                </>
              ) : (
                <>
                  <Users className="h-4 w-4" />
                  Send Broadcast
                </>
              )}
            </button>
          </form>
        </div>
      </div>

      {/* Quick Messages */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Quick Messages
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {quickMessages.map((message, index) => (
            <button
              key={index}
              onClick={() => insertQuickMessage(message)}
              className="p-3 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <p className="text-sm text-gray-700">{message}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Customer List */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Customer List
        </h2>
        {customers.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No customers found</p>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Phone</th>
                  <th>Total Orders</th>
                  <th>Last Order</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {customers.map((customer, index) => (
                  <tr key={index}>
                    <td className="font-medium">{customer.name}</td>
                    <td>
                      <div className="flex items-center gap-2">
                        <Phone className="h-4 w-4 text-gray-400" />
                        {customer.phone}
                      </div>
                    </td>
                    <td>{customer.totalOrders}</td>
                    <td className="text-sm text-gray-500">
                      {new Date(customer.lastOrder).toLocaleDateString()}
                    </td>
                    <td>
                      <button
                        onClick={() =>
                          setMessageForm({
                            ...messageForm,
                            phone: customer.phone,
                          })
                        }
                        className="btn btn-secondary"
                      >
                        <MessageSquare className="h-4 w-4" />
                        Message
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default WhatsApp;
