import React, { useState } from 'react';
import Login from './components/Login';
import OrdersTable from './components/OrdersTable';
import UploadModal from './components/UploadModal';

export default function App() {
  const [token, setToken] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);

  if (!token) {
    return <Login onLogin={(t) => setToken(t)} />;
  }

  return (
    <div>
      <button onClick={() => setShowModal(true)}>Import Excel</button>
      <OrdersTable token={token} />
      {showModal && <UploadModal token={token} onClose={() => setShowModal(false)} />}
    </div>
  );
}
