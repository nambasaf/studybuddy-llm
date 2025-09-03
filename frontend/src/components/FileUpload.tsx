import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

interface FileUploadProps {
  onUploadSuccess: (docId: string) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string>('');

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setUploading(true);
    setUploadStatus('Uploading and processing document...');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setUploadStatus(`✅ Success! Processed ${response.data.chunks_created} chunks`);
      onUploadSuccess(response.data.document_id);
    } catch (error) {
      setUploadStatus('❌ Upload failed. Please try again.');
      console.error('Upload error:', error);
    } finally {
      setUploading(false);
    }
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    multiple: false
  });

  return (
    <div className="upload-section">
      <h2>Upload Your Study Material</h2>
      
      <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
        <input {...getInputProps()} />
        {uploading ? (
          <p>Processing...</p>
        ) : (
          <p>
            {isDragActive
              ? 'Drop your PDF here...'
              : 'Drag & drop a PDF here, or click to select'}
          </p>
        )}
      </div>
      
      {uploadStatus && <p className="upload-status">{uploadStatus}</p>}
    </div>
  );
};

export default FileUpload;