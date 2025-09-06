import React, { useEffect, useState } from 'react'
import ExcelModal from './ExcelModal'

function OrderRow({ order, onUpdate, onDelete }) {
  const [editing, setEditing] = useState(false)
  const [item, setItem] = useState(order.item)
  const [quantity, setQuantity] = useState(order.quantity)

  function save() {
    onUpdate(order.id, { item, quantity: Number(quantity) })
    setEditing(false)
  }

  return (
    <tr>
      <td>
        {editing ? (
          <input value={item} onChange={(e) => setItem(e.target.value)} />
        ) : (
          order.item
        )}
      </td>
      <td>
        {editing ? (
          <input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
          />
        ) : (
          order.quantity
        )}
      </td>
      <td>
        {editing ? (
          <button onClick={save}>Save</button>
        ) : (
          <button onClick={() => setEditing(true)}>Edit</button>
        )}
        <button onClick={() => onDelete(order.id)}>Delete</button>
      </td>
    </tr>
  )
}

export default function Orders() {
  const [orders, setOrders] = useState([])
  const [item, setItem] = useState('')
  const [quantity, setQuantity] = useState(1)
  const [showModal, setShowModal] = useState(false)

  useEffect(() => {
    fetch('/orders')
      .then((res) => res.json())
      .then(setOrders)
  }, [])

  function refresh() {
    fetch('/orders')
      .then((res) => res.json())
      .then(setOrders)
  }

  function createOrder(e) {
    e.preventDefault()
    fetch('/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ item, quantity: Number(quantity) }),
    })
      .then((res) => res.json())
      .then((order) => setOrders([...orders, order]))
    setItem('')
    setQuantity(1)
  }

  function updateOrder(id, data) {
    fetch(`/orders/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
      .then((res) => res.json())
      .then((updated) =>
        setOrders(orders.map((o) => (o.id === id ? updated : o)))
      )
  }

  function deleteOrder(id) {
    fetch(`/orders/${id}`, { method: 'DELETE' }).then(() =>
      setOrders(orders.filter((o) => o.id !== id))
    )
  }

  return (
    <div>
      <h2>Orders</h2>
      <form onSubmit={createOrder}>
        <input
          value={item}
          onChange={(e) => setItem(e.target.value)}
          placeholder="Item"
        />
        <input
          type="number"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
        />
        <button type="submit">Add</button>
      </form>
      <button onClick={() => setShowModal(true)}>Import Excel</button>
      <ExcelModal
        open={showModal}
        onClose={() => setShowModal(false)}
        onUploaded={refresh}
      />
      <table>
        <thead>
          <tr>
            <th>Item</th>
            <th>Quantity</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order) => (
            <OrderRow
              key={order.id}
              order={order}
              onUpdate={updateOrder}
              onDelete={deleteOrder}
            />
          ))}
        </tbody>
      </table>
    </div>
  )
}
