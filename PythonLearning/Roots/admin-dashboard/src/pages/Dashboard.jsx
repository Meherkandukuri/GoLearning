import React, { useState, useEffect } from "react";
import { Package, ShoppingCart, MessageSquare, TrendingUp } from "lucide-react";
import { productsApi, ordersApi } from "../services/api";
import toast from "react-hot-toast";

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalProducts: 0,
    totalOrders: 0,
    pendingOrders: 0,
    todayRevenue: 0,
  });
  const [loading, setLoading] = useState(true);
  const [recentOrders, setRecentOrders] = useState([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [productsRes, ordersRes] = await Promise.all([
        productsApi.getAll(),
        ordersApi.getAll(),
      ]);

      const products = productsRes.data;
      const orders = ordersRes.data;

      // Calculate stats
      const totalProducts = products.length;
      const totalOrders = orders.length;
      const pendingOrders = orders.filter((order) =>
        ["new", "confirmed", "preparing"].includes(order.status)
      ).length;

      // Calculate today's revenue
      const today = new Date().toISOString().split("T")[0];
      const todayOrders = orders.filter((order) =>
        order.created_at.startsWith(today)
      );
      const todayRevenue = todayOrders.reduce((sum, order) => {
        return (
          sum +
          order.items.reduce(
            (itemSum, item) => itemSum + item.quantity * item.price_each,
            0
          )
        );
      }, 0);

      setStats({
        totalProducts,
        totalOrders,
        pendingOrders,
        todayRevenue,
      });

      // Get recent orders (last 5)
      setRecentOrders(orders.slice(0, 5));
    } catch (error) {
      console.error("Error fetching dashboard data:", error);
      toast.error("Failed to load dashboard data");
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    {
      title: "Total Products",
      value: stats.totalProducts,
      icon: Package,
      color: "blue",
    },
    {
      title: "Total Orders",
      value: stats.totalOrders,
      icon: ShoppingCart,
      color: "green",
    },
    {
      title: "Pending Orders",
      value: stats.pendingOrders,
      icon: MessageSquare,
      color: "yellow",
    },
    {
      title: "Today's Revenue",
      value: `₹${stats.todayRevenue.toFixed(2)}`,
      icon: TrendingUp,
      color: "purple",
    },
  ];

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
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Welcome to Roots Admin Dashboard</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="card">
              <div className="flex items-center">
                <div className={`p-3 rounded-lg bg-${stat.color}-50`}>
                  <Icon className={`h-6 w-6 text-${stat.color}-600`} />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">
                    {stat.title}
                  </p>
                  <p className="text-2xl font-bold text-gray-900">
                    {stat.value}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Recent Orders */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Recent Orders
        </h2>
        {recentOrders.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No orders yet</p>
        ) : (
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
                </tr>
              </thead>
              <tbody>
                {recentOrders.map((order) => (
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
                        className={`status-badge ${getStatusBadge(
                          order.status
                        )}`}
                      >
                        {order.status}
                      </span>
                    </td>
                    <td className="text-sm text-gray-500">
                      {new Date(order.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Quick Actions
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <a
            href="/products"
            className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <div className="flex items-center gap-3">
              <Package className="h-8 w-8 text-blue-600" />
              <div>
                <h3 className="font-medium">Manage Products</h3>
                <p className="text-sm text-gray-500">
                  Add, edit, or remove products
                </p>
              </div>
            </div>
          </a>
          <a
            href="/orders"
            className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <div className="flex items-center gap-3">
              <ShoppingCart className="h-8 w-8 text-green-600" />
              <div>
                <h3 className="font-medium">View Orders</h3>
                <p className="text-sm text-gray-500">Track and manage orders</p>
              </div>
            </div>
          </a>
          <a
            href="/whatsapp"
            className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <div className="flex items-center gap-3">
              <MessageSquare className="h-8 w-8 text-purple-600" />
              <div>
                <h3 className="font-medium">WhatsApp Tools</h3>
                <p className="text-sm text-gray-500">
                  Send messages and broadcasts
                </p>
              </div>
            </div>
          </a>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
