import React, { useState, useEffect } from "react";
import { Plus, Edit, Trash2, Package } from "lucide-react";
import { productsApi } from "../services/api";
import toast from "react-hot-toast";

const Products = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    price: "",
    unit: "kg",
    in_stock: true,
  });

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await productsApi.getAll();
      setProducts(response.data);
    } catch (error) {
      console.error("Error fetching products:", error);
      toast.error("Failed to load products");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingProduct) {
        await productsApi.update(editingProduct.id, formData);
        toast.success("Product updated successfully");
      } else {
        await productsApi.create(formData);
        toast.success("Product created successfully");
      }
      setShowModal(false);
      setEditingProduct(null);
      setFormData({
        name: "",
        description: "",
        price: "",
        unit: "kg",
        in_stock: true,
      });
      fetchProducts();
    } catch (error) {
      console.error("Error saving product:", error);
      toast.error("Failed to save product");
    }
  };

  const handleEdit = (product) => {
    setEditingProduct(product);
    setFormData({
      name: product.name,
      description: product.description || "",
      price: product.price.toString(),
      unit: product.unit,
      in_stock: product.in_stock,
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this product?")) {
      try {
        await productsApi.delete(id);
        toast.success("Product deleted successfully");
        fetchProducts();
      } catch (error) {
        console.error("Error deleting product:", error);
        toast.error("Failed to delete product");
      }
    }
  };

  const openModal = () => {
    setEditingProduct(null);
    setFormData({
      name: "",
      description: "",
      price: "",
      unit: "kg",
      in_stock: true,
    });
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setEditingProduct(null);
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
          <h1 className="text-2xl font-bold text-gray-900">Products</h1>
          <p className="text-gray-600">Manage your vegetable inventory</p>
        </div>
        <button onClick={openModal} className="btn btn-primary">
          <Plus className="h-4 w-4" />
          Add Product
        </button>
      </div>

      {/* Products Grid */}
      {products.length === 0 ? (
        <div className="card text-center py-12">
          <Package className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            No products yet
          </h3>
          <p className="text-gray-500 mb-4">
            Get started by adding your first product
          </p>
          <button onClick={openModal} className="btn btn-primary">
            <Plus className="h-4 w-4" />
            Add Product
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <div key={product.id} className="card">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {product.name}
                  </h3>
                  <p className="text-sm text-gray-500 mb-2">
                    {product.description || "No description"}
                  </p>
                  <div className="flex items-center gap-4">
                    <span className="text-xl font-bold text-green-600">
                      ₹{product.price}/{product.unit}
                    </span>
                    <span
                      className={`status-badge ${
                        product.in_stock
                          ? "status-confirmed"
                          : "status-cancelled"
                      }`}
                    >
                      {product.in_stock ? "In Stock" : "Out of Stock"}
                    </span>
                  </div>
                </div>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => handleEdit(product)}
                  className="btn btn-secondary flex-1"
                >
                  <Edit className="h-4 w-4" />
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(product.id)}
                  className="btn btn-danger"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center p-4">
            <div
              className="fixed inset-0 bg-gray-600 bg-opacity-75"
              onClick={closeModal}
            />
            <div className="relative bg-white rounded-lg shadow-xl max-w-md w-full">
              <div className="p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">
                  {editingProduct ? "Edit Product" : "Add New Product"}
                </h2>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="form-group">
                    <label className="form-label">Product Name</label>
                    <input
                      type="text"
                      className="form-input"
                      value={formData.name}
                      onChange={(e) =>
                        setFormData({ ...formData, name: e.target.value })
                      }
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Description</label>
                    <textarea
                      className="form-input form-textarea"
                      value={formData.description}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          description: e.target.value,
                        })
                      }
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="form-group">
                      <label className="form-label">Price</label>
                      <input
                        type="number"
                        step="0.01"
                        className="form-input"
                        value={formData.price}
                        onChange={(e) =>
                          setFormData({ ...formData, price: e.target.value })
                        }
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label className="form-label">Unit</label>
                      <select
                        className="form-input form-select"
                        value={formData.unit}
                        onChange={(e) =>
                          setFormData({ ...formData, unit: e.target.value })
                        }
                      >
                        <option value="kg">kg</option>
                        <option value="g">g</option>
                        <option value="piece">piece</option>
                        <option value="bunch">bunch</option>
                        <option value="dozen">dozen</option>
                        <option value="packet">packet</option>
                      </select>
                    </div>
                  </div>
                  <div className="form-group">
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={formData.in_stock}
                        onChange={(e) =>
                          setFormData({
                            ...formData,
                            in_stock: e.target.checked,
                          })
                        }
                        className="rounded"
                      />
                      <span className="form-label mb-0">In Stock</span>
                    </label>
                  </div>
                  <div className="flex gap-3 pt-4">
                    <button type="submit" className="btn btn-primary flex-1">
                      {editingProduct ? "Update" : "Create"} Product
                    </button>
                    <button
                      type="button"
                      onClick={closeModal}
                      className="btn btn-secondary"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Products;
