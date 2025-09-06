import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Props {
  token: string;
}

interface Order {
  id: number;
  item: string;
  quantity: number;
}

export default function OrdersTable({ token }: Props) {
  const [orders, setOrders] = useState<Order[]>([]);

  useEffect(() => {
    axios.get('/api/orders').then((res) => setOrders(res.data));
  }, []);

  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Item</th>
          <th>Quantity</th>
        </tr>
      </thead>
      <tbody>
        {orders.map((o) => (
          <tr key={o.id}>
            <td>{o.id}</td>
            <td>{o.item}</td>
            <td>{o.quantity}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
