import React, { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from "recharts";
import { TrendingUp, Package, ShoppingCart, DollarSign } from "lucide-react";
import { productsApi, ordersApi } from "../services/api";
import toast from "react-hot-toast";

const Analytics = () => {
  const [analytics, setAnalytics] = useState({
    totalRevenue: 0,
    totalOrders: 0,
    totalProducts: 0,
    averageOrderValue: 0,
  });
  const [loading, setLoading] = useState(true);
  const [salesData, setSalesData] = useState([]);
  const [productData, setProductData] = useState([]);
  const [orderStatusData, setOrderStatusData] = useState([]);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const [productsRes, ordersRes] = await Promise.all([
        productsApi.getAll(),
        ordersApi.getAll(),
      ]);

      const products = productsRes.data;
      const orders = ordersRes.data;

      // Calculate basic analytics
      const totalRevenue = orders.reduce((sum, order) => {
        return (
          sum +
          order.items.reduce(
            (itemSum, item) => itemSum + item.quantity * item.price_each,
            0
          )
        );
      }, 0);

      const totalOrders = orders.length;
      const totalProducts = products.length;
      const averageOrderValue =
        totalOrders > 0 ? totalRevenue / totalOrders : 0;

      setAnalytics({
        totalRevenue,
        totalOrders,
        totalProducts,
        averageOrderValue,
      });

      // Prepare sales data (last 7 days)
      const last7Days = [];
      for (let i = 6; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        const dateStr = date.toISOString().split("T")[0];

        const dayOrders = orders.filter((order) =>
          order.created_at.startsWith(dateStr)
        );

        const dayRevenue = dayOrders.reduce((sum, order) => {
          return (
            sum +
            order.items.reduce(
              (itemSum, item) => itemSum + item.quantity * item.price_each,
              0
            )
          );
        }, 0);

        last7Days.push({
          date: date.toLocaleDateString("en-US", { weekday: "short" }),
          revenue: dayRevenue,
          orders: dayOrders.length,
        });
      }

      setSalesData(last7Days);

      // Prepare product data (top selling products)
      const productSales = {};
      orders.forEach((order) => {
        order.items.forEach((item) => {
          if (productSales[item.product_name]) {
            productSales[item.product_name] += item.quantity;
          } else {
            productSales[item.product_name] = item.quantity;
          }
        });
      });

      const topProducts = Object.entries(productSales)
        .map(([name, quantity]) => ({ name, quantity }))
        .sort((a, b) => b.quantity - a.quantity)
        .slice(0, 5);

      setProductData(topProducts);

      // Prepare order status data
      const statusCounts = {};
      orders.forEach((order) => {
        statusCounts[order.status] = (statusCounts[order.status] || 0) + 1;
      });

      const statusData = Object.entries(statusCounts).map(
        ([status, count]) => ({
          status,
          count,
        })
      );

      setOrderStatusData(statusData);
    } catch (error) {
      console.error("Error fetching analytics:", error);
      toast.error("Failed to load analytics data");
    } finally {
      setLoading(false);
    }
  };

  const COLORS = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"];

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
        <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
        <p className="text-gray-600">
          Business insights and performance metrics
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-green-50">
              <DollarSign className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Revenue</p>
              <p className="text-2xl font-bold text-gray-900">
                ₹{analytics.totalRevenue.toFixed(2)}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-blue-50">
              <ShoppingCart className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Orders</p>
              <p className="text-2xl font-bold text-gray-900">
                {analytics.totalOrders}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-purple-50">
              <Package className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">
                Total Products
              </p>
              <p className="text-2xl font-bold text-gray-900">
                {analytics.totalProducts}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-yellow-50">
              <TrendingUp className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">
                Avg Order Value
              </p>
              <p className="text-2xl font-bold text-gray-900">
                ₹{analytics.averageOrderValue.toFixed(2)}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sales Trend */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Sales Trend (Last 7 Days)
          </h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={salesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip
                  formatter={(value, name) => [
                    name === "revenue" ? `₹${value.toFixed(2)}` : value,
                    name === "revenue" ? "Revenue" : "Orders",
                  ]}
                />
                <Line
                  type="monotone"
                  dataKey="revenue"
                  stroke="#3b82f6"
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="orders"
                  stroke="#10b981"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Order Status Distribution */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Order Status Distribution
          </h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={orderStatusData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ status, count }) => `${status}: ${count}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {orderStatusData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Top Selling Products */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Top Selling Products
        </h2>
        {productData.length === 0 ? (
          <p className="text-gray-500 text-center py-8">
            No sales data available
          </p>
        ) : (
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={productData} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" width={100} />
                <Tooltip />
                <Bar dataKey="quantity" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Insights */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Insights</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-blue-50 rounded-lg">
            <h3 className="font-medium text-blue-900 mb-2">Revenue Growth</h3>
            <p className="text-sm text-blue-700">
              {analytics.totalRevenue > 0
                ? "Your store is generating consistent revenue. Keep up the great work!"
                : "Start by adding products and processing orders to see revenue growth."}
            </p>
          </div>

          <div className="p-4 bg-green-50 rounded-lg">
            <h3 className="font-medium text-green-900 mb-2">
              Customer Engagement
            </h3>
            <p className="text-sm text-green-700">
              {analytics.totalOrders > 0
                ? `You have ${analytics.totalOrders} orders. Consider implementing customer loyalty programs.`
                : "Focus on marketing and customer acquisition to increase orders."}
            </p>
          </div>

          <div className="p-4 bg-yellow-50 rounded-lg">
            <h3 className="font-medium text-yellow-900 mb-2">
              Product Performance
            </h3>
            <p className="text-sm text-yellow-700">
              {productData.length > 0
                ? `${productData[0]?.name} is your top-selling product. Consider promoting it more.`
                : "Add more products to your catalog to increase sales opportunities."}
            </p>
          </div>

          <div className="p-4 bg-purple-50 rounded-lg">
            <h3 className="font-medium text-purple-900 mb-2">
              Order Efficiency
            </h3>
            <p className="text-sm text-purple-700">
              {analytics.averageOrderValue > 0
                ? `Your average order value is ₹${analytics.averageOrderValue.toFixed(
                    2
                  )}. Consider upselling strategies.`
                : "Focus on increasing order values through product bundles and promotions."}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
