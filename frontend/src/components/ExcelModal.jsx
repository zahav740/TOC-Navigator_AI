import React, { useState } from 'react'

export default function ExcelModal({ open, onClose, onUploaded }) {
  const [file, setFile] = useState(null)

  function upload(e) {
    e.preventDefault()
    if (!file) return
    const formData = new FormData()
    formData.append('file', file)
    fetch('/orders/import-excel', { method: 'POST', body: formData }).then(() => {
      onUploaded && onUploaded()
      setFile(null)
      onClose()
    })
  }

  if (!open) return null
  return (
    <div className="modal">
      <form onSubmit={upload}>
        <input
          type="file"
          accept=".xls,.xlsx"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button type="submit">Upload</button>
        <button type="button" onClick={onClose}>
          Close
        </button>
      </form>
    </div>
  )
}
