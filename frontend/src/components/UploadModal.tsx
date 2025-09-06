import React, { useState } from 'react';
import axios from 'axios';

interface Props {
  token: string;
  onClose: () => void;
}

export default function UploadModal({ token, onClose }: Props) {
  const [file, setFile] = useState<File | null>(null);

  const handleUpload = async () => {
    if (!file) return;
    const form = new FormData();
    form.append('file', file);
    await axios.post('/api/orders/import-excel', form);
    onClose();
  };

  return (
    <div>
      <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <button onClick={handleUpload}>Upload</button>
      <button onClick={onClose}>Close</button>
    </div>
  );
}
